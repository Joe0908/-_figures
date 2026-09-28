"""F03: old_and_new_strands. Coordinates in mm; all objects remain editable."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shared_shapes import Drawing
from production_utils import export_figure
OUT = Path(__file__).resolve().parent

def build_figure():
    c=Drawing("F03",116)
    for x,title in [(6,"原来的一份"),(65,"各自作为模板"),(123,"两份复制结果")]:
        c.heading("heading."+str(x),title,(x,106))
    c.strand("old.a.start",10,71,32)
    c.strand("old.b.start",10,57,32,color="secondary")
    c.text("old.a.tag","旧链 A",(26,79),size=8.5)
    c.text("old.b.tag","旧链 B",(26,49),size=8.5)
    for i,x in enumerate(range(12,41,5)):
        c.line(f"pairs.{i}",[(x,60),(x,68)],width=.8,color="muted")
    # Continuous old-strand paths preserve identity across the three views.
    c.line("old.a.path",[(42,71),(61,84),(158,84)],width=1.5)
    c.line("old.b.path",[(42,57),(61,43),(158,43)],width=1.5,color="secondary")
    c.strand("new.a",67,73,91,color="accent",dashed=True)
    c.strand("new.b",67,54,91,color="accent",dashed=True)
    c.edge("template.a",(89,82),(89,75),kind="template")
    c.edge("template.b",(89,45),(89,52),kind="template")
    c.text("template.key","虚线箭头：模板参照",(87,94),size=8.5)
    c.text("output.a","旧链 A ＋ 新链",(140,64),size=8.5)
    c.text("output.b","新链 ＋ 旧链 B",(140,33),size=8.5)
    c.node("raw","游离的 DNA 原料",(57,23),w=49,h=12,color="accent",size=8.5)
    c.edge("synthesis",(72,30),(76,51),kind="process",color="accent")
    c.text("synthesis.label","合成新链",(92,36),size=8.5)
    c.note("旧链各保留一条；铜色虚线是新链。仅示意链的去向，不表示真实空间或时间比例。",y=9)
    return c.result()


def main():
    result=build_figure()
    fig=result.figure
    fig.savefig(OUT / "F03_old_and_new_strands.pdf", metadata={"CreationDate":None,"ModDate":None})
    return export_figure(result,ROOT,OUT / "F03_old_and_new_strands.pdf")

if __name__=="__main__":
    main()
