"""F07: sequence_structure_action. Coordinates in mm; all objects remain editable."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shared_shapes import Drawing
from production_utils import export_figure
OUT = Path(__file__).resolve().parent

def build_figure():
    c=Drawing("F07",116)
    for x,title in [(6,"氨基酸顺序"),(66,"折叠与表面性质"),(128,"接触与作用")]:
        c.heading("heading."+str(x),title,(x,106))
    chain=[(12,76),(19,78),(26,75),(33,78),(40,76)]
    for i,xy in enumerate(chain):
        if i:c.line(f"sequence.join.{i}",[chain[i-1],xy],color="primary",zorder=1)
        c.circle(f"sequence.aa.{i}",xy,r=2.6,color="accent" if i==2 else "primary")
    c.text("change.label","某一位置改变",(26,62),size=8.5)
    c.edge("folding",(46,76),(64,76),kind="conditional")
    c.line("folded",[(71,67),(68,78),(77,88),(85,82),(75,76),(86,67),(96,77),(91,90)],width=2)
    c.circle("surface",(94,79),r=2.7,color="accent")
    c.text("surface.label","接触面与化学性质",(83,55),size=8.5)
    c.edge("effect",(103,76),(119,76),kind="conditional")
    c.ellipse("partner",(143,77),30,24,color="secondary")
    c.text("partner.label","作用伙伴",(143,77),size=9.5)
    c.circle("contact",(126,79),r=2.7,color="accent")
    c.node("action","细胞过程改变",(142,43),w=39,h=12,color="secondary",size=8.5)
    c.edge("action.link",(143,63),(143,51),kind="conditional")
    c.text("condition","位置、折叠与接触条件共同影响结果",(83,28),size=9.5)
    c.note("一个氨基酸变化可能保留原有作用，也可能改变关键接触；示意不表示必然失活。",y=9)
    return c.result()


def main():
    result=build_figure()
    fig=result.figure
    fig.savefig(OUT / "F07_sequence_structure_action.pdf", metadata={"CreationDate":None,"ModDate":None})
    return export_figure(result,ROOT,OUT / "F07_sequence_structure_action.pdf")

if __name__=="__main__":
    main()
