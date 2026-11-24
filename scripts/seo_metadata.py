#!/usr/bin/env python3
"""Normalize and validate SEO metadata in a built Writerside site (standard library only).

normalize --site DIR
    For every top-level Writerside page in DIR (pages with og:url and no meta refresh):
    * set the document language to zh-TW,
    * use the meta description, or derive one from the first paragraphs of the article,
      and copy it to og:description, twitter:description and the WebPage JSON-LD,
    * add a self canonical (the page's og:url),
    * for pages listed in data/seo-noindex.txt: add noindex and drop the canonical.
    In DIR/sitemap.xml: remove every <lastmod> and the URLs of noindex pages.

validate --site DIR
    Check the result: one canonical equal to og:url on every indexable page, no canonical and a
    noindex tag on listed pages, no hot-linked dotblogs images, no <lastmod>, and no noindex URL in
    the sitemap.

Running normalize twice gives the same result.
"""

import argparse
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SITE_URL = "https://jakeuj.com/"
NOINDEX_FILE = ROOT / "data/seo-noindex.txt"
NOINDEX_TAG = '<meta name="robots" content="noindex, follow">'
DESCRIPTION_LIMIT = 120
DESCRIPTION_MIN = 50
SKIP_TAGS = {"aside", "pre", "code", "figure", "table", "footer", "script", "style", "nav"}


def load_noindex(path=NOINDEX_FILE):
    """URLs (https://jakeuj.com/<page>.html), one per line; '#' starts a comment."""
    if not path.exists():
        return set()
    urls = set()
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        value = line.split("#", 1)[0].strip()
        if not value:
            continue
        if not value.startswith(SITE_URL) or not value.endswith(".html"):
            raise ValueError(f"{path.name}:{number}: expected {SITE_URL}<page>.html, got {value!r}")
        urls.add(unquote(value))
    return urls


class Article(HTMLParser):
    """Text of <p> elements inside <article>, skipping metadata blocks and code."""

    def __init__(self):
        super().__init__()
        self.depth = 0  # inside <article>
        self.skip = 0  # inside a skipped element
        self.in_p = False
        self.paragraphs = []
        self._buf = []

    def handle_starttag(self, tag, attrs):
        if tag == "article":
            self.depth += 1
        elif self.depth and tag in SKIP_TAGS:
            self.skip += 1
        elif self.depth and not self.skip and tag == "p":
            self.in_p = True
            self._buf = []

    def handle_endtag(self, tag):
        if tag == "article" and self.depth:
            self.depth -= 1
        elif self.depth and tag in SKIP_TAGS and self.skip:
            self.skip -= 1
        elif tag == "p" and self.in_p:
            self.in_p = False
            text = re.sub(r"\s+", " ", "".join(self._buf)).strip()
            if text:
                self.paragraphs.append(text)

    def handle_data(self, data):
        if self.in_p and not self.skip:
            self._buf.append(data)


def derive_description(page):
    parser = Article()
    parser.feed(page)
    text = ""
    for paragraph in parser.paragraphs:
        if re.match(r"^(首次發表|標籤)[：:]|^https?://", paragraph):
            continue
        text = f"{text} {paragraph}".strip() if text else paragraph
        if len(text) >= DESCRIPTION_MIN:
            break
    if not text:
        return ""
    if len(text) > DESCRIPTION_LIMIT:
        text = text[: DESCRIPTION_LIMIT - 1].rstrip("，。、；：,.;: ") + "…"
    return text


def og_url(page):
    match = re.search(r'<meta property="og:url" content="([^"]*)">', page)
    return match.group(1) if match else ""


def is_redirect(page):
    return bool(re.search(r'http-equiv="refresh"', page[: page.find("</head>") + 1 or 2000], re.I))


def canonicals(page):
    return re.findall(r'<link rel="canonical" href="([^"]*)">', page)


def normalize_language(page):
    page = re.sub(r'<html lang="[^"]+"', '<html lang="zh-TW"', page, count=1)
    page = re.sub(
        r'(<meta property="og:locale" content=")[^"]*(">)', r"\1zh_TW\2", page, count=1
    )
    return re.sub(r'("inLanguage"\s*:\s*)"[^"]*"', r'\1"zh-TW"', page)


