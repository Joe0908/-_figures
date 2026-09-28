"""F16: 同一 DNA 可以产生不同 RNA 图景. Four independent contrasts."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
from shared_shapes import Drawing


def rna_tokens(c,name,x,y,count):
    for i in range(count):
        c.strand(name+f'.{i}',x,y+(i-(count-1)/2)*3.2,29)


def build_figure():
    c=Drawing('F16',height=126)
    c.heading('shared.heading','相同 DNA 背景',(6,117))
    c.dna('shared.dna',83,114,71,gap=4)
    c.text('condition.a','条件 A',(68,102),size=11.5)
    c.text('condition.b','条件 B',(132,102),size=11.5)
    c.rect('condition.a.boundary',(40,15),57,80,color='secondary',weight=.04)
    c.rect('condition.b.boundary',(103,15),59,80,color='secondary',weight=.04)
    rows=[(84,'检出情况'),(64,'RNA 数量'),(43,'剪接版本'),(24,'不变参照')]
    for i,(y,value) in enumerate(rows):
        c.text(f'row.{i}.label',value,(22,y),size=9)
    for i,y in enumerate((74,54,34)):
        c.line(f'row.divider.{i}',[(8,y),(162,y)],color='muted',width=.8,dashed=True)
    c.text('detection.a','很少／未检出',(68,84),size=9)
    rna_tokens(c,'detection.b',117,84,3)
    rna_tokens(c,'abundance.a',54,64,1)
    rna_tokens(c,'abundance.b',117,64,3)
    c.segments('splice.a',[1,2,4],48,40,segment_w=11,h=6,gap=1.8)
    c.segments('splice.b',[1,3,4],111,40,segment_w=11,h=6,gap=1.8)
    rna_tokens(c,'stable.a',54,24,2)
    rna_tokens(c,'stable.b',117,24,2)
    c.note('示意：图符仅表示定性差别；RNA 存量与版本不等于即时转录速率。')
    return c.result()


def main():
    from production_utils import export_figure
    result=build_figure();fig=result.figure;OUT=Path(__file__).resolve().parent
    fig.savefig(OUT/'F16_rna_landscapes.pdf',metadata={'CreationDate':None,'ModDate':None})
    return export_figure(result,ROOT,OUT/'F16_rna_landscapes.pdf')


if __name__=='__main__':
    main()
