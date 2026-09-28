"""Deterministic multi-figure exports, measured layout and vector/font checks."""
from pathlib import Path
import hashlib
import json
import platform
import shutil
import xml.etree.ElementTree as ET
import matplotlib as mpl
from matplotlib.text import Text
import pymupdf
from PIL import Image
from book_style import STYLE, FONT_PATH, rc_settings
from layout_utils import check_layout
from export_utils import embed_svg_font


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def export_figure(result, root, working_pdf):
    root, working_pdf = Path(root), Path(working_pdf)
    fid=result.spec["id"]
    layout=check_layout(result)
    if not layout["passed"]:
        raise ValueError(fid+" layout failed: "+json.dumps(layout["errors"],ensure_ascii=False))
    paths={fmt:root/"outputs"/fmt/(working_pdf.stem+"."+fmt) for fmt in ("png","pdf","svg")}
    for path in paths.values():path.parent.mkdir(parents=True,exist_ok=True)
    with mpl.rc_context(rc_settings()):
        # Re-save the explicit adjacent target under the common font contract.
        result.figure.savefig(working_pdf,metadata={"CreationDate":None,"ModDate":None})
        shutil.copyfile(working_pdf,paths["pdf"])
        result.figure.savefig(paths["png"],dpi=STYLE.dpi)
        result.figure.savefig(paths["svg"],metadata={"Date":None})
    texts=[a.get_text() for a in result.artists.values() if isinstance(a,Text)]
    embed_svg_font(paths["svg"],"\n".join(texts))
    size=[float(v*25.4) for v in result.figure.get_size_inches()]
    im=Image.open(paths["png"])
    assert all(abs(a-b/25.4*STYLE.dpi)<=1 for a,b in zip(im.size,size))
    assert min(im.info["dpi"])>=599
    pdf=pymupdf.open(paths["pdf"]);page=pdf[0]
    assert len(pdf)==1 and not page.get_images()
    assert all(abs(a-b)<.02 for a,b in zip((page.rect.width/72*25.4,page.rect.height/72*25.4),size))
    fonts=page.get_fonts(full=True)
    assert fonts and all(pdf.extract_font(f[0])[3] for f in fonts)
    extracted="".join(page.get_text().split())
    assert all("".join(t.split()) in extracted for t in texts), [t for t in texts if "".join(t.split()) not in extracted]
    tree=ET.parse(paths["svg"]);ns={"s":"http://www.w3.org/2000/svg"}
    svg_texts=tree.findall(".//s:text",ns)
    assert len(svg_texts)==sum(len(t.splitlines()) for t in texts)
    assert not tree.findall(".//s:image",ns)
    sources=[*sorted(p for p in root.glob("*.py") if not p.name.startswith('.')),
             working_pdf.with_suffix('.py'),root/'figure_specs'/f'{fid}.json',FONT_PATH]
    report={"version":"book-figures-v1.0","figure":result.spec,"size_mm":size,
            "environment":{"python":platform.python_version(),"matplotlib":mpl.__version__},
            "layout":layout,"exports":{"passed":True,"png_pixels":im.size,"png_dpi":im.info["dpi"],
                "pdf_raster_images":0,"pdf_vector_paths":len(page.get_drawings()),"svg_text_count":len(svg_texts),"fonts_embedded":True},
            "artists":{k:{"type":type(a).__name__,"role":a._running_life_role} for k,a in result.artists.items()},
            "source_hashes":{str(p.relative_to(root)):sha(p) for p in sources},
            "outputs":{fmt:{"path":str(p.relative_to(root)),"sha256":sha(p)} for fmt,p in paths.items()},
            "adjacent_pdf_sha256":sha(working_pdf),
            "not_verified":["Physical print/CMYK proof","Real reader study","Tavotto application round-trip"]}
    dest=root/'outputs/manifests'/f'{fid}_validation.json';dest.parent.mkdir(exist_ok=True,parents=True)
    dest.write_text(json.dumps(report,ensure_ascii=False,indent=2))
    pdf.close()
    print(json.dumps({"id":fid,"passed":True,"artists":len(result.artists),"size_mm":size},ensure_ascii=False))
    return report
