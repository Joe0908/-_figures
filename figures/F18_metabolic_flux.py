"""F18: 相同代谢物浓度与不同代谢流. Equal pools, qualitative turnover."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
from shared_shapes import Drawing


def draw_pool(c,key,x,turnover):
    c.text(key+'.heading',turnover,(x,104),size=11.5)
    c.rect(key+'.pool',(x-13,49),26,26,color='primary',weight=.10)
    for i,(dx,dy) in enumerate(((-6,-4),(0,-4),(6,-4),(-6,4),(0,4),(6,4))):
        c.circle(key+f'.metabolite.{i}',(x+dx,62+dy),1.3,color='primary')
    c.text(key+'.production.label','制造',(x,94),size=9)
    c.text(key+'.input.label','输入',(x-32,62),size=9)
    c.text(key+'.output.label','输出',(x+32,62),size=9)
    c.text(key+'.consumption.label','消耗',(x,31),size=9)
    c.edge(key+'.production',(x,88),(x,77),kind='process')
    c.edge(key+'.input',(x-23,62),(x-15,62),kind='process')
    c.edge(key+'.output',(x+15,62),(x+23,62),kind='process')
    c.edge(key+'.consumption',(x,47),(x,37),kind='process')


def build_figure():
    c=Drawing('F18',height=116)
    draw_pool(c,'slower',44,'较慢周转')
    draw_pool(c,'faster',124,'较快周转')
    c.text('equal_state','同一时点：相同体积、相同浓度',(85,19),size=9.5)
    c.note('概念示意：箭头等宽，快慢由标签表示；没有浓度或流速的实测数值。')
    return c.result()


def main():
    from production_utils import export_figure
    result=build_figure();fig=result.figure;OUT=Path(__file__).resolve().parent
    fig.savefig(OUT/'F18_metabolic_flux.pdf',metadata={'CreationDate':None,'ModDate':None})
    return export_figure(result,ROOT,OUT/'F18_metabolic_flux.pdf')


if __name__=='__main__':
    main()
