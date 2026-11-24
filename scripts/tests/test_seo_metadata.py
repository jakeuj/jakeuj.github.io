"""Tests for scripts/seo_metadata.py."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import seo_metadata as seo  # noqa: E402

URL = "https://jakeuj.com/excel.html"


def page(description="", url=URL, body="", extra_head=""):
    meta = f'<meta name="description" content="{description}">' if description else ""
    return (
        '<!DOCTYPE html><html lang="en-US"><head><title>Excel</title>'
        f"{meta}"
        '<meta property="og:description" content="">'
        '<meta property="og:locale" content="en_US">'
        f'<meta property="og:url" content="{url}">'
        '<meta name="twitter:description" content="">'
        '<script type="application/ld+json">{"description": "", "inLanguage":"en-US"}</script>'
        f"{extra_head}</head><body><main><article class=\"article\"><h1>Excel</h1>"
        '<aside class="prompt"><p>首次發表：2023-06-13</p></aside>'
        f"{body}</article></main></body></html>"
    )


SITEMAP = (
    '<?xml version="1.0" encoding="UTF-8"?>'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    "<url><loc>https://jakeuj.com/excel.html</loc><lastmod>2026-02-12</lastmod></url>"
    "<url><loc>https://jakeuj.com/%E8%88%8A.html</loc><lastmod>2026-02-12</lastmod></url>"
    "</urlset>"
)


class SeoMetadataTest(unittest.TestCase):
    def build(self, pages, sitemap=SITEMAP):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        site = Path(tmp.name)
        for name, text in pages.items():
            (site / name).write_text(text, encoding="utf-8")
        (site / "sitemap.xml").write_text(sitemap, encoding="utf-8")
        return site

    def test_derives_description_and_syncs_every_copy(self):
        body = "<p>筆記下 MiniExcel</p><section><h2>填充</h2><p>" + "使用樣板填充來產生 Excel 檔案，" * 8 + "</p></section>"
        out = seo.normalize_page(page(body=body))
        description = out.split('<meta name="description" content="')[1].split('"')[0]
        self.assertTrue(description.startswith("筆記下 MiniExcel 使用樣板填充"))
        self.assertLessEqual(len(description), seo.DESCRIPTION_LIMIT)
        self.assertNotIn("首次發表", description)
        self.assertIn(f'<meta property="og:description" content="{description}">', out)
        self.assertIn(f'<meta name="twitter:description" content="{description}">', out)
        self.assertIn(f'"description": "{description}"', out)
        self.assertIn('<html lang="zh-TW"', out)
        self.assertIn('"inLanguage":"zh-TW"', out)

    def test_keeps_web_summary_description(self):
        out = seo.normalize_page(page(description="手寫摘要", body="<p>正文</p>"))
        self.assertEqual(out.count('<meta name="description"'), 1)
        self.assertIn('<meta property="og:description" content="手寫摘要">', out)

    def test_paragraphs_starting_with_a_link_are_skipped(self):
        body = "<p>https://nodejs.org/en/download/</p><p>安裝 Node.js 的步驟，" + "說明" * 30 + "</p>"
        self.assertTrue(seo.derive_description(page(body=body)).startswith("安裝 Node.js"))

    def test_code_and_figures_do_not_become_descriptions(self):
        body = "<figure><p>圖說</p></figure><pre><p>code</p></pre><p>真正的第一段文字，" + "內容" * 30 + "</p>"
        self.assertTrue(seo.derive_description(page(body=body)).startswith("真正的第一段文字"))

    def test_canonical_is_added_once_and_idempotent(self):
        once = seo.normalize_page(page(body="<p>內文</p>"))
        self.assertEqual(seo.canonicals(once), [URL])
        self.assertEqual(seo.normalize_page(once), once)

    def test_redirect_pages_are_left_alone(self):
        text = page(extra_head='<meta http-equiv="refresh" content="0; url=new.html">')
        self.assertEqual(seo.normalize_page(text), text)

    def test_noindex_page_is_marked_and_leaves_the_sitemap(self):
        listed = {"https://jakeuj.com/舊.html"}
        site = self.build(
            {
                "excel.html": page(body="<p>內文</p>"),
                "old.html": page(url="https://jakeuj.com/%E8%88%8A.html", body="<p>舊文</p>"),
            }
        )
        seo.normalize(site, listed)
        old = (site / "old.html").read_text(encoding="utf-8")
        self.assertIn(seo.NOINDEX_TAG, old)
        self.assertEqual(seo.canonicals(old), [])
        sitemap = (site / "sitemap.xml").read_text(encoding="utf-8")
        self.assertNotIn("<lastmod>", sitemap)
        self.assertNotIn("%E8%88%8A", sitemap)
        self.assertIn("<loc>https://jakeuj.com/excel.html</loc>", sitemap)
        seo.validate(site, listed)

    def test_listed_page_must_exist(self):
        site = self.build({"excel.html": page(body="<p>內文</p>")})
        with self.assertRaisesRegex(ValueError, "not built"):
            seo.normalize(site, {"https://jakeuj.com/missing.html"})

    def test_validate_reports_hotlinked_images_and_missing_canonical(self):
        site = self.build(
            {"excel.html": page(body='<p>x</p><img src="https://dotblogsfile.blob.core.windows.net/a.png">')},
            sitemap=SITEMAP.replace("<lastmod>2026-02-12</lastmod>", ""),
        )
        with self.assertRaises(ValueError) as caught:
            seo.validate(site, set())
        self.assertIn("dotblogsfile", str(caught.exception))
        self.assertIn("canonical", str(caught.exception))

    def test_noindex_file_rejects_other_hosts(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "seo-noindex.txt"
            path.write_text("# comment\nhttps://jakeuj.com/%E8%88%8A.html\n", encoding="utf-8")
            self.assertEqual(seo.load_noindex(path), {"https://jakeuj.com/舊.html"})
            path.write_text("https://example.com/a.html\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                seo.load_noindex(path)
        self.assertEqual(seo.load_noindex(Path("/nonexistent/seo-noindex.txt")), set())


if __name__ == "__main__":
    unittest.main()
