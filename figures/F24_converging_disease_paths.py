"""F24: 相似疾病表现可以来自不同路径. Native semantic Artists; importing writes no files."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from shared_shapes import Drawing


LAYOUT = {"height":116,"path_y":(81,49),"disease":(143,65)}


def build_figure():
    c = Drawing("F24",height=LAYOUT["height"])
    c.heading("title","同一病名，需要继续辨认机制",(6,106.5))
    c.text("patient.a","甲",(10,81),size=10)
    egfr=c.node("path.a.egfr","特定 EGFR\n激活改变",(41,81),w=42,h=18)
    signal=c.node("path.a.signal","异常生长\n信号持续",(91,81),w=38,h=18)
    c.edge("path.a.signal_propagation",egfr["right"],signal["left"],kind="process",source="path.a.egfr",target="path.a.signal")
    c.text("patient.b","乙",(10,49),size=10)
    unknown=c.node("path.b.unknown","其他可能路径\n或机制尚未明确",(47,49),w=54,h=18,color="secondary")
    disease=c.node("disease.shared","肺腺癌\n相似组织表现",LAYOUT["disease"],w=40,h=27)
    c.edge("convergence.a",signal["right"],(123,72),kind="conditional",source="path.a.signal",target="disease.shared")
    c.edge("convergence.b",unknown["right"],(123,58),kind="conditional",source="path.b.unknown",target="disease.shared")
    c.text("classification.label","组织层分类",(143,91),size=9,color="muted")
    c.text("unknown.boundary","尚未明确 ≠ 没有机制",(86,36),size=8.5,color="muted")
    c.rect("measurement.boundary",(6,14),158,16,color="supplement",weight=.06)
    c.text("measurement.question","分子检测：哪些变化真正参与了疾病的形成和维持？",(85,24),size=9)
    c.text("measurement.caution","发现变化或有用标志物，并不自动证明因果。",(85,18),size=8.5,color="muted")
    c.edge("measurement.port",(41,40),(41,30),kind="observe",source="path.b.unknown",target="measurement.boundary")
    c.note("不同路径可汇合到相似表现；此图不为乙补造具体驱动基因。",y=8)
    return c.result()


def main():
    from production_utils import export_figure
    result = build_figure()
    fig = result.figure
    OUT = Path(__file__).resolve().parent
    fig.savefig(OUT / "F24_converging_disease_paths.pdf", metadata={"CreationDate": None, "ModDate": None})
    return export_figure(result, ROOT, OUT / "F24_converging_disease_paths.pdf")


if __name__ == "__main__":
    main()
