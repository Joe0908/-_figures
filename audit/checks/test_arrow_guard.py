from pathlib import Path
import argparse,hashlib,json,sys
p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('out',type=Path);a=p.parse_args();sys.path.insert(0,str(a.root))
from layout_utils import new_canvas,register,BuildResult,check_layout
from book_style import font_properties
from matplotlib.patches import FancyArrowPatch
from matplotlib.text import Text

def case(name,xy,start,end):
 fig,ax=new_canvas();artists={}
 t=ax.text(*xy,'核验文本',ha='center',va='center',fontproperties=font_properties(8.5));register(artists,name+'.text',t,'text')
 edge=FancyArrowPatch(start,end,arrowstyle='-|>',mutation_scale=8.5,shrinkA=0,shrinkB=0,linewidth=1.1);ax.add_patch(edge);register(artists,name+'.edge',edge,'process')
 result=BuildResult(fig,ax,artists,{});fig.canvas.draw();renderer=fig.canvas.get_renderer();raw_path=edge.get_path().transformed(edge.get_transform());raw_hit=raw_path.intersects_bbox(t.get_window_extent(renderer).padded(.35*fig.dpi/25.4+edge.get_linewidth()*fig.dpi/72/2),filled=False)
 report=check_layout(result)
 return {'name':name,'raw_path_crosses_text':raw_hit,'passed':report['passed'],'errors':report['errors']}
records=[case('real_crossing',(80,70),(60,70),(100,70)),case('clear_arrow',(40,40),(80,70),(100,70)),case('dummy_origin',(20,14),(80,70),(100,70))]
checks={'true_crossing_rejected':not records[0]['passed'] and any(x['kind']=='stroke_crosses_text' for x in records[0]['errors']),'ordinary_arrow_accepted':records[1]['passed'],'dummy_regression_exercised':records[2]['raw_path_crosses_text'],'dummy_origin_false_crossing_removed':records[2]['passed']}
report={'source_sha256':hashlib.sha256((a.root/'layout_utils.py').read_bytes()).hexdigest(),'tests':records,'checks':checks,'passed':all(checks.values())}
a.out.write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
