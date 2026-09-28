from pathlib import Path
from html.parser import HTMLParser
import argparse,hashlib,json,re,xml.etree.ElementTree as ET,zipfile
import pymupdf
p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('out',type=Path);a=p.parse_args()
class Catalog(HTMLParser):
 def __init__(self):super().__init__();self.articles={};self.cur=None;self.tag=None;self.links=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='article':self.cur=d['id'];self.articles[self.cur]={'title':'','code':''}
  if tag in ['h2','code']:self.tag=tag
  if 'href' in d:self.links.append(d['href'])
  if 'src' in d:self.links.append(d['src'])
 def handle_endtag(self,tag):
  if tag=='article':self.cur=None
  if tag in ['h2','code']:self.tag=None
 def handle_data(self,data):
  if self.cur and self.tag:self.articles[self.cur]['title' if self.tag=='h2' else 'code']+=data
h=Catalog();h.feed((a.root/'FIGURE_INDEX.html').read_text())
original=Path('/Users/lester9113/Downloads/运行生命.docx');original_sha=hashlib.sha256(original.read_bytes()).hexdigest()
with zipfile.ZipFile(original) as z:xml=ET.fromstring(z.read('word/document.xml'))
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
paras=[''.join(t.text or '' for t in x.findall('.//w:t',ns)) for x in xml.findall('.//w:body/w:p',ns)]
titles={m.group(1):s for s in paras if (m:=re.match(r'图 (F\d{2})｜',s))}
errors=[]
def check(ok,name,detail=None):
 if not ok:errors.append({'check':name,'detail':detail})
check(original_sha=='2feab6034a2d85dbc78c8045dbb5e29c1a909889eb6a70e17b937fcd9140704d','original_manuscript_unchanged')
check(list(h.articles)==[f'F{i:02d}' for i in range(1,31)],'catalog_has_30_in_order')
md=(a.root/'FIGURE_INDEX.md').read_text();trace=(a.root/'SOURCE_TRACEABILITY.md').read_text();volume=pymupdf.open(a.root/'Running_Life_F01-F30.pdf');toc=volume.get_toc()
check(len(volume)==30,'volume_has_30_pages');check(toc==[[1,titles[f'F{i:02d}'],i] for i in range(1,31)],'original_titles_in_pdf_bookmarks')
for i in range(1,31):
 fid=f'F{i:02d}';spec=json.loads((a.root/'figure_specs'/f'{fid}.json').read_text());source=next(a.root.glob('figures/'+fid+'_*.py'));single=pymupdf.open(a.root/'outputs/pdf'/(source.stem+'.pdf'))
 check('图 '+fid+'｜'+spec['title']==titles[fid],'spec_original_title',fid)
 check(h.articles[fid]['title']==titles[fid],'html_original_title',fid)
 check(h.articles[fid]['code']==source.read_text(),'html_full_source_exact',fid)
 check(titles[fid] in md and titles[fid] in trace,'markdown_source_titles',fid)
 for key in ['cognitive_task','layout_rationale','components','source_paragraphs']:check(bool(spec.get(key)),'spec_required_metadata',[fid,key])
 check(all(spec[k] in md for k in ['cognitive_task','layout_rationale','components']),'metadata_in_index',fid)
 page=volume[i-1];check(not page.get_images(),'volume_vector_only',fid);check(''.join(page.get_text().split())==''.join(single[0].get_text().split()),'merged_pdf_page_text',fid)
 check(abs(page.rect.width-single[0].rect.width)<.01 and abs(page.rect.height-single[0].rect.height)<.01,'merged_pdf_page_size',fid);single.close()
for link in h.links:
 if link.startswith('#'):check(link[1:] in h.articles,'catalog_anchor',link)
 elif '://' not in link:check((a.root/link).exists(),'catalog_relative_link_exists',link)
volume.close();result={'passed':not errors,'errors':errors,'original_sha256':original_sha,'figure_titles':titles,'html_articles':len(h.articles),'html_links_checked':len(h.links),'pdf_pages':30,'scope':'Read-only catalog, source fidelity, links, merged vector PDF and bookmark inspection.'};a.out.write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False))
