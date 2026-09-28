"""F14: 相同 DNA 的不同表观状态. Identical sequence, different environment."""
from pathlib import Path
import sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
from shared_shapes import Drawing


def draw_state(c,key,y,modified=False):
    c.dna(key+'.dna',22,y-7,72,gap=4,rungs=True)
    for i,letter in enumerate('ATCGAC'):
        c.text(key+f'.base.{i}',letter,(28+i*12,y+3),size=9.5)
    c.text(key+'.name','状态 B' if modified else '状态 A',(13,y+3),size=9)
    if modified:
        c.circle(key+'.methyl',(52,y+15),1.6,color='accent')
        c.line(key+'.methyl.bond',[(52,y+13.3),(52,y+6)],color='accent',width=.8)
        c.text(key+'.methyl.label','甲基',(66,y+15),size=8.5,color='accent')
    t=np.linspace(0,1,160)
    yy=y-3+(5 if modified else 3)*np.sin(t*4*np.pi)
    c.line(key+'.chromatin',np.column_stack((110+44*t,yy)),color='primary')
    for i,x in enumerate((118,137,149) if modified else (120,140)):
        c.circle(key+f'.protein.{i}',(x,y-3),2,color='supplement')
    c.edge(key+'.same_material',(97,y-4),(106,y-4),kind='zoom')


def build_figure():
    c=Drawing('F14',height=116)
    c.heading('sequence.heading','字母顺序相同',(22,106))
    c.heading('state.heading','局部状态不同',(108,106))
    draw_state(c,'state_a',81)
    draw_state(c,'state_b',43,modified=True)
    c.text('sequence.identity','两行都是 A T C G A C',(59,24),size=9)
    c.text('environment.label','修饰、包装与\n周边蛋白环境',(132,24),size=8.5)
    c.note('示意：加上甲基后 C 仍然是 C；甲基化并不是通用的“关闭”指令。')
    return c.result()


def main():
    from production_utils import export_figure
    result=build_figure();fig=result.figure;OUT=Path(__file__).resolve().parent
    fig.savefig(OUT/'F14_epigenetic_states.pdf',metadata={'CreationDate':None,'ModDate':None})
    return export_figure(result,ROOT,OUT/'F14_epigenetic_states.pdf')


if __name__=='__main__':
    main()
