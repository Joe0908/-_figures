"""Check this revision without rebuilding or touching root F01–F30."""
from pathlib import Path
import sys, importlib, json
from build_chapter4 import FILES
from chapter_drawing import HERE, check_layout, sha

def validate():
    records=[]
    for name in FILES:
        r=importlib.import_module(Path(name).stem).build_figure()
        layout=check_layout(r)
        assert layout['passed'],layout['errors']
        manifest=HERE/'outputs'/'manifests'/(r.spec['id']+'_validation.json')
        m=json.loads(manifest.read_text())
        for obj in m['outputs'].values():assert sha(HERE/obj['path'])==obj['sha256']
        for name,value in m['source_hashes'].items():assert sha(HERE.parent/name)==value,name
        assert m['exports']['passed']
        records.append(dict(id=r.spec['id'],layout_passed=True,output_hashes_match=True,source_hashes_match=True,
                            size_mm=r.spec['size_mm'],word_minimum_text_pt=m['minimum_word_text_pt']))
    report=dict(passed=True,scope='chapter4_revision only',figures=records,
                boundary='Geometry, font/vector export and byte binding; not a real-reader comprehension study.')
    p=HERE/'outputs'/'manifests'/'chapter4_validation.json';p.write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps(report,ensure_ascii=False))
    return report

if __name__=='__main__':validate()
