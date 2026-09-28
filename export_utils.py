"""Fixed-size vector/text exports and preflight for the F01 pilot."""
import base64
import hashlib
import io
import json
from pathlib import Path
import platform
import shutil
import xml.etree.ElementTree as ET

import pymupdf as fitz
from fontTools import subset
from fontTools.ttLib import TTFont
import matplotlib
import numpy
from PIL import Image
from matplotlib.text import Text

from book_style import STYLE, FONT_PATH, font_properties
from layout_utils import check_layout

STEM = "F01_genome_chromosome_dna_gene"


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def preflight(result):
    report = check_layout(result)
    if not report["passed"]:
        raise ValueError("Layout preflight failed:\n" + json.dumps(report["errors"], ensure_ascii=False, indent=2))
    return report


def embed_svg_font(path, text):
    """Keep editable SVG text, with a self-contained subset webfont.

    Some desktop vector editors ignore SVG @font-face; they can load the
    supplied full font. No text is rasterized or converted to paths here.
    """
    font = TTFont(FONT_PATH, recalcTimestamp=False)
    options = subset.Options()
    options.recalc_timestamp = False
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(text=text)
    subsetter.subset(font)
    font.flavor = "woff"
    stream = io.BytesIO()
    font.save(stream)
    encoded = base64.b64encode(stream.getvalue()).decode("ascii")
    family = font_properties().get_name()
    css = f"<style type=\"text/css\">@font-face{{font-family:'{family}';src:url(data:font/woff;base64,{encoded}) format('woff');font-weight:400;font-style:normal;}}</style>"
    svg = Path(path).read_text()
    if "<defs>" not in svg:
        raise ValueError("SVG defs missing; font embedding was not applied")
    Path(path).write_text(svg.replace("<defs>", "<defs>" + css, 1))


def check_exports(paths, expected_text_count):
    errors = []
    png = Image.open(paths["png"])
    expected = (STYLE.width_mm / 25.4 * STYLE.dpi, STYLE.height_mm / 25.4 * STYLE.dpi)
    if any(abs(a - b) > 1 for a, b in zip(png.size, expected)):
        errors.append("PNG pixel dimensions")
    dpi = png.info.get("dpi", (0, 0))
    if min(dpi) < 300 or any(abs(v - STYLE.dpi) > 0.1 for v in dpi):
        errors.append("PNG dpi")
    pdf = fitz.open(paths["pdf"])
    page = pdf[0]
    pdf_mm = [page.rect.width / 72 * 25.4, page.rect.height / 72 * 25.4]
    if len(pdf) != 1 or any(abs(a - b) > 0.02 for a, b in zip(pdf_mm, (STYLE.width_mm, STYLE.height_mm))):
        errors.append("PDF dimensions/pages")
    if page.get_images():
        errors.append("PDF contains raster images")
    fonts = page.get_fonts(full=True)
    if not fonts or any(not pdf.extract_font(f[0])[3] for f in fonts):
        errors.append("PDF font not embedded")
    extracted = "".join(page.get_text().split())
    for term in ("基因组", "一条染色体", "DNA上的一个区域", "HBB", "非真实比例"):
        if term not in extracted:
            errors.append(f"PDF missing text: {term}")
    xml = ET.parse(paths["svg"])
    root = xml.getroot()
    ns = {"s": "http://www.w3.org/2000/svg"}
    svg_texts = root.findall(".//s:text", ns)
    if len(svg_texts) != expected_text_count or root.findall(".//s:image", ns):
        errors.append("SVG text count/raster images")
    svg_mm = [float(root.attrib[k].removesuffix("pt")) / 72 * 25.4 for k in ("width", "height")]
    if any(abs(a - b) > 0.02 for a, b in zip(svg_mm, (STYLE.width_mm, STYLE.height_mm))):
        errors.append("SVG dimensions")
    if "data:font/woff;base64," not in Path(paths["svg"]).read_text():
        errors.append("SVG subset font absent")
    result = {"passed": not errors, "errors": errors, "png_pixels": list(png.size), "png_dpi": dpi,
              "pdf_mm": pdf_mm, "pdf_pages": len(pdf), "pdf_raster_images": len(page.get_images()),
              "pdf_fonts": [{"name": f[3], "type": f[2], "embedded": bool(pdf.extract_font(f[0])[3])} for f in fonts],
              "pdf_vector_paths": len(page.get_drawings()), "svg_mm": svg_mm, "svg_text_count": len(svg_texts),
              "svg_font": "Embedded WOFF subset with text retained; full TTF supplied for editors."}
    pdf.close()
    if errors:
        raise ValueError("Export preflight failed: " + "; ".join(errors))
    return result


def export_figure(result, layout_report, root, working_pdf):
    root = Path(root)
    paths = {fmt: root / "outputs" / fmt / f"{STEM}.{fmt}" for fmt in ("png", "pdf", "svg")}
    for p in paths.values():
        p.parent.mkdir(parents=True, exist_ok=True)
    result.figure.savefig(paths["png"], dpi=STYLE.dpi)
    shutil.copyfile(working_pdf, paths["pdf"])
    result.figure.savefig(paths["svg"], metadata={"Date": None})
    full_text = "\n".join(a.get_text() for a in result.artists.values() if isinstance(a, Text))
    embed_svg_font(paths["svg"], full_text)
    exported = check_exports(paths, layout_report["text_count"])
    # macOS may create AppleDouble ._*.py sidecars on removable volumes.
    # They are filesystem metadata, never reproducible source dependencies.
    sources = [*sorted(p for p in root.glob("*.py") if not p.name.startswith(".")),
               root / "figures" / f"{STEM}.py", FONT_PATH]
    source_hashes = {str(p.relative_to(root)): sha256(p) for p in sources}
    manifest = {
        "figure": result.spec, "size_mm": [STYLE.width_mm, STYLE.height_mm],
        "font": {"family": font_properties().get_name(), "path": str(FONT_PATH.relative_to(root)), "sha256": sha256(FONT_PATH)},
        "environment": {"python": platform.python_version(), "matplotlib": matplotlib.__version__, "numpy": numpy.__version__},
        "source_hashes": source_hashes,
        "outputs": {fmt: {"path": str(p.relative_to(root)), "sha256": sha256(p)} for fmt, p in paths.items()},
        "adjacent_pdf_sha256": sha256(working_pdf),
        "layout": layout_report, "exports": exported,
        "artists": {k: {"type": type(a).__name__, "role": a._running_life_role} for k, a in result.artists.items()},
        "not_verified": ["Real novice reader five-second test", "Physical print proof", "Tavotto application round-trip"],
    }
    target = root / "outputs" / "manifests" / "F01_validation.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(json.dumps({"figure": "F01", "layout_passed": True, "exports_passed": True,
                      "size_mm": manifest["size_mm"], "outputs": [str(p) for p in paths.values()]}, ensure_ascii=False))
    return manifest
