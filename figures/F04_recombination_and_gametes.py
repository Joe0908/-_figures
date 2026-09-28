"""F04: recombination_and_gametes. Coordinates in mm; all objects remain editable."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shared_shapes import Drawing
from production_utils import export_figure
OUT = Path(__file__).resolve().parent

def chromosome(c,name,x,y,colors):
    for i,color in enumerate(colors):
        c.rect(f"{name}.{i}",(x+7*i,y),7,5.5,color=color,weight=.32,radius=0)
        c.text(f"{name}.origin.{i}","A" if color=="primary" else "B",(x+7*i+3.5,y+2.75),size=8.5)

def build_figure():
    c=Drawing("F04",126)
    for x,title in [(6,"亲本的同源染色体"),(68,"交换对应片段"),(127,"抽取一种配子")]:
        c.heading("heading."+str(x),title,(x,116))
    for k,(y,title) in enumerate([(91,"父方示例"),(54,"母方示例")]):
        c.text(f"parent.{k}",title,(6,y+11),ha="left",size=8.5)
        chromosome(c,f"pair.{k}.a",10,y,['primary']*4)
        chromosome(c,f"pair.{k}.b",10,y-8,['secondary']*4)
        c.edge(f"exchange.{k}",(44,y-2),(67,y-2),kind="process")
        chromosome(c,f"recombined.{k}.a",73,y,['primary']*2+['secondary']*2)
        chromosome(c,f"recombined.{k}.b",73,y-8,['secondary']*2+['primary']*2)
        c.edge(f"gamete.{k}",(107,y-2),(126,y-2),kind="process")
        chromosome(c,f"selected.{k}",132,y-2,['primary']*2+['secondary']*2 if k==0 else ['secondary']*2+['primary']*2)
    c.text("sperm","精子中的一份",(146,78),size=8.5)
    c.text("egg","卵子中的一份",(146,41),size=8.5)
    c.line("combine.sperm.route",[(163,87),(163,29),(158,29)])
    c.edge("combine.sperm",(158,29),(154,26.5),kind="process")
    c.line("combine.egg.route",[(146,37),(122,37),(122,18)])
    c.edge("combine.egg",(122,18),(126,18),kind="process")
    chromosome(c,"zygote.p",126,21,['primary']*2+['secondary']*2)
    chromosome(c,"zygote.m",126,15,['secondary']*2+['primary']*2)
    c.text("zygote.label","受精组合：来自双亲的两份",(117,31),ha="right",size=9.5)
    c.note("A/B 区分每位亲本内部的同源来源；只画部分染色体与一种配子组合。",y=8)
    return c.result()


def main():
    result=build_figure()
    fig=result.figure
    fig.savefig(OUT / "F04_recombination_and_gametes.pdf", metadata={"CreationDate":None,"ModDate":None})
    return export_figure(result,ROOT,OUT / "F04_recombination_and_gametes.pdf")

if __name__=="__main__":
    main()
