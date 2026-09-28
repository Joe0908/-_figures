"""F05: transcription_and_splicing. Coordinates in mm; all objects remain editable."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shared_shapes import Drawing
from production_utils import export_figure
OUT = Path(__file__).resolve().parent

def build_figure():
    c=Drawing("F05",116)
    c.heading("transcription.heading","先按模板合成 RNA",(6,106))
    c.heading("splicing.heading","再加工出不同版本",(95,106))
    c.dna("dna",9,81,59)
    c.text("dna.label","DNA 保留在原处",(39,94),size=9.5)
    c.edge("template",(27,79),(27,67),kind="template")
    c.segments("initial",[1,2,3,4],9,54,segment_w=12)
    c.text("initial.label","初始 RNA",(16,44),size=9.5)
    c.node("raw","游离 RNA 原料",(36,26),w=43,h=12,color="secondary",size=8.5)
    c.edge("assembly",(49,33),(49,51),kind="process",color="secondary")
    c.edge("branch.a",(69,58),(102,80),kind="process")
    c.edge("branch.b",(69,56),(102,39),kind="process")
    c.text("splicing","剪接",(86,57),size=8.5)
    c.segments("mature.a",[1,2,4],105,80,segment_w=14,color="secondary")
    c.segments("mature.b",[1,3,4],105,36,segment_w=14,color="secondary")
    c.text("a.label","成熟 RNA 版本 A",(128,95),size=9.5)
    c.text("b.label","成熟 RNA 版本 B",(128,51),size=9.5)
    c.note("编号只是片段示意；不同加工可保留不同组合，并非所有基因都有这两种版本。",y=9)
    return c.result()


def main():
    result=build_figure()
    fig=result.figure
    fig.savefig(OUT / "F05_transcription_and_splicing.pdf", metadata={"CreationDate":None,"ModDate":None})
    return export_figure(result,ROOT,OUT / "F05_transcription_and_splicing.pdf")

if __name__=="__main__":
    main()
