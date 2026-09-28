"""F27: KJ 的分子修复与临床观察. Native semantic Artists; importing writes no files."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from shared_shapes import Drawing


LAYOUT={"height":140,"design_y":113,"mechanism_y":85,"observation_cards":[(6,21,76,37),(88,21,76,37)]}


def build_figure():
    c=Drawing("F27",height=LAYOUT["height"])
    c.heading("design.heading","设计、验证与递送",(6,130.5))
    design=[]
    for name,label,x,w in [("variant","CPS1 变异\n提前停止",24,34),("editor","个体化\n编辑器",64,32),("test","实验模型\n测试",104,32),("delivery","脂质纳米颗粒\n递送肝细胞",145,37)]:
        design.append(c.node("design."+name,label,(x,113),w=w,h=18,size=8.5))
    for i in range(3):
        c.edge(f"design.step.{i}",design[i]["right"],design[i+1]["left"],kind="process",source=["variant","editor","test"][i],target=["editor","test","delivery"][i])
    c.text("mechanism.heading","进入肝细胞后：拟实现的目标机制",(6,98),ha="left",size=9.5)
    c.dna("mechanism.sequence",15,83,36,gap=4,region=(31,6))
    c.text("mechanism.sequence_label","目标碱基改写",(33,76),size=8.5)
    cps=c.node("mechanism.cps1","拟增加完整 CPS1",(87,85),w=48,h=14,size=9)
    function=c.node("mechanism.function","拟改善\n氮处理功能",(145,85),w=37,h=17,color="secondary",size=9)
    c.edge("mechanism.sequence_to_protein",(52,85),cps["left"],kind="conditional",source="mechanism.sequence",target="mechanism.cps1")
    c.edge("mechanism.protein_to_function",cps["right"],function["left"],kind="conditional",source="mechanism.cps1",target="mechanism.function")
    c.heading("observation.heading","原稿报告的观察：单名患者",(6,65))
    for i,(x,y,w,h) in enumerate(LAYOUT["observation_cards"]):
        c.rect(f"observation.card.{i}",(x,y),w,h,color="supplement",weight=.07)
    c.text("early.date","2025 年早期临床报告",(11,52),ha="left",size=9.5,color="supplement")
    c.text("early.observed","更多膳食蛋白质\n部分清除氮药物减少\n未报告严重治疗相关不良事件",(44,38),size=8.5)
    c.text("early.boundary","一位患者的早期结果",(44,25),size=8.5,color="muted")
    c.text("later.date","2026 年医院一周年更新",(93,52),ha="left",size=9.5,color="supplement")
    c.text("later.observed","回家后能够行走、说话\n继续达到新的发育里程碑",(126,39),size=8.5)
    c.text("later.boundary","医院更新，非长期疗效结论",(126,25),size=8.5,color="muted")
    c.note("单人早期结果与后续更新均不等于已治愈；长期安全与持续获益仍待观察。",y=8)
    return c.result()


def main():
    from production_utils import export_figure
    result = build_figure()
    fig = result.figure
    OUT = Path(__file__).resolve().parent
    fig.savefig(OUT / "F27_kj_mechanism_and_observation.pdf", metadata={"CreationDate": None, "ModDate": None})
    return export_figure(result, ROOT, OUT / "F27_kj_mechanism_and_observation.pdf")


if __name__ == "__main__":
    main()
