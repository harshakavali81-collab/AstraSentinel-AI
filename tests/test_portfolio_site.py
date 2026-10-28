"""Check static portfolio landing-page links and honest demo labeling."""
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

class AssetLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.assets = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        for key in ("src", "href"):
            value = d.get(key, "")
            if value and not value.startswith(("http:", "https:", "#", "mailto:", "data:")):
                self.assets.append(value.split("#")[0])


def test_portfolio_site_has_no_broken_local_asset_links():
    page = (DOCS / "index.html").read_text(encoding="utf-8")
    parser = AssetLinks()
    parser.feed(page)
    assert len(parser.assets) >= 9
    for asset in parser.assets:
        assert ".." not in Path(asset).parts
        assert (DOCS / asset).is_file(), asset
    assert "synthetic" in page.lower()
    assert "flight" in page.lower()
    assert "not real mission screenshots" in page.lower()


def test_static_site_has_no_required_external_script():
    page = (DOCS / "index.html").read_text(encoding="utf-8")
    assert "<script" not in page
    assert "api/rocket" not in page
    assert (DOCS / "landing.css").is_file()
