"""F06: translation. Coordinates in mm; all objects remain editable."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shared_shapes import Drawing
from production_utils import export_figure
OUT = Path(__file__).resolve().parent

def build_figure():
    c=Drawing("F06",116)
    c.heading("heading","RNA 提供读取顺序，氨基酸来自独立原料",(6,106))
    c.strand("mrna",10,38,147,color="secondary")
    for i,codon in enumerate(['AUG','GCU','AAA','GGC']):
        c.text(f"codon.{i}",codon,(30+i*34,44),size=11.5)
    c.ellipse("ribosome",(64,61),40,46,color="supplement",fill=False)
    c.text("ribosome.label","核糖体",(65,26),size=9.5)
    c.text("mrna.label","mRNA",(145,30),size=9.5)
    c.line("trna",[(63,51),(59,61),(63,67),(67,61),(63,51)],color="accent")
    c.line("trna.carry.contact",[(63,67),(63,70)],color="accent")
    c.line("trna.label.leader",[(96,63),(70,62)],color="muted",width=.8)
    c.circle("incoming.aa",(63,72),r=2.3,color="accent")
    c.text("trna.label","tRNA",(111,65),size=8.5)
    c.text("trna.recognition","识别密码子",(118,55),size=8.5)
    c.edge("recognition",(102,50),(70,49),kind="template",color="accent")
    c.text("peptide.label","正在增长的氨基酸链",(44,93),size=9.5)
    for i,(x,y) in enumerate([(27,88),(35,85),(43,81),(51,78)]):
        if i:c.line(f"peptide.join.{i}",[[(27,88),(35,85),(43,81),(51,78)][i-1],(x,y)],color="primary",zorder=1)
        c.circle(f"peptide.aa.{i}",(x,y),r=2.3)
    c.edge("join",(60,73),(55,77),kind="process",color="accent")
    c.text("join.label","连接",(76,87),size=8.5)
    c.node("raw","独立的氨基酸原料",(128,86),w=49,h=12,color="accent",size=9.5)
    c.edge("carry",(101,82),(67,74),kind="process",color="accent")
    c.text("carry.label","由 tRNA 携带",(104,98),size=8.5)
    c.edge("read.direction",(16,19),(83,19),kind="process",color="secondary")
    c.text("read.label","沿 RNA 的读取方向",(115,19),size=8.5)
    c.note("核糖体按三个碱基一组读取；mRNA 不会变成氨基酸，肽链由氨基酸连接而成。",y=9)
    return c.result()


def main():
    result=build_figure()
    fig=result.figure
    fig.savefig(OUT / "F06_translation.pdf", metadata={"CreationDate":None,"ModDate":None})
    return export_figure(result,ROOT,OUT / "F06_translation.pdf")

if __name__=="__main__":
    main()
