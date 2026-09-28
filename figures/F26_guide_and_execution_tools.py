"""F26: 引导 RNA 定位与执行工具的不同任务. Native semantic Artists; importing writes no files."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from shared_shapes import Drawing


LAYOUT = {"height":126,"navigation_frame":(6,31,60,79),"cut_frame":(78,62,86,50),"base_frame":(78,24,86,33)}


def build_figure():
    c=Drawing("F26",height=LAYOUT["height"])
    c.heading("title","先定位，再由不同工具执行任务",(6,116.5))
    for key in ["navigation_frame","cut_frame","base_frame"]:
        x,y,w,h=LAYOUT[key]
        c.rect(key,(x,y),w,h,color="secondary",fill=False)
    c.text("navigation.heading","共同的定位模块",(36,102),size=10)
    c.ellipse("navigation.cas_carrier",(35,69),26,24,color="secondary",weight=.10)
    c.dna("navigation.target",13,65,44,gap=4,region=(31,8))
    c.strand("navigation.guide",28,82,14,color="accent")
    c.text("navigation.guide_label","引导 RNA",(35,90),size=9.5)
    for i,x in enumerate([31,35,39]):
        c.line(f"navigation.recognition.{i}",[(x,79),(x,73)],color="accent",dashed=True,width=.8,role="recognition")
    c.text("navigation.target_label","DNA 目标区域",(36,53),size=9)
    c.text("navigation.carrier_label","定位载体携带工具",(36,42),size=8.5)
    c.edge("tool_branch.cut",(66,78),(78,90),kind="order",source="navigation",target="cut")
    c.edge("tool_branch.base",(66,61),(78,41),kind="order",source="navigation",target="base")
    c.text("cut.heading","切割工具",(83,105),ha="left",size=10)
    c.dna("cut.left",84,88,11,gap=4)
    c.dna("cut.right",99,88,11,gap=4)
    c.line("cut.break.upper",[(95.5,94),(98,90)],color="accent",width=1.5,role="intervention")
    c.line("cut.break.lower",[(95.5,90),(98,86)],color="accent",width=1.5,role="intervention")
    repair=c.node("cut.repair","细胞修复",(139,90),w=39,h=12,size=9)
    c.edge("cut.to_repair",(111,90),repair["left"],kind="process",source="cut.dna",target="cut.repair")
    c.edge("repair.indel",(134,84),(124,76),kind="conditional",source="cut.repair",target="repair.indel_result")
    c.edge("repair.template",(144,84),(151,76),kind="conditional",source="cut.repair",target="repair.template_result")
    c.text("repair.indel_result","插入／删除",(121,69),size=8.5)
    c.text("repair.template_result","依模板*",(151,69),size=8.5)
    c.text("base.heading","碱基编辑工具",(83,51),ha="left",size=10)
    c.dna("base.target",85,33,31,gap=4,region=(99,6))
    c.text("base.action","改写某些碱基\n无需先切断双链",(140,37),size=8.5)
    c.note("* 按模板修复需要额外模板与合适条件；工具执行不保证得到预期序列。",y=16,name="repair.condition")
    c.note("定位与执行是不同任务；碱基编辑受位点与工具限制，图中地址仅为抽象示意。",y=8)
    return c.result()


def main():
    from production_utils import export_figure
    result = build_figure()
    fig = result.figure
    OUT = Path(__file__).resolve().parent
    fig.savefig(OUT / "F26_guide_and_execution_tools.pdf", metadata={"CreationDate": None, "ModDate": None})
    return export_figure(result, ROOT, OUT / "F26_guide_and_execution_tools.pdf")


if __name__ == "__main__":
    main()
