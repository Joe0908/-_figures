"""F19: 五扇窗口观察同一个细胞. Observation links carry no arrowheads."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
from shared_shapes import Drawing


def build_figure():
    c=Drawing('F19',height=126)
    c.ellipse('cell.system',(85,67),76,59,color='secondary',weight=.06)
    c.text('cell.label','同一细胞系统',(85,60),size=9.5)
    c.dna('cell.dna',60,73,33,gap=3)
    for i,x in enumerate((78,85)):
        c.circle(f'cell.state.{i}',(x,79),1.1,color='accent')
        c.line(f'cell.state.bond.{i}',[(x,78),(x,76)],color='accent',width=.8)
    c.text('cell.dna.label','DNA 与调控状态',(77,66),size=8.5)
    for i in range(2):
        c.strand(f'cell.rna.{i}',99,73+i*4,13)
    c.text('cell.rna.label','RNA',(106,66),size=8.5)
    for i,x in enumerate((66,75)):
        c.circle(f'cell.protein.{i}',(x,53),2.1,color='primary')
    c.text('cell.protein.label','蛋白质',(71,44),size=8.5)
    for i,(x,y) in enumerate(((98,53),(105,54),(111,52))):
        c.circle(f'cell.metabolite.{i}',(x,y),1.2,color='primary')
    c.text('cell.metabolite.label','代谢物',(102,47),size=8.5)
    windows=[
        ('genome','基因组\n序列',(32,111),48,(32,102),(61,77)),
        ('epigenome','表观基因组\n调控状态',(85,111),48,(85,102),(85,81)),
        ('transcriptome','转录组\nRNA 存量／版本',(138,111),48,(138,102),(112,78)),
        ('proteome','蛋白质组\n数量与状态',(41,22),62,(41,31),(66,51)),
        ('metabolome','代谢组\n小分子存量',(129,22),62,(129,31),(111,50)),
    ]
    for key,title,center,width,start,end in windows:
        c.node('window.'+key,title,center,w=width,h=17,color='supplement',size=9)
        c.edge('observe.'+key,start,end,kind='observe',source='window.'+key+'.boundary',target='measure.'+key)
        c.circle('measure.'+key,end,.65,color='supplement',weight=1)
    c.note('“同一细胞”是认知系统；不保证同一枚细胞同时完成五类测量，各窗口也有检测范围。')
    return c.result()


def main():
    from production_utils import export_figure
    result=build_figure();fig=result.figure;OUT=Path(__file__).resolve().parent
    fig.savefig(OUT/'F19_five_windows.pdf',metadata={'CreationDate':None,'ModDate':None})
    return export_figure(result,ROOT,OUT/'F19_five_windows.pdf')


if __name__=='__main__':
    main()
