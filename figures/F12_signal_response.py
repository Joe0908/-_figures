"""F12: 细胞怎样接收并回应外部信号. Relative timing, not measured minutes."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
from shared_shapes import Drawing


def build_figure():
    c=Drawing('F12',height=116)
    c.heading('outside.heading','外部输入',(6,105))
    c.rect('cell.boundary',(44,28),119,65,color='secondary',weight=.06)
    c.text('cell.label','细胞内',(59,87),size=9,color='muted')
    c.node('input','外部信号',(21,66),w=28,h=15,color='secondary',size=9)
    c.node('reception','受体／\n感应分子',(61,66),w=26,h=18,color='secondary',size=9)
    c.node('existing','已有蛋白\n状态改变',(100,66),w=29,h=18,size=9)
    c.node('fast','较快：细胞\n形状或行为改变',(145,84),w=34,h=17,color='primary',size=8.5)
    c.node('transcription','较慢：影响\n转录因子与转录',(99,39),w=37,h=17,size=8.5)
    c.node('products','RNA 与新蛋白\n后续行为改变',(145,39),w=34,h=17,color='secondary',size=8.5)
    c.node('conditions','既有细胞状态＋信号持续时间',(105,104),w=101,h=12,color='secondary',size=9)
    c.edge('input.reception',(36,66),(47,66),kind='influence')
    c.edge('reception.existing',(75,66),(84,66),kind='influence')
    c.edge('existing.fast',(115,72),(127,80),kind='influence')
    c.edge('existing.transcription',(100,56),(100,49),kind='influence')
    c.edge('transcription.products',(119,39),(127,39),kind='conditional')
    c.edge('conditions.response',(104,97),(104,77),kind='conditional')
    c.text('branch.meaning','同一输入，可走不同时间路径',(100,18),size=9,color='muted')
    c.note('示意：快慢取决于具体过程；并非所有反应都要先制造新的 RNA。')
    return c.result()


def main():
    from production_utils import export_figure
    result=build_figure();fig=result.figure;OUT=Path(__file__).resolve().parent
    fig.savefig(OUT/'F12_signal_response.pdf',metadata={'CreationDate':None,'ModDate':None})
    return export_figure(result,ROOT,OUT/'F12_signal_response.pdf')


if __name__=='__main__':
    main()
