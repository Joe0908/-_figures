"""F13: 从细胞行为到组织结构的空间反馈. Space and behavior form a loop."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
from shared_shapes import Drawing


def draw_tissue(c):
    c.heading('tissue.heading','上皮与基质示意',(6,107))
    for i,x in enumerate((10,26,42)):
        c.rect(f'tissue.cell.{i}',(x,72),14,22,color='secondary',weight=.08)
        c.ellipse(f'tissue.nucleus.{i}',(x+7,82),5,7,color='primary')
        c.line(f'tissue.attachment.{i}',[(x+7,68),(x+7,72)],color='secondary',width=1.1)
    for i,x in enumerate((25,41)):
        c.line(f'tissue.contact.{i}',[(x-1,84),(x+1,84)],color='secondary',width=1.5)
    c.rect('tissue.matrix',(8,63),50,5,color='secondary',weight=.18,radius=0)
    c.text('tissue.matrix.label','细胞外基质',(33,55),size=9)
    c.text('tissue.neighbors','邻居接触',(33,99),size=8.5,color='muted')
    c.text('tissue.context','位置、邻居与基质\n也是细胞的输入',(33,35),size=9)


def build_figure():
    c=Drawing('F13',height=116)
    draw_tissue(c)
    c.heading('loop.heading','空间与行为持续往返',(72,107))
    c.node('location','位置与邻居\n基质条件',(112,89),w=51,h=18,color='secondary',size=9)
    c.node('signals','局部信号\n与已有状态',(148,63),w=30,h=19,size=9)
    c.node('behaviors','移动／黏附／增殖\n清除／分泌',(112,36),w=63,h=20,size=9)
    c.node('space','空间与基质\n重新改变',(78,63),w=28,h=19,color='secondary',size=8.5)
    c.edge('location.signals',(137,84),(148,74),kind='influence')
    c.edge('signals.behaviors',(148,52),(141,41),kind='influence')
    c.edge('behaviors.space',(79,36),(76,52),kind='process')
    c.edge('space.location',(78,74),(86,86),kind='influence')
    c.note('示意：行为是多种可能选择，不是每个细胞必经的步骤；空间关系也不是固定成品。')
    return c.result()


def main():
    from production_utils import export_figure
    result=build_figure();fig=result.figure;OUT=Path(__file__).resolve().parent
    fig.savefig(OUT/'F13_spatial_feedback.pdf',metadata={'CreationDate':None,'ModDate':None})
    return export_figure(result,ROOT,OUT/'F13_spatial_feedback.pdf')


if __name__=='__main__':
    main()
