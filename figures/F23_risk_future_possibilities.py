"""F23: 风险描述未来机会. Native semantic Artists; importing writes no files."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from shared_shapes import Drawing


LAYOUT = {"height": 126, "reference_y": 100, "individual": (28,66), "futures": [(139,78),(139,51)]}


def build_figure():
    c = Drawing("F23", height=LAYOUT["height"])
    c.heading("title","风险估计从人群而来，用于判断未来机会",(6,116.5))
    ref=c.node("reference","相似条件人群\n已有的观察结果",(35,100),w=58,h=19,color="supplement")
    estimate=c.node("estimate","特定疾病、人群与时期\n未来患病机会的估计",(122,100),w=80,h=19,color="supplement")
    c.edge("evidence.reference_to_estimate",ref["right"],estimate["left"],kind="observe",source="reference",target="estimate")
    now=c.node("individual.now","一个人\n现在未患病",LAYOUT["individual"],w=41,h=20,color="secondary")
    disease=c.node("future.disease","未来患病",LAYOUT["futures"][0],w=46,h=13)
    no_disease=c.node("future.no_disease","同期未患病",LAYOUT["futures"][1],w=46,h=13,color="secondary")
    c.edge("future.possibility.disease",now["right"],disease["left"],kind="conditional",source="individual.now",target="future.disease")
    c.edge("future.possibility.no_disease",now["right"],no_disease["left"],kind="conditional",source="individual.now",target="future.no_disease")
    c.edge("estimate.reference_for_individual",(103,90.5),(86,79),kind="observe",source="estimate",target="future.possibilities")
    c.text("estimate.role","提供参照",(79,87),size=8.5,color="supplement")
    c.text("future.label","可能的未来",(104,44),size=9.5)
    cond=c.node("conditions","遗传背景、年龄、暴露、身体状态\n条件改变或出现新证据时，可以更新估计",(85,26),w=143,h=20,color="secondary",size=9)
    c.edge("conditions.influence",(85,36),(85,56),kind="influence",source="conditions",target="future.possibilities")
    c.note("分支不表示概率比例；风险不能预先点名谁会患病，也不等于当前诊断。",y=8)
    return c.result()


def main():
    from production_utils import export_figure
    result = build_figure()
    fig = result.figure
    OUT = Path(__file__).resolve().parent
    fig.savefig(OUT / "F23_risk_future_possibilities.pdf", metadata={"CreationDate": None, "ModDate": None})
    return export_figure(result, ROOT, OUT / "F23_risk_future_possibilities.pdf")


if __name__ == "__main__":
    main()
