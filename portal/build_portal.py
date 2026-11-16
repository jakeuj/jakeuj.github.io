#!/usr/bin/env python3
"""Build the jakeuj.com portal (index.html) into a built Pages site directory.

Reads portal/sites.json and the publication data used for the RSS feed, then:
  * writes <site>/index.html (replaces Writerside's redirect stub),
  * adds the root URL to <site>/sitemap.xml,
  * adds Sitemap lines for project sites already served from jakeuj.com to <site>/robots.txt.

Running it again on the same site directory gives the same result.
Python standard library only.
"""

import argparse
from datetime import datetime, timedelta, timezone
import html
import json
from pathlib import Path
from string import Template
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
PORTAL = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))

import publication  # noqa: E402  (shared loader for data/posts.json)

SITE_URL = "https://jakeuj.com/"
NOTES_URL = "https://jakeuj.com/default.html"
OG_IMAGE = "https://jakeuj.com/images/og-image.png"
TITLE = "Jakeuj｜技術筆記與作品"
DESCRIPTION = (
    "Jakeuj 的個人網站入口：.NET、ABP、Azure、Docker、AI 工具與 macOS 的技術筆記，"
    "以及 Guild Wars 2、Path of Exile 中文化與各種瀏覽器小工具。"
)
GITHUB = "https://github.com/jakeuj"
LATEST_COUNT = 5
TOPICS = [
    (".NET／C#", "c-sharp.html"),
    ("ABP", "abp.html"),
    ("Azure", "azure.html"),
    ("Docker", "docker.html"),
    ("AI／LLM", "llm.html"),
    ("macOS 開發環境", "macos-dotfiles-guide.html"),
]
REQUIRED = ("slug", "name", "description", "category", "url", "repo")

THEME_SCRIPT = """(function () {
  try {
    var t = localStorage.getItem("jakeuj-portal:theme");
    if (t === "light" || t === "dark") document.documentElement.setAttribute("data-theme", t);
  } catch (e) {}
})();"""

TOGGLE_SCRIPT = """(function () {
  var root = document.documentElement;
  var btn = document.getElementById("theme-toggle");
  if (!btn) return;
  function current() {
    var t = root.getAttribute("data-theme");
    if (t) return t;
    return window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  function label() {
    btn.setAttribute("aria-label", current() === "dark" ? "切換為淺色模式" : "切換為深色模式");
  }
  btn.addEventListener("click", function () {
    var next = current() === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    try { localStorage.setItem("jakeuj-portal:theme", next); } catch (e) {}
    label();
  });
  label();
})();"""

