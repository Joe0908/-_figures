"""F02: complementary_strands. Coordinates in mm; all objects remain editable."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shared_shapes import Drawing
from production_utils import export_figure
OUT = Path(__file__).resolve().parent

def build_figure():
    c=Drawing("F02",100)
    c.heading("panel", "两条链，保存互补的序列",(6,90))
    c.strand("upper.backbone",25,70,88)
    c.strand("lower.backbone",25,42,88)
    for i,(a,b) in enumerate(zip("ACGT","TGCA")):
        x=36+i*22
        c.text(f"upper.base.{i}",a,(x,63),size=11.5)
        c.text(f"lower.base.{i}",b,(x,49),size=11.5)
        c.line(f"upper.attach.{i}",[(x,70),(x,67)],width=.8)
        c.line(f"lower.attach.{i}",[(x,42),(x,45)],width=.8)
        c.line(f"pair.{i}",[(x,59),(x,53)],color="accent" if i==1 else "primary",dashed=True)
    for name,label,xy in [('u5','5′',(18,70)),('u3','3′',(120,70)),('l3','3′',(18,42)),('l5','5′',(120,42))]:
        c.text(name,label,xy,size=8.5)
    c.text("pair.rule","A 对 T\nC 对 G",(145,57))
    c.bracket("pair.bracket",26,112,31)
    c.text("meaning","已有一条链的序列，限制另一条链的对应位置",(85,23))
    c.note("配对线表示对应关系；两条链方向相反。序列与间距均为示意。",y=9)
    return c.result()


def main():
    result=build_figure()
    fig=result.figure
    fig.savefig(OUT / "F02_complementary_strands.pdf", metadata={"CreationDate":None,"ModDate":None})
    return export_figure(result,ROOT,OUT / "F02_complementary_strands.pdf")

if __name__=="__main__":
    main()
