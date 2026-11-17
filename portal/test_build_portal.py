from datetime import datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import struct
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_portal  # noqa: E402

SITEMAP = (
    "<?xml version='1.0' encoding='UTF-8'?>"
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    "<url><loc>https://jakeuj.com/default.html</loc></url></urlset>"
)
ROBOTS = "User-agent: *\nAllow: /\n\nSitemap: https://jakeuj.com/sitemap.xml\n"
NOW = datetime(2026, 11, 17, tzinfo=timezone.utc)


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.jsonld = []
        self.in_jsonld = False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag == "script":
            self.in_jsonld = attrs.get("type") == "application/ld+json"

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_jsonld = False

    def handle_data(self, text):
        if self.in_jsonld:
            self.jsonld.append(json.loads(text))

    def find(self, tag, **attrs):
        return [a for t, a in self.tags if t == tag and all(a.get(k) == v for k, v in attrs.items())]


class BuildPortalTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.site = Path(self.tmp.name)
        (self.site / "sitemap.xml").write_text(SITEMAP, encoding="utf-8")
        (self.site / "robots.txt").write_text(ROBOTS, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def load_data(self, data):
        path = self.site / "sites.json"
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        return build_portal.load_sites(path)

    def built_page(self):
        build_portal.build(self.site, now=NOW)
        return Page((self.site / "index.html").read_text(encoding="utf-8"))

    def test_build_is_idempotent_and_complete(self):
        def snapshot():
            return {str(p.relative_to(self.site)): p.read_bytes() for p in self.site.rglob("*") if p.is_file()}

        build_portal.build(self.site, now=NOW)
        first = snapshot()
        build_portal.build(self.site, now=NOW)
        second = snapshot()
        self.assertEqual(first, second)

        page = second["index.html"].decode("utf-8")
        self.assertIn('<link rel="canonical" href="https://jakeuj.com/">', page)
        self.assertNotIn("http-equiv=\"refresh\"", page)
        self.assertIn('<html lang="zh-TW">', page)
        self.assertIn("https://jakeuj.com/portal/portal-og.png", page)
        self.assertEqual(page.count('class="card"'), len(build_portal.load_sites()["sites"]))
        self.assertEqual(page.count("<time datetime="), build_portal.LATEST_COUNT)

        self.assertEqual(second["sitemap.xml"].count(b"<loc>https://jakeuj.com/</loc>"), 1)
        robots = second["robots.txt"].decode("utf-8")
        self.assertTrue(robots.endswith("\n"))
        sites = build_portal.load_sites()["sites"]
        for url in build_portal.project_sitemaps(sites):
            self.assertEqual(robots.count(f"Sitemap: {url}\n"), 1)
            self.assertTrue(url.startswith("https://jakeuj.com/"))
        for rule in build_portal.robots_disallows(sites):
            self.assertEqual(robots.count(rule + "\n"), 1)
            self.assertLess(robots.index(rule), robots.index("Sitemap:"))
        for s in sites:
            for alias in s.get("aliases", []) if build_portal.on_main_host(s) else []:
                stub = second[f"{alias}/index.html"].decode("utf-8")
                self.assertIn(f'href="{s["url"]}"', stub)
                self.assertIn('content="noindex"', stub)

    def test_jsonld_links_website_person_and_visible_projects(self):
        page = self.built_page()
        self.assertEqual(len(page.jsonld), 1)
        graph = page.jsonld[0]
        self.assertEqual(graph["@context"], "https://schema.org")
        website, person, projects = graph["@graph"]
        self.assertEqual([n["@type"] for n in graph["@graph"]], ["WebSite", "Person", "ItemList"])
        self.assertEqual(website["url"], "https://jakeuj.com/")
        self.assertEqual(website["publisher"], {"@id": person["@id"]})
        self.assertEqual(website["mainEntity"], {"@id": projects["@id"]})
        data = build_portal.load_sites()
        self.assertEqual({k: person[k] for k in data["person"]}, data["person"])
        expected = [s for c in data["categories"] for s in data["sites"]
                    if s["category"] == c["id"] and s["url"].startswith("https://jakeuj.com/")]
        self.assertEqual(projects["numberOfItems"], len(expected))
        self.assertEqual([e["position"] for e in projects["itemListElement"]], list(range(1, len(expected) + 1)))
        for item, site in zip(projects["itemListElement"], expected):
            self.assertEqual(item["@type"], "ListItem")
            self.assertEqual({k: item[k] for k in ("name", "description", "url")},
                             {k: site[k] for k in ("name", "description", "url")})
            self.assertEqual(len(page.find("a", href=f'/{site["slug"]}/')), 1)

    def test_jsonld_excludes_other_hosts_and_keeps_visible_order(self):
        data = build_portal.load_sites()
        data["categories"].reverse()
        first, second = data["sites"][0], data["sites"][1]
        first["url"] = "https://old.jakeuj.com/"
        second["url"] = "https://jakeuj.com.example.org/"
        projects = json.loads(build_portal.render_jsonld(data))["@graph"][2]
        expected = [s["url"] for c in data["categories"] for s in data["sites"]
                    if s["category"] == c["id"] and s not in (first, second)]
        self.assertEqual([e["url"] for e in projects["itemListElement"]], expected)
        self.assertEqual(projects["numberOfItems"], len(data["sites"]) - 2)
        self.assertEqual([e["position"] for e in projects["itemListElement"]], list(range(1, len(expected) + 1)))

    def test_jsonld_handles_no_main_host_projects(self):
        data = build_portal.load_sites()
        for site in data["sites"]:
            site["url"] = f'https://{site["slug"]}.example.org/'
        projects = json.loads(build_portal.render_jsonld(data))["@graph"][2]
        self.assertEqual(projects["numberOfItems"], 0)
        self.assertEqual(projects["itemListElement"], [])

    def test_old_sites_json_builds_with_default_person(self):
        data = json.loads((build_portal.PORTAL / "sites.json").read_text(encoding="utf-8"))
        del data["person"]
        loaded = self.load_data(data)
        self.assertEqual(loaded["person"]["name"], "Jakeuj")
        self.assertEqual(loaded["person"]["url"], "https://jakeuj.com/")
        build_portal.build(self.site, sites_path=self.site / "sites.json", now=NOW)
        page = Page((self.site / "index.html").read_text(encoding="utf-8"))
        self.assertEqual(page.jsonld[0]["@graph"][1]["name"], "Jakeuj")

    def test_rejects_invalid_person(self):
        valid = {"name": "Jakeuj", "url": "https://jakeuj.com/"}
        cases = [
            ("null_object", None), ("array_object", []), ("string_object", "Jakeuj"),
            ("missing_name", {"url": valid["url"]}), ("empty_name", {**valid, "name": "  "}),
            ("non_string_name", {**valid, "name": 42}), ("missing_url", {"name": "Jakeuj"}),
            ("null_url", {**valid, "url": None}), ("http_url", {**valid, "url": "http://jakeuj.com/"}),
            ("relative_url", {**valid, "url": "/"}), ("missing_host", {**valid, "url": "https:///"}),
            ("credentials", {**valid, "url": "https://user:secret@jakeuj.com/"}),
            ("whitespace", {**valid, "url": "https://jakeuj.com/ x"}),
            ("bad_port", {**valid, "url": "https://jakeuj.com:invalid/"}),
            ("social_not_list", {**valid, "sameAs": valid["url"]}),
            ("social_null", {**valid, "sameAs": None}),
            ("social_non_url", {**valid, "sameAs": [42]}),
            ("social_http", {**valid, "sameAs": ["http://github.com/jakeuj"]}),
        ]
        for case, person in cases:
            with self.subTest(case=case):
                data = build_portal.load_sites()
                data["person"] = person
                with self.assertRaises(ValueError):
                    self.load_data(data)

    def test_person_without_social_profiles(self):
        for case, extra in [("omitted", {}), ("empty", {"sameAs": []})]:
            with self.subTest(case=case):
                data = build_portal.load_sites()
                data["person"] = {"name": "Jakeuj", "url": "https://jakeuj.com/", **extra}
                person = json.loads(build_portal.render_jsonld(self.load_data(data)))["@graph"][1]
                self.assertNotIn("sameAs", person)

    def test_jsonld_and_cards_escape_user_text(self):
        text = '</script><script>alert("x")</script> & <tag>'
        data = build_portal.load_sites()
        data["person"]["name"] = text
        data["sites"][0].update(name=text, description=text)
        page = Page(build_portal.render_page(data, [], 2026))
        self.assertEqual(len(page.find("script")), 3)
        self.assertEqual(page.find("tag"), [])
        graph = page.jsonld[0]["@graph"]
        self.assertEqual(graph[1]["name"], text)
        self.assertEqual(graph[2]["itemListElement"][0]["name"], text)
        self.assertEqual(graph[2]["itemListElement"][0]["description"], text)
        self.assertEqual(page.find("a", href="https://github.com/jakeuj/coolpc-quote")[0]["aria-label"],
                         text + " 的 GitHub 原始碼")

    def test_images_are_copied_with_correct_dimensions_and_metadata(self):
        page = self.built_page()
        for source in (build_portal.PORTAL / "assets").iterdir():
            self.assertEqual((self.site / "portal" / source.name).read_bytes(), source.read_bytes())
        icons = page.find("link", rel="icon") + page.find("link", rel="apple-touch-icon")
        self.assertEqual({i["sizes"] for i in icons}, {"16x16", "32x32", "48x48", "180x180"})
        for icon in icons:
            blob = (self.site / icon["href"]).read_bytes()
            self.assertEqual(blob[:8], b"\x89PNG\r\n\x1a\n")
            self.assertEqual(struct.unpack(">II", blob[16:24]), tuple(map(int, icon["sizes"].split("x"))))
        image = page.find("img", src="portal/avatar-192.png")[0]
        self.assertEqual((image["width"], image["height"]), ("192", "192"))
        fallback = (self.site / image["src"]).read_bytes()
        self.assertEqual(struct.unpack(">II", fallback[16:24]), (192, 192))
        source = page.find("source", type="image/webp")[0]
        self.assertEqual(source["sizes"], "(min-width: 768px) 174px, 78px")
        candidates = source["srcset"].split(", ")
        self.assertEqual([c.split()[1] for c in candidates], ["96w", "192w", "256w"])
        for candidate in candidates:
            blob = (self.site / candidate.split()[0]).read_bytes()
            self.assertEqual((blob[:4], blob[8:12]), (b"RIFF", b"WEBP"))
            # These pre-generated RGBA assets store their canvas in VP8X.
            self.assertEqual(blob[12:16], b"VP8X")
            size = int(candidate.split()[1][:-1])
            self.assertEqual(tuple(int.from_bytes(blob[i:i + 3], "little") + 1 for i in (24, 27)),
                             (size, size))
        og = (self.site / "portal/portal-og.png").read_bytes()
        self.assertEqual(struct.unpack(">II", og[16:24]), (1200, 630))
        self.assertEqual(page.find("meta", property="og:image")[0]["content"], build_portal.OG_IMAGE)
        self.assertEqual(page.find("meta", name="twitter:image")[0]["content"], build_portal.OG_IMAGE)
        self.assertEqual(page.find("meta", property="og:image:type")[0]["content"], "image/png")
        self.assertEqual(page.find("meta", property="og:image:width")[0]["content"], "1200")
        self.assertEqual(page.find("meta", property="og:image:height")[0]["content"], "630")

    def test_build_uses_only_local_inputs(self):
        expected = sum(build_portal.on_main_host(s) for s in build_portal.load_sites()["sites"])
        with mock.patch("socket.socket", side_effect=AssertionError("Build attempted network access")), \
             mock.patch("socket.getaddrinfo", side_effect=AssertionError("Build attempted DNS lookup")):
            page = self.built_page()
        self.assertEqual(page.jsonld[0]["@graph"][2]["numberOfItems"], expected)

    def test_accessible_markup_and_heading_order(self):
        page = self.built_page()
        self.assertEqual(page.find("main", id="main")[0]["tabindex"], "-1")
        self.assertEqual(len(page.find("a", href="#main")), 1)
        self.assertEqual(len(page.find("h1")), 1)
        previous = 0
        for tag, _ in page.tags:
            if re.fullmatch(r"h[1-6]", tag):
                level = int(tag[1])
                self.assertLessEqual(level, previous + 1)
                previous = level
        for site in build_portal.load_sites()["sites"]:
            link = page.find("a", href="https://github.com/jakeuj/" + site["repo"])[0]
            self.assertEqual(link["aria-label"], site["name"] + " 的 GitHub 原始碼")
        avatar = page.find("img", src="portal/avatar-192.png")[0]
        self.assertEqual(avatar["alt"], "Jakeuj 的初音頭像")
        brand = page.find("img", src="images/hatsune-miku-seeklogo.svg")[0]
        self.assertEqual(brand["alt"], "")

    def test_evennia_stays_visible_without_crawl_or_sitemap_rules(self):
        page = self.built_page()
        self.assertEqual(len(page.find("a", href="/evennia/")), 1)
        urls = [e["url"] for e in page.jsonld[0]["@graph"][2]["itemListElement"]]
        self.assertIn("https://jakeuj.com/evennia/", urls)
        self.assertNotIn("/evennia/", (self.site / "robots.txt").read_text())
        self.assertNotIn("<loc>https://jakeuj.com/evennia/", (self.site / "sitemap.xml").read_text())

    def test_rss_publication_keeps_one_alternate(self):
        self.built_page()
        for _ in range(2):
            build_portal.publication.publish({"posts": []}, self.site)
            page = Page((self.site / "index.html").read_text(encoding="utf-8"))
            self.assertEqual(len(page.find("link", rel="alternate", type="application/rss+xml")), 1)
            self.assertEqual(page.find("link", rel="canonical")[0]["href"], "https://jakeuj.com/")

    def test_color_tokens_meet_text_and_focus_contrast(self):
        css = (build_portal.PORTAL / "portal.css").read_text(encoding="utf-8")
        def tokens(selector):
            block = re.search(re.escape(selector) + r"\s*\{([^}]+)\}", css)[1]
            return dict(re.findall(r"--([\w-]+):\s*(#[0-9a-f]{6});", block))
        def luminance(color):
            channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
            return sum((v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4) * weight
                       for v, weight in zip(channels, (.2126, .7152, .0722)))
        for theme, palette in [("light", tokens(":root")),
                               ("dark", {**tokens(":root"), **tokens(':root[data-theme="dark"]')})]:
            pairs = [(fg, bg) for fg in ("text", "muted", "primary", "accent")
                     for bg in ("bg", "surface", "surface-2")]
            pairs += [("on-primary", "primary"), ("on-primary", "primary-hover")]
            for fg, bg in pairs:
                with self.subTest(theme=theme, foreground=fg, background=bg):
                    values = sorted([luminance(palette[fg]), luminance(palette[bg])])
                    self.assertGreaterEqual((values[1] + .05) / (values[0] + .05), 4.5)

    def test_rejects_duplicate_slug(self):
        data = build_portal.load_sites()
        data["sites"].append(dict(data["sites"][0]))
        path = self.site / "sites.json"
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        with self.assertRaises(ValueError):
            build_portal.load_sites(path)

    def test_rejects_main_host_url_not_matching_slug(self):
        data = build_portal.load_sites()
        data["sites"][0]["url"] = "https://jakeuj.com/somewhere-else/"
        path = self.site / "sites.json"
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        with self.assertRaises(ValueError):
            build_portal.load_sites(path)

    def test_only_main_host_sitemaps_go_to_robots(self):
        sites = [
            {"slug": "a", "url": "https://jakeuj.com/a/", "sitemap": True},
            {"slug": "b", "url": "https://b.jakeuj.com/", "sitemap": True},
            {"slug": "c", "url": "https://jakeuj.com/c/"},
        ]
        self.assertEqual(build_portal.project_sitemaps(sites), ["https://jakeuj.com/a/sitemap.xml"])

    def test_alias_must_not_overwrite_real_page(self):
        sites = [{"slug": "a", "url": "https://jakeuj.com/a/", "aliases": ["old"]}]
        (self.site / "old").mkdir()
        (self.site / "old" / "index.html").write_text("<p>real</p>", encoding="utf-8")
        with self.assertRaises(ValueError):
            build_portal.write_aliases(self.site, sites)


if __name__ == "__main__":
    unittest.main()