PAGE = Template("""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>$title</title>
<meta name="description" content="$description">
<link rel="canonical" href="$site_url">
<link rel="icon" type="image/png" sizes="16x16" href="images/miku.png">
<meta name="theme-color" content="#fff8f8" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#1a1316" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Jakeuj">
<meta property="og:locale" content="zh_TW">
<meta property="og:title" content="$title">
<meta property="og:description" content="$description">
<meta property="og:url" content="$site_url">
<meta property="og:image" content="$og_image">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Jakeuj 筆記本">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@jakeuj">
<meta name="twitter:creator" content="@jakeuj">
<meta name="twitter:title" content="$title">
<meta name="twitter:description" content="$description">
<meta name="twitter:image" content="$og_image">
<meta name="twitter:image:alt" content="Jakeuj 筆記本">
<script type="application/ld+json">$jsonld</script>
<script>$theme_script</script>
<style>
$css</style>
</head>
<body>
<a class="skip-link" href="#main">跳到主要內容</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="./" aria-label="Jakeuj 首頁">
      <img src="images/hatsune-miku-seeklogo.svg" alt="" width="70" height="30">
      <span>Jakeuj</span>
    </a>
    <nav class="site-nav" aria-label="主要導覽">
      <a href="#notes">筆記</a>
      <a href="#projects">作品</a>
      <a href="$github">GitHub</a>
    </nav>
    <button class="theme-toggle" id="theme-toggle" type="button" aria-label="切換深淺色模式">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9z"/></svg>
    </button>
  </div>
</header>
<main id="main">
  <div class="hero">
    <div class="wrap hero-grid">
      <div>
        <h1>Jakeuj 的<span class="accent">筆記</span>與<span class="accent">作品</span></h1>
        <p class="lead">工作上遇到的 .NET、ABP、Azure、Docker、AI 工具與 macOS 問題，整理成可以直接照做的筆記；下班後做的遊戲中文化、插件與瀏覽器小工具，也都從這裡進去。</p>
        <div class="actions">
          <a class="btn btn-primary" href="default.html">閱讀技術筆記</a>
          <a class="btn btn-ghost" href="#projects">看看作品</a>
        </div>
      </div>
      <div class="avatar"><img src="images/miku.png" alt="Jakeuj 的初音頭像" width="256" height="256"></div>
    </div>
  </div>

  <section id="notes" aria-labelledby="notes-title">
    <div class="wrap">
      <div class="section-head">
        <h2 id="notes-title">技術筆記</h2>
        <p>實作、部署與排錯紀錄，持續更新。</p>
      </div>
      <div class="notes-grid">
        <div class="panel notes-intro">
          <h3><a href="default.html">Jakeuj 筆記本</a></h3>
          <p>依主題分類的公開知識庫，每篇都記錄環境、步驟與驗證方式。</p>
          <ul class="chips" aria-label="筆記主題">
$topics
          </ul>
          <p class="more"><a href="recent-posts.html">依日期瀏覽所有文章</a> · <a href="feed.xml">RSS 訂閱</a></p>
        </div>
        <div class="panel latest">
          <h3>最新文章</h3>
          <ol class="posts">
$latest
          </ol>
        </div>
      </div>
    </div>
  </section>

  <section id="projects" aria-labelledby="projects-title">
    <div class="wrap">
      <div class="section-head">
        <h2 id="projects-title">作品與工具</h2>
        <p>都是開源專案，原始碼在 GitHub。</p>
      </div>
$categories
    </div>
  </section>
</main>
<footer class="site-footer">
  <div class="wrap">
    <p>© $year Jakeuj</p>
    <ul>
      <li><a href="default.html">技術筆記</a></li>
      <li><a href="feed.xml">RSS</a></li>
      <li><a href="$github">GitHub</a></li>
      <li><a href="https://www.linkedin.com/in/jakeuj/">LinkedIn</a></li>
      <li><a href="https://www.youtube.com/@Jakeuj">YouTube</a></li>
    </ul>
  </div>
</footer>
<script>$toggle_script</script>
</body>
</html>
""")


def esc(value):
    return html.escape(value, quote=True)


def load_sites(path=PORTAL / "sites.json"):
    data = json.loads(path.read_text(encoding="utf-8"))
    categories = data["categories"]
    category_ids = [c["id"] for c in categories]
    if len(set(category_ids)) != len(category_ids):
        raise ValueError("Duplicate category id")
    slugs = set()
    for site in data["sites"]:
        missing = [k for k in REQUIRED if not str(site.get(k, "")).strip()]
        if missing:
            raise ValueError(f"Site {site.get('slug', '?')} missing {', '.join(missing)}")
        slug = site["slug"]
        if slug in slugs:
            raise ValueError(f"Duplicate slug: {slug}")
        slugs.add(slug)
        if slug != slug.lower() or "/" in slug:
            raise ValueError(f"Slug must be lowercase without slashes: {slug}")
        if site["category"] not in category_ids:
            raise ValueError(f"Unknown category for {slug}: {site['category']}")
        url = urlsplit(site["url"])
        if url.scheme != "https" or not url.netloc or not url.path.endswith("/"):
            raise ValueError(f"Site URL must be https and end with '/': {site['url']}")
        if url.netloc == "jakeuj.com" and url.path != f"/{slug}/":
            raise ValueError(f"jakeuj.com URL must be /{slug}/: {site['url']}")
        if "sitemap" in site and not isinstance(site["sitemap"], bool):
            raise ValueError(f"sitemap must be true/false: {slug}")
    return data


def on_main_host(site):
    return urlsplit(site["url"]).netloc == "jakeuj.com"


def project_sitemaps(sites):
    return [s["url"] + "sitemap.xml" for s in sites if s.get("sitemap") and on_main_host(s)]


def render_topics():
    return "\n".join(
        f'            <li><a href="{esc(href)}">{esc(name)}</a></li>' for name, href in TOPICS
    )


def render_latest(posts):
    items = []
    for p in posts[:LATEST_COUNT]:
        path = urlsplit(p["url"]).path.lstrip("/")
        items.append(
            "            <li>"
            f'<a href="{esc(path)}">{esc(p["title"])}</a>'
            f'<time datetime="{esc(p["published"])}">{esc(p["published"])}</time>'
            f'<p>{esc(p["summary"])}</p>'
            "</li>"
        )
    return "\n".join(items)


