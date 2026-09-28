"""F17: 蛋白质数量与功能状态. State changes are separate comparisons."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
from shared_shapes import Drawing


def protein(c,name,xy,r=3.6):
    c.circle(name,xy,r,color='primary',weight=.18)


def build_figure():
    c=Drawing('F17',height=126)
    c.heading('common.heading','蛋白质总量相同，状态可以不同',(6,117))
    for i,(x,title) in enumerate(((6,'磷酸化'),(60,'位置'),(114,'结合伙伴'))):
        c.rect(f'panel.{i}',(x,26),48,80,color='secondary',weight=.04)
        c.text(f'panel.{i}.heading',title,(x+24,102),size=10)
        c.text(f'panel.{i}.a','A',(x+6,90),size=8.5,color='muted')
        c.text(f'panel.{i}.b','B',(x+6,57),size=8.5,color='muted')
    protein(c,'phosphorylation.a',(30,83))
    protein(c,'phosphorylation.b',(30,49))
    c.line('phosphorylation.bond',[(32.76,51.30),(33.70,52.08)],color='accent',width=.8)
    c.circle('phosphorylation.marker',(36,54),3,color='accent')
    c.text('phosphorylation.marker.label','P',(36,54),size=8.5,color='accent')
    c.text('phosphorylation.a.label','未加该磷酸基',(30,71),size=8.5)
    c.text('phosphorylation.b.label','加上该磷酸基',(30,35),size=8.5)
    for key,y in (('a',83),('b',49)):
        c.ellipse('location.'+key+'.cell',(85,y),26,23,color='secondary')
        c.ellipse('location.'+key+'.nucleus',(90,y),10,13,color='primary',weight=.07)
    protein(c,'location.a.protein',(77,83),2.5)
    protein(c,'location.b.protein',(90,49),2.5)
    c.text('location.a.label','位于细胞质',(84,68),size=8.5)
    c.text('location.b.label','位于细胞核',(84,34),size=8.5)
    protein(c,'binding.a.protein',(131,83))
    c.circle('binding.a.partner',(152,83),3,color='supplement')
    protein(c,'binding.b.protein',(136,49))
    c.circle('binding.b.partner',(142.5,49),3,color='supplement')
    c.text('binding.a.label','尚未结合',(138,71),size=8.5)
    c.text('binding.b.label','与伙伴结合',(138,35),size=8.5)
    c.text('result','功能可能改变',(85,18),size=9.5,color='accent')
    c.note('三组是独立比较；图符不是实测数量，磷酸化也不普遍等于激活。')
    return c.result()


def main():
    from production_utils import export_figure
    result=build_figure();fig=result.figure;OUT=Path(__file__).resolve().parent
    fig.savefig(OUT/'F17_protein_states.pdf',metadata={'CreationDate':None,'ModDate':None})
    return export_figure(result,ROOT,OUT/'F17_protein_states.pdf')


if __name__=='__main__':
    main()
