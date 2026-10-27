"""Check the original GitHub visual gallery and the relative README image links."""
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "docs" / "gallery"
NAMES = (
    "astrasentinel-banner.svg",
    "orbital-geometry.svg",
    "satellite-health-intelligence.svg",
    "space-weather-observatory.svg",
    "rocket-flight-analysis.svg",
    "atmospheric-layers.svg",
    "scientific-graphs.svg",
    "mission-control-ui-concept.svg",
)

def test_all_original_artwork_is_parseable_svg():
    for name in NAMES:
        path = ART / name
        assert path.is_file(), name
        data = path.read_text(encoding="utf-8")
        root = ElementTree.fromstring(data)
        assert root.tag == "{http://www.w3.org/2000/svg}svg"
        assert root.get("viewBox"), name
        assert "<script" not in data.lower()
        assert len(data) > 1200, name

def test_readme_gallery_uses_existing_relative_assets():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    index = (ROOT / "docs" / "VISUAL_GALLERY.md").read_text(encoding="utf-8")
    for name in NAMES:
        assert "gallery/" + name in index, name
    for name in NAMES[:6]:
        assert "docs/gallery/" + name in readme, name
    assert "not a screenshot" in index.lower()