def render_categories(data):
    blocks = []
    for cat in data["categories"]:
        sites = [s for s in data["sites"] if s["category"] == cat["id"]]
        if not sites:
            continue
        cards = []
        for s in sites:
            href = urlsplit(s["url"]).path if on_main_host(s) else s["url"]
            shown = "jakeuj.com" + href if on_main_host(s) else urlsplit(s["url"]).netloc
            cards.append(
                '          <article class="card">\n'
                f'            <h4><a href="{esc(href)}">{esc(s["name"])}</a></h4>\n'
                f'            <p>{esc(s["description"])}</p>\n'
                '            <p class="meta">'
                f'<span class="path">{esc(shown)}</span>'
                f'<a href="{esc(GITHUB + "/" + s["repo"])}">GitHub</a></p>\n'
                "          </article>"
            )
        blocks.append(
            f'      <div class="category" id="cat-{esc(cat["id"])}">\n'
            f'        <h3>{esc(cat["name"])}</h3>\n'
            f'        <p>{esc(cat["description"])}</p>\n'
            '        <div class="cards">\n' + "\n".join(cards) + "\n        </div>\n"
            "      </div>"
        )
    return "\n".join(blocks)


def render_jsonld():
    website = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": f"{SITE_URL}#website",
        "url": SITE_URL,
        "name": "Jakeuj",
        "alternateName": ["Jakeuj 筆記本", "jakeuj.com"],
        "description": DESCRIPTION,
        "inLanguage": "zh-TW",
    }
    return json.dumps(website, ensure_ascii=False).replace("</", "<\\/")


def render_page(data, posts, year):
    return PAGE.substitute(
        title=esc(TITLE),
        description=esc(DESCRIPTION),
        site_url=SITE_URL,
        og_image=OG_IMAGE,
        github=GITHUB,
        jsonld=render_jsonld(),
        theme_script=THEME_SCRIPT,
        toggle_script=TOGGLE_SCRIPT,
        css=(PORTAL / "portal.css").read_text(encoding="utf-8"),
        topics=render_topics(),
        latest=render_latest(posts),
        categories=render_categories(data),
        year=year,
    )


def update_sitemap(path):
    text = path.read_text(encoding="utf-8")
    entry = f"<url><loc>{SITE_URL}</loc><changefreq>weekly</changefreq><priority>1</priority></url>"
    if f"<loc>{SITE_URL}</loc>" in text:
        return False
    marker = 'xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    if marker not in text:
        raise ValueError("sitemap.xml has no <urlset> opening tag")
    path.write_text(text.replace(marker, marker + entry, 1), encoding="utf-8")
    return True


def update_robots(path, sitemaps):
    lines = path.read_text(encoding="utf-8").rstrip("\n").split("\n")
    present = {line.strip() for line in lines}
    added = [f"Sitemap: {url}" for url in sitemaps if f"Sitemap: {url}" not in present]
    if added:
        path.write_text("\n".join(lines + added) + "\n", encoding="utf-8")
    return added


def build(site, root=ROOT, sites_path=PORTAL / "sites.json", now=None):
    site = Path(site)
    data = load_sites(sites_path)
    posts = publication.load(root)["posts"]
    if len(posts) < LATEST_COUNT:
        raise ValueError("Not enough published posts for the latest list")
    now = now or datetime.now(timezone(timedelta(hours=8)))
    (site / "index.html").write_text(render_page(data, posts, now.year), encoding="utf-8")
    update_sitemap(site / "sitemap.xml")
    added = update_robots(site / "robots.txt", project_sitemaps(data["sites"]))
    return {"sites": len(data["sites"]), "robots_added": added}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, help="built Pages directory (e.g. dir)")
    parser.add_argument("--check", action="store_true", help="validate sites.json only")
    args = parser.parse_args()
    try:
        if args.check:
            data = load_sites()
            print(f"Portal check: OK ({len(data['sites'])} sites)")
            return 0
        if not args.site:
            parser.error("--site is required unless --check is given")
        result = build(args.site)
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as e:
        print(f"Portal build failed: {e}", file=sys.stderr)
        return 1
    print(f"Portal build: OK ({result['sites']} sites, robots +{len(result['robots_added'])})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
