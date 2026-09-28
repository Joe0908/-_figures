"""F10: access_to_transcription. Coordinates in mm; all objects remain editable."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shared_shapes import Drawing
from production_utils import export_figure
OUT = Path(__file__).resolve().parent

def build_figure():
    c=Drawing("F10",126)
    c.heading("a.heading","包装影响接近机会",(6,116))
    c.heading("b.heading","空间接触与分子组装",(74,116))
    for i,x in enumerate([16,29,42]):
        c.circle(f"packing.protein.{i}",(x,88),r=5,color="supplement")
    c.line("packing.dna",[(8,89),(12,94),(20,94),(24,82),(33,82),(37,94),(45,94),(51,89)],width=1.4)
    c.text("packing.label","局部包装动态变化",(29,74),size=8.5)
    c.edge("access",(54,87),(69,87),kind="conditional")
    # A continuous folded DNA path brings distant regions into spatial contact.
    c.line("folded.dna",[(75,79),(87,85),(91,97),(109,102),(124,94),(121,81),(110,76),(113,63),(150,63)],width=1.5)
    c.rect("enhancer",(85,81),9,5,color="accent",weight=.32,radius=0,role="region_fill")
    c.rect("promoter",(108,68),9,5,color="accent",weight=.32,radius=0,role="region_fill")
    c.text("enhancer.label","增强子",(75,99),size=8.5)
    c.text("promoter.label","启动子",(141,75),size=8.5)
    c.ellipse("tf",(96,76),13,10,color="secondary")
    c.line("tf.contact",[(90,82),(92,79)],color="secondary",width=1.1)
    c.edge("cooperation",(102,73),(110,64),kind="conditional",color="secondary")
    c.text("tf.label","转录因子",(78,64),size=8.5)
    c.ellipse("machine",(117,58),23,13,color="supplement")
    c.text("machine.label","转录机器",(143,52),size=8.5)
    c.edge("template",(151,63),(155,33),kind="template")
    c.strand("rna",104,31,45,color="secondary")
    c.text("rna.label","新合成的 RNA",(126,22),size=8.5)
    c.node("raw","RNA 原料",(73,31),w=27,h=12,color="secondary",size=8.5)
    c.edge("synthesis",(89,31),(101,31),kind="process",color="secondary")
    c.text("condition","可接近性只是条件之一；\n因子状态与协作也影响转录。",(6,45),ha="left",size=8.5)
    c.note("DNA 折叠使序列上相距较远的区域靠近；并非所有转录因子都促进转录。",y=9)
    return c.result()


def main():
    result=build_figure()
    fig=result.figure
    fig.savefig(OUT / "F10_access_to_transcription.pdf", metadata={"CreationDate":None,"ModDate":None})
    return export_figure(result,ROOT,OUT / "F10_access_to_transcription.pdf")

if __name__=="__main__":
    main()
