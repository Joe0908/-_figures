from pathlib import Path
import argparse,collections,hashlib,json,platform,sys
p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('run',type=Path);a=p.parse_args();a.root=a.root.resolve()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
errors=[]
def check(ok,name,detail=None):
 if not ok:errors.append({'check':name,'detail':detail})
manifest=a.root/'RELEASE_MANIFEST.json';m=json.loads(manifest.read_text());mhash=sha(manifest)
check(mhash=='24af06384cf6394d5b45aefda4e4f58f5c3ce4f3fc0bab1f411a47248dfdb7fd','announced_frozen_manifest_hash')
actual={str(p.relative_to(a.root)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in a.root.rglob('*') if p.is_file() and p!=manifest and 'audit' not in p.relative_to(a.root).parts and not any(q.startswith('.') or q=='__pycache__' for q in p.relative_to(a.root).parts)}
check(set(actual)==set(m['files']),'manifest_exact_core_coverage',{'missing':sorted(set(actual)-set(m['files'])),'extra':sorted(set(m['files'])-set(actual))})
for rel,item in m['files'].items():check(actual.get(rel)==item,'manifest_file_hash_and_size',rel)
input_checks={}
for name,expected in m['input_sha256'].items():
 path=Path('/Users/lester9113/Downloads')/name;input_checks[name]={'expected':expected,'actual':sha(path),'unchanged':sha(path)==expected};check(input_checks[name]['unchanged'],'input_original_unchanged',name)
f01_expected={'png':'9d34a7d5d9b798ba9b60b44af4621fb070a7f1487149aa5a00980ac1cb9c164c','pdf':'2edc68da71aa9b4a849c67ca4b132b77ed3c6b1f8820721af85805382d73e05a','svg':'46d5b4a6c29fc3594f29bd8957f2bc1ea3528e8270df5a53f511e0408da3971b'}
for fmt,expected in f01_expected.items():check(sha(next((a.root/'outputs'/fmt).glob('F01_*.'+fmt)))==expected,'f01_approved_output_preserved',fmt)
check(sha(a.root/'fonts/NotoSansSC-Regular.ttf')=='c9c55065eafd571f28dbfe688e00067fbb441a3acabdceeb543b8a0077364a10','approved_font_preserved')
figures=sorted((a.root/'figures').glob('F[0-9][0-9]_*.py'));check(len(figures)==30,'thirty_scripts')
for fmt in ['png','pdf','svg']:check(len(list((a.root/'outputs'/fmt).glob('F[0-9][0-9]_*.'+fmt)))==30,'thirty_exports',fmt)
adjacent=[]
for f in figures:
 pdf=f.with_suffix('.pdf');export=a.root/'outputs/pdf'/pdf.name;equal=sha(pdf)==sha(export);adjacent.append({'id':f.name[:3],'hash':sha(pdf),'same_as_output':equal});check(equal,'adjacent_pdf_identical',f.name[:3])
order=json.loads((a.root/'outputs/manifests/build_order_01_30.json').read_text())
check([r['id'] for r in order]==[f'F{i:02d}' for i in range(1,31)],'production_order_01_to_30')
for i,r in enumerate(order):
 check(sha(a.root/r['source'])==r['sha256'],'production_log_source_hash',r['id']);check(r['ended_unix']>=r['started_unix'],'production_positive_duration',r['id'])
 if i:check(r['started_unix']>=order[i-1]['ended_unix'],'production_nonoverlapping_sequential',r['id'])
probes=[json.loads((a.run/'probes'/f'F{i:02d}.json').read_text()) for i in range(1,31)]
changes=[]
for folder in ['previews_02_10_v1','previews_11_20_v1','previews_21_30_v1']:
 for old in json.loads((a.run.parent/folder/'preview_manifest.json').read_text()):
  new=probes[int(old['id'][1:])-1]
  if new['source_sha256']!=old['source_sha256']:changes.append({'id':old['id'],'preliminary_source_sha256':old['source_sha256'],'final_source_sha256':new['source_sha256']})
result={'passed':not errors,'errors':errors,'version':m['version'],'manifest_sha256':mhash,'core_file_count':len(actual),'inputs':input_checks,'f01_approved_hashes':f01_expected,'adjacent_pdf_checks':adjacent,'production_order_checked':True,'source_changes_since_preliminary_visual':changes,'statistics':{'figure_count':len(probes),'artists':sum(r['artist_count'] for r in probes),'texts':sum(len(r['texts']) for r in probes),'minimum_font_pt':min(t['size_pt'] for r in probes for t in r['texts']),'height_counts_mm':dict(collections.Counter(round(r['size_mm'][1]) for r in probes)),'pdf_raster_images':sum(r['exports']['pdf']['images'] for r in probes),'svg_raster_images':sum(r['exports']['svg']['images'] for r in probes)},'scope':'Read-only final core manifest, original inputs, approved F01, adjacency, source versions and build-order checks.'}
(a.run/'release_binding_check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2))
