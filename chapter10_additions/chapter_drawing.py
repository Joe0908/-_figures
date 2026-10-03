"""Chapter 10 adapter, using the repository palette, font and geometry checks.

Coordinates are millimetres on a 170 mm master. Labels stay readable when
the image is inserted at the supplied book's 108 mm text-column width.
"""
from pathlib import Path
from dataclasses import replace
import sys, json, platform
ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from book_style import STYLE, FONT_PATH, rc_settings
from palette import PRIMARY, SECONDARY, ACCENT, SUPPLEMENT, INK, MUTED, tint
from shared_shapes import Drawing
from layout_utils import new_canvas, check_layout
from production_utils import sha
from export_utils import embed_svg_font
from matplotlib.text import Text
import matplotlib as mpl
import pymupdf
from PIL import Image
import xml.etree.ElementTree as ET
import numpy as np

LABEL, NOTE, HEADING = 14.5, 13.5, 17

class ChapterDrawing(Drawing):
    def __init__(self, fid, height, title, task):
        self.id = fid
        self.style = replace(STYLE, height_mm=height)
        with mpl.rc_context(rc_settings()):
            self.figure, self.ax = new_canvas(self.style)
        self.artists = {}
        self.spec = dict(id=fid, title=title, cognitive_task=task,
                         size_mm=[170, height], palette='海青与铜',
                         relations_drawn=[],
                         source_document='运行生命_第五部分_段落版(1).docx')

    def text(self, name, value, xy, *, size=LABEL, **kwargs):
        return super().text(name, value, xy, size=size, **kwargs)

    def heading(self, name, value, xy, *, ha='left'):
        return self.text(name, value, xy, size=HEADING, ha=ha)

    def note(self, value, *, y=8, name='scope.note'):
        return self.text(name, value, (6, y), size=NOTE, color=MUTED, ha='left')


def export(result, script):
    """Run the repository layout check and native vector/font export contract."""
    script=Path(script);stem=script.stem
    layout=check_layout(result)
    if not layout['passed']:
        raise ValueError(json.dumps(layout['errors'],ensure_ascii=False,indent=2))
    paths={fmt:HERE/'outputs'/fmt/(stem+'.'+fmt) for fmt in ('png','pdf','svg')}
    for p in paths.values():p.parent.mkdir(parents=True,exist_ok=True)
    with mpl.rc_context(rc_settings()):
        result.figure.savefig(paths['png'],dpi=STYLE.dpi)
        result.figure.savefig(paths['pdf'],metadata={'CreationDate':None,'ModDate':None})
        result.figure.savefig(paths['svg'],metadata={'Date':None})
    texts=[a.get_text() for a in result.artists.values() if isinstance(a,Text)]
    embed_svg_font(paths['svg'],'\n'.join(texts))
    im=Image.open(paths['png']);size=result.spec['size_mm']
    assert all(abs(a-b/25.4*STYLE.dpi)<=1 for a,b in zip(im.size,size))
    assert min(im.info['dpi'])>=599
    pdf=pymupdf.open(paths['pdf']);page=pdf[0]
    assert len(pdf)==1 and not page.get_images()
    assert all(abs(a-b)<.02 for a,b in zip((page.rect.width/72*25.4,page.rect.height/72*25.4),size))
    assert all(pdf.extract_font(f[0])[3] for f in page.get_fonts(full=True))
    extracted=''.join(page.get_text().split())
    assert all(''.join(t.split()) in extracted for t in texts)
    svg=ET.parse(paths['svg']);ns={'s':'http://www.w3.org/2000/svg'}
    assert len(svg.findall('.//s:text',ns))==sum(len(t.splitlines()) for t in texts)
    assert not svg.findall('.//s:image',ns)
    dependencies=[script,HERE/'chapter_drawing.py',ROOT/'book_style.py',ROOT/'palette.py',
                  ROOT/'shared_shapes.py',ROOT/'layout_utils.py',ROOT/'production_utils.py',ROOT/'export_utils.py',FONT_PATH]
    report=dict(figure=result.spec,layout=layout,environment=dict(python=platform.python_version(),matplotlib=mpl.__version__),
                exports=dict(passed=True,png_dpi=im.info['dpi'],png_pixels=im.size,pdf_raster_images=0,
                             pdf_vector_paths=len(page.get_drawings()),fonts_embedded=True,svg_text_count=len(svg.findall('.//s:text',ns))),
                source_hashes={str(p.relative_to(ROOT)):sha(p) for p in dependencies},
                outputs={fmt:dict(path=str(p.relative_to(HERE)),sha256=sha(p)) for fmt,p in paths.items()},
                minimum_master_text_pt=min(a.get_fontsize() for a in result.artists.values() if isinstance(a,Text)),
                word_width_mm=108,minimum_word_text_pt=NOTE*108/170,
                not_verified=['Physical print/CMYK','Real novice reader study','All vector editor round trips'])
    dest=HERE/'outputs'/'manifests'/(result.spec['id']+'_validation.json')
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(report,ensure_ascii=False,indent=2))
    pdf.close()
    print(json.dumps(dict(id=result.spec['id'],passed=True,size_mm=size),ensure_ascii=False))
    return report
