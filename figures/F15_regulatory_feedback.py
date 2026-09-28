"""F15: 基因调控与表观状态相互影响. Labelled directional mechanisms."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
from shared_shapes import Drawing


def build_figure():
    c=Drawing('F15',height=116)
    c.node('context','外部信号与历史',(85,103),w=67,h=12,color='secondary',size=9)
    c.node('state','染色质状态\n修饰与核小体组织',(32,75),w=49,h=20,color='secondary',size=9)
    c.node('access','分子接触机会\n调控蛋白组合',(85,75),w=41,h=20,size=9)
    c.node('transcription','启动子／增强子协作\n与转录',(138,75),w=49,h=20,size=9)
    c.edge('state.access',(58,75),(63,75),kind='influence')
    c.edge('access.transcription',(107,75),(112,75),kind='conditional')
    c.edge('context.state',(62,96),(40,87),kind='conditional')
    c.edge('context.regulation',(105,96),(130,87),kind='conditional')
    c.node('remodeling','相关蛋白识别／招募\n局部状态被重新塑造',(85,37),w=71,h=20,color='secondary',size=9)
    c.edge('activity.remodeling',(138,63),(122,42),kind='influence')
    c.edge('remodeling.state',(48,38),(31,63),kind='influence')
    c.text('forward.label','状态影响基因的使用机会',(85,88),size=8.5,color='muted')
    c.text('return.label','调控活动反过来塑造状态',(85,20),size=9,color='muted')
    c.note('两条方向代表不同机制；修饰与高表达同时出现，尚不足以证明因果。')
    return c.result()


def main():
    from production_utils import export_figure
    result=build_figure();fig=result.figure;OUT=Path(__file__).resolve().parent
    fig.savefig(OUT/'F15_regulatory_feedback.pdf',metadata={'CreationDate':None,'ModDate':None})
    return export_figure(result,ROOT,OUT/'F15_regulatory_feedback.pdf')


if __name__=='__main__':
    main()
