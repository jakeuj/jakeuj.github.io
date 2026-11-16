import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_portal  # noqa: E402

SITEMAP = (
    "<?xml version='1.0' encoding='UTF-8'?>"
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    "<url><loc>https://jakeuj.com/default.html</loc></url></urlset>"
)
ROBOTS = "User-agent: *\nAllow: /\n\nSitemap: https://jakeuj.com/sitemap.xml\n"


class BuildPortalTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.site = Path(self.tmp.name)
        (self.site / "sitemap.xml").write_text(SITEMAP, encoding="utf-8")
        (self.site / "robots.txt").write_text(ROBOTS, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_build_is_idempotent_and_complete(self):
        def snapshot():
            return {str(p.relative_to(self.site)): p.read_text(encoding="utf-8") for p in self.site.rglob("*") if p.is_file()}

        build_portal.build(self.site)
        first = snapshot()
        build_portal.build(self.site)
        second = snapshot()
        self.assertEqual(first, second)

        page = second["index.html"]
        self.assertIn('<link rel="canonical" href="https://jakeuj.com/">', page)
        self.assertNotIn("http-equiv=\"refresh\"", page)
        self.assertIn('<html lang="zh-TW">', page)
        self.assertIn("https://jakeuj.com/images/og-image.png", page)
        self.assertEqual(page.count('class="card"'), len(build_portal.load_sites()["sites"]))
        self.assertEqual(page.count("<time datetime="), build_portal.LATEST_COUNT)

        self.assertEqual(second["sitemap.xml"].count("<loc>https://jakeuj.com/</loc>"), 1)
        robots = second["robots.txt"]
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
                stub = second[f"{alias}/index.html"]
                self.assertIn(f'href="{s["url"]}"', stub)
                self.assertIn('content="noindex"', stub)

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
