"""Freeze binding, one clean sequential rebuild, and independent read-only export probes."""
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,sys,time
p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('audit',type=Path);a=p.parse_args();a.root=a.root.resolve();a.audit=a.audit.resolve()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inventory(root):return {str(p.relative_to(root)):sha(p) for p in sorted(root.rglob('*')) if p.is_file() and not any(q.startswith('._') or q=='__pycache__' for q in p.relative_to(root).parts)}
before=inventory(a.root);(a.audit/'frozen_inventory.json').write_text(json.dumps(before,ensure_ascii=False,indent=2))
clone=a.audit/'clean_rebuild'
if clone.exists():raise SystemExit('Refusing to overwrite existing clean rebuild; choose a new audit run directory.')
shutil.copytree(a.root,clone,ignore=shutil.ignore_patterns('._*','__pycache__','outputs'))
for f in (clone/'figures').glob('*.pdf'):
 if not f.name.startswith('._'):f.unlink()
figures=sorted((clone/'figures').glob('F[0-9][0-9]_*.py'))
assert len(figures)==30 and [f.name[:3] for f in figures]==[f'F{x:02d}' for x in range(1,31)]
env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';env['MPLCONFIGDIR']=str(a.audit/'mpl_cache');env['MPLBACKEND']='Agg'
steps=[];errors=[]
for f in figures:
 fid=f.name[:3];start=time.monotonic();r=subprocess.run([sys.executable,str(f)],cwd=clone,env=env,text=True,capture_output=True)
 (a.audit/(fid+'_rebuild.log')).write_text(r.stdout+'\n'+r.stderr)
 step={'id':fid,'returncode':r.returncode,'seconds':round(time.monotonic()-start,3)};steps.append(step)
 if r.returncode:errors.append({'check':'clean_rebuild_exit','id':fid,'detail':r.stderr[-2000:]})
 print(json.dumps(step),flush=True)
 if r.returncode:break
matches=[]
if not errors:
 for f in figures:
  fid=f.name[:3]
  for fmt in ['png','pdf','svg']:
   rel=Path('outputs')/fmt/(f.stem+'.'+fmt);orig=a.root/rel;rebuilt=clone/rel
   rec={'id':fid,'format':fmt,'candidate':sha(orig),'rebuilt':sha(rebuilt),'equal':sha(orig)==sha(rebuilt)};matches.append(rec)
   if not rec['equal']:errors.append({'check':'byte_identical_rebuild','detail':rec})
  target=a.audit/'probes'/f'{fid}.json';target.parent.mkdir(exist_ok=True)
  r=subprocess.run([sys.executable,str(Path(__file__).parent/'probe_figure.py'),str(a.root),fid,str(target)],env=env,text=True,capture_output=True)
  (a.audit/(fid+'_probe.log')).write_text(r.stdout+'\n'+r.stderr)
  if r.returncode or not target.exists():errors.append({'check':'probe_execution','id':fid,'detail':r.stderr[-2000:]})
  elif not json.loads(target.read_text())['passed']:errors.append({'check':'independent_probe','id':fid,'detail':json.loads(target.read_text())['errors']})
  print(json.dumps({'probe':fid,'returncode':r.returncode}),flush=True)
after=inventory(a.root)
changed={k:{'before':before.get(k),'after':after.get(k)} for k in set(before)|set(after) if before.get(k)!=after.get(k)}
if changed:errors.append({'check':'candidate_changed_during_audit','detail':changed})
record={'passed':not errors,'candidate_root':str(a.root),'inventory_sha256':sha(a.audit/'frozen_inventory.json'),'sequential_rebuild':steps,'output_comparisons':matches,'candidate_changed':changed,'errors':errors,'scope':'Automated checks only. Final visual, scientific and documentation audit reported separately.'}
(a.audit/'full_check.json').write_text(json.dumps(record,ensure_ascii=False,indent=2));print(json.dumps({'passed':not errors,'errors':errors},ensure_ascii=False),flush=True)
