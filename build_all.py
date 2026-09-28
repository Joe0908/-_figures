"""Rebuild selected figures in numeric order; defaults to all thirty."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--start',type=int,default=1)
    parser.add_argument('--end',type=int,default=30)
    args=parser.parse_args()
    if not 1 <= args.start <= args.end <= 30:
        parser.error('Expected 1 <= start <= end <= 30')
    records=[]
    for number in range(args.start,args.end+1):
        fid=f'F{number:02d}'
        paths=sorted(ROOT.joinpath('figures').glob(fid+'_*.py'))
        if len(paths)!=1:raise RuntimeError(f'{fid}: expected one source, got {paths}')
        path=paths[0];start=time.time()
        subprocess.run([sys.executable,str(path)],cwd=ROOT,check=True)
        records.append({'id':fid,'source':str(path.relative_to(ROOT)),
                        'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                        'started_unix':start,'ended_unix':time.time()})
    output=ROOT/'outputs'/'manifests'/f'build_order_{args.start:02d}_{args.end:02d}.json'
    output.write_text(json.dumps(records,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
