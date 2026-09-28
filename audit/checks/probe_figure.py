"""Independent read-only native object and export inspection. Writes only JSON audit report."""
from pathlib import Path
import argparse,base64,hashlib,importlib.util,io,json,math,re,sys,xml.etree.ElementTree as ET
p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('fid');p.add_argument('out',type=Path);a=p.parse_args()
sys.path.insert(0,str(a.root))
import matplotlib as mpl
from matplotlib.text import Text
from matplotlib.colors import to_rgb
from PIL import Image
import pymupdf
from fontTools.ttLib import TTFont
from book_style import FONT_PATH,missing_glyphs

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
errors=[];observations=[]
def check(ok,name,detail=None):
 if not ok: errors.append({'check':name,'detail':detail})
source=next(a.root.glob('figures/'+a.fid+'_*.py'));before=sha(source)
spec=importlib.util.spec_from_file_location(a.fid,source);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
r=module.build_figure();fig=r.figure;fig.canvas.draw();renderer=fig.canvas.get_renderer();width,height=[float(x*25.4) for x in fig.get_size_inches()]
check(abs(width-170)<.001 and any(abs(height-h)<.001 for h in [100,116,126,140]),'physical_size',[width,height])
texts=[];ids=[]
for key,obj in r.artists.items():
 ids.append(obj.get_gid());check(obj.get_gid()==key,'gid_matches_registry',key)
 box=obj.get_window_extent(renderer); vals=[float(x) for x in box.extents]
 check(all(math.isfinite(x) for x in vals),'finite_extents',key)
 check(box.x0>=-.01 and box.y0>=-.01 and box.x1<=fig.bbox.width+.01 and box.y1<=fig.bbox.height+.01,'artist_inside_canvas',key)
 if isinstance(obj,Text):
  text=obj.get_text();texts.append({'id':key,'text':text,'size_pt':obj.get_fontsize(),'font':obj.get_fontproperties().get_file(),'color':obj.get_color(),'extent_mm':[x/fig.dpi*25.4 for x in vals]})
  check(obj.get_fontsize()>=8.5,'minimum_font',key)
  check(Path(obj.get_fontproperties().get_file()).resolve()==FONT_PATH.resolve(),'bundled_font',key)
  check(not missing_glyphs(text),'glyph_coverage',key)
check(len(ids)==len(set(ids)) and all(ids),'unique_semantic_ids')
registered_text={id(o) for o in r.artists.values() if isinstance(o,Text)}
check(all(id(o) in registered_text for o in r.axes.texts if o.get_visible()),'all_axes_text_registered')
# Independent text-to-text clearance measurement. Does not certify stroke relationships.
for i,x in enumerate(texts):
 for y in texts[i+1:]:
  bx,by=x['extent_mm'],y['extent_mm']
  if bx[0]-.4<by[2]+.4 and bx[2]+.4>by[0]-.4 and bx[1]-.4<by[3]+.4 and bx[3]+.4>by[1]-.4:
   errors.append({'check':'text_clearance_0.8mm','detail':[x['id'],y['id']]})
files={fmt:a.root/'outputs'/fmt/(source.stem+'.'+fmt) for fmt in ['png','pdf','svg']}
check(all(x.is_file() for x in files.values()),'all_three_exports_present')
export={}
if all(x.is_file() for x in files.values()):
 im=Image.open(files['png']);export['png']={'pixels':im.size,'dpi':im.info.get('dpi')}
 check(all(abs(v-mm/25.4*600)<=1 for v,mm in zip(im.size,[width,height])),'png_pixel_dimensions')
 check(im.info.get('dpi') and all(abs(v-600)<.1 for v in im.info['dpi']),'png_dpi')
 pdf=pymupdf.open(files['pdf']);page=pdf[0];pdf_text=''.join(page.get_text().split());fonts=page.get_fonts(full=True)
 export['pdf']={'pages':len(pdf),'size_mm':[page.rect.width*25.4/72,page.rect.height*25.4/72],'images':len(page.get_images()),'vector_paths':len(page.get_drawings()),'fonts':[{'name':f[3],'type':f[2],'embedded':bool(pdf.extract_font(f[0])[3])} for f in fonts]}
 check(len(pdf)==1,'pdf_single_page');check(not page.get_images(),'pdf_no_raster');check(bool(page.get_drawings()),'pdf_has_vectors')
 check(fonts and all(pdf.extract_font(f[0])[3] for f in fonts),'pdf_embedded_fonts')
 check(all(abs(v-mm)<.02 for v,mm in zip(export['pdf']['size_mm'],[width,height])),'pdf_size')
 for t in texts:check(''.join(t['text'].split()) in pdf_text,'pdf_text_complete',t['id'])
 pdf_spans=[s for b in page.get_text('dict')['blocks'] if b['type']==0 for l in b['lines'] for s in l['spans']]
 check(all(s['size']>=8.49 for s in pdf_spans),'pdf_font_minimum')
 pdf.close()
 xml=ET.parse(files['svg']).getroot();ns={'s':'http://www.w3.org/2000/svg'};nodes=xml.findall('.//s:text',ns);svg_ids={e.attrib.get('id') for e in xml.iter()}
 export['svg']={'native_text_count':len(nodes),'images':len(xml.findall('.//s:image',ns)),'semantic_ids':len(set(ids)&svg_ids)}
 check(not xml.findall('.//s:image',ns),'svg_no_raster');check(len(nodes)==sum(len(t['text'].splitlines()) for t in texts),'svg_text_line_count')
 for key in ids:check(key in svg_ids,'svg_semantic_id_present',key)
 svg_texts=[''.join(e.itertext()) for e in nodes]
 for t in texts:
  for line in t['text'].splitlines():check(line in svg_texts,'svg_text_complete',t['id'])
 svg_content=files['svg'].read_text();match=re.search(r'data:font/woff;base64,([A-Za-z0-9+/=]+)',svg_content)
 check(bool(match),'svg_self_contained_woff')
 if match:
  font=TTFont(io.BytesIO(base64.b64decode(match.group(1))));cmap=font.getBestCmap();chars={c for t in texts for c in t['text'] if not c.isspace()};check(all(ord(c) in cmap for c in chars),'svg_woff_glyph_coverage')
  export['svg']['font_subset_glyphs']=len(cmap)
 check(all(abs(float(xml.attrib[k].removesuffix('pt'))/72*25.4-mm)<.02 for k,mm in zip(['width','height'],[width,height])),'svg_size')
check(before==sha(source),'source_unchanged_during_probe')
record={'id':a.fid,'passed':not errors,'errors':errors,'source_sha256':before,'source':str(source),'size_mm':[width,height],'artist_count':len(r.artists),'texts':texts,'relations':r.spec.get('relations_drawn',[]),'spec':r.spec,'exports':export,'output_hashes':{k:sha(v) for k,v in files.items() if v.is_file()},'notes':['Native objects and files inspected independently; does not replace actual visual/scientific audit.']}
a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(record,ensure_ascii=False,indent=2));print(json.dumps({'id':a.fid,'passed':not errors,'errors':errors},ensure_ascii=False))