def normalize_page(page, noindex_urls=frozenset()):
    """Return the normalized page text."""
    url = og_url(page)
    if not url or is_redirect(page):
        return page
    page = normalize_language(page)

    match = re.search(r'<meta name="description" content="([^"]+)">', page)
    if match:
        description_attr = match.group(1)
    else:
        description = derive_description(page)
        description_attr = html.escape(description, quote=True) if description else ""
        if description_attr and "</head>" in page:
            page = page.replace(
                "</head>", f'<meta name="description" content="{description_attr}"></head>', 1
            )
    if description_attr:
        description_json = json.dumps(html.unescape(description_attr), ensure_ascii=False)
        page = re.sub(
            r'(<meta property="og:description" content=")[^"]*(">)',
            lambda m: f"{m.group(1)}{description_attr}{m.group(2)}",
            page,
            count=1,
        )
        page = re.sub(
            r'(<meta name="twitter:description" content=")[^"]*(">)',
            lambda m: f"{m.group(1)}{description_attr}{m.group(2)}",
            page,
            count=1,
        )
        page = re.sub(
            r'("description":\s*)""', lambda m: f"{m.group(1)}{description_json}", page, count=1
        )

    noindex = unquote(url) in noindex_urls
    if noindex and NOINDEX_TAG not in page:
        page = page.replace("</head>", f"{NOINDEX_TAG}</head>", 1)
    if not noindex and not canonicals(page) and "</head>" in page:
        page = page.replace(
            "</head>", f'<link rel="canonical" href="{html.escape(url, quote=True)}"></head>', 1
        )
    return page


def normalize_sitemap(text, noindex_urls=frozenset()):
    text = re.sub(r"\s*<lastmod>[^<]*</lastmod>", "", text)

    def keep(match):
        loc = re.search(r"<loc>([^<]*)</loc>", match.group(0))
        if loc and unquote(html.unescape(loc.group(1))) in noindex_urls:
            return ""
        return match.group(0)

    return re.sub(r"<url>.*?</url>\s*", keep, text, flags=re.S)


def pages(site):
    return sorted(Path(site).glob("*.html"))


def normalize(site, noindex_urls=None):
    site = Path(site)
    noindex_urls = load_noindex() if noindex_urls is None else noindex_urls
    built = set()
    patched = described = 0
    for path in pages(site):
        text = path.read_text(encoding="utf-8")
        url = og_url(text)
        if url:
            built.add(unquote(url))
        updated = normalize_page(text, noindex_urls)
        if '<meta name="description"' not in text and '<meta name="description"' in updated:
            described += 1
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            patched += 1
    missing = sorted(noindex_urls - built)
    if missing:
        raise ValueError("seo-noindex.txt lists pages that were not built: " + ", ".join(missing))
    sitemap = site / "sitemap.xml"
    text = sitemap.read_text(encoding="utf-8")
    updated = normalize_sitemap(text, noindex_urls)
    if updated != text:
        sitemap.write_text(updated, encoding="utf-8")
    print(f"Patched SEO metadata in {patched} pages ({described} derived descriptions)")


def validate(site, noindex_urls=None):
    site = Path(site)
    noindex_urls = load_noindex() if noindex_urls is None else noindex_urls
    errors = []
    undescribed = 0
    for path in pages(site):
        text = path.read_text(encoding="utf-8")
        url = og_url(text)
        if "dotblogsfile.blob.core.windows.net" in text:
            errors.append(f"{path.name}: still loads images from dotblogsfile")
        if not url or is_redirect(text):
            continue
        if unquote(url) in noindex_urls:
            if NOINDEX_TAG not in text:
                errors.append(f"{path.name}: listed in seo-noindex.txt but has no noindex tag")
            if canonicals(text):
                errors.append(f"{path.name}: noindex page must not have a canonical")
            continue
        if canonicals(text) != [url]:
            errors.append(f"{path.name}: canonical {canonicals(text)} != og:url {url}")
        if not re.search(r'<meta name="description" content="[^"]+"', text):
            undescribed += 1
    sitemap = (site / "sitemap.xml").read_text(encoding="utf-8")
    if "<lastmod>" in sitemap:
        errors.append("sitemap.xml: contains <lastmod>")
    listed = {unquote(html.unescape(u)) for u in re.findall(r"<loc>([^<]*)</loc>", sitemap)}
    for url in sorted(noindex_urls & listed):
        errors.append(f"sitemap.xml: contains noindex page {url}")
    if undescribed:
        print(f"::warning::{undescribed} pages have no meta description")
    if errors:
        raise ValueError("SEO validation failed:\n" + "\n".join(errors[:50]))
    print(f"SEO metadata OK: {len(pages(site))} pages, {len(noindex_urls)} noindex")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("command", choices=["normalize", "validate"])
    parser.add_argument("--site", type=Path, default=Path("dir"))
    args = parser.parse_args()
    {"normalize": normalize, "validate": validate}[args.command](args.site)


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        print(f"::error::{error}")
        sys.exit(1)
