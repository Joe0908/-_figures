"""F29: CAR T 进入身体后仍继续运行. Native semantic Artists; importing writes no files."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from shared_shapes import Drawing


LAYOUT={"height":140,"running_y":117,"response_y":92,"target_y":53}


def target_cell(c,name,center,kind,color):
    c.circle(name+".cell",center,7,color=color)
    x,y=center
    c.line(name+".cd19_stalk",[(x,y+7),(x,y+10)],color="primary",width=1.2,role="receptor")
    c.line(name+".cd19_tip",[(x-2,y+10),(x+2,y+10)],color="primary",width=1.2,role="receptor")
    c.text(name+".identity",kind,(x,y-12),size=8.5)
    c.text(name+".marker","CD19",(x,y+15),size=8.5)


def build_figure():
    c=Drawing("F29",height=LAYOUT["height"])
    c.heading("a.heading","A  回输后的 CAR-T 继续运行",(6,130.5))
    search=c.node("a.search","迁移与搜索",(26,117),w=36,h=13,color="secondary",size=9)
    recognize=c.node("a.recognize","识别 CD19",(73,117),w=36,h=13,size=9)
    response=c.node("a.response","激活与杀伤",(124,117),w=44,h=13,size=9)
    c.edge("a.search_to_recognize",search["right"],recognize["left"],kind="process",source="a.search",target="a.recognize")
    c.edge("a.recognize_to_response",recognize["right"],response["left"],kind="conditional",source="a.recognize",target="a.response")
    expansion=c.node("a.expansion","扩增",(102,92),w=34,h=13,color="secondary",size=9)
    c.edge("a.activation_to_expansion",(117,110.5),(109,98.5),kind="conditional",source="a.response",target="a.expansion")
    c.edge("a.loop",(85,92),(26,110.5),kind="process",rad=-.28,source="a.expansion",target="a.search")
    c.text("a.loop_label","继续搜索",(47,85),size=8.5)
    fate=c.node("a.persistence","可能持续存在\n或逐渐失功",(146,92),w=35,h=17,color="secondary",size=8.5)
    c.edge("a.possible_fate",expansion["right"],fate["left"],kind="conditional",source="a.expansion",target="a.persistence")
    c.line("panel.separator",[(6,79),(164,79)],color="muted",width=.5,role="panel_separator")
    c.text("b.heading","B  同一靶点的不同细胞",(6,73),ha="left",size=10)
    target_cell(c,"b.tumor",(26,51),"肿瘤细胞","primary")
    target_cell(c,"b.normal",(65,51),"正常 B 细胞","secondary")
    c.text("b.on_target","正常 B 细胞减少属在靶影响",(44,27),size=8.5)
    c.line("panel.vertical",[(87,21),(87,76)],color="muted",width=.5,role="panel_separator")
    c.text("c.heading","C  可能的群体变化",(93,73),ha="left",size=10)
    for i,(x,y) in enumerate([(103,56),(111,56),(107,48)]):
        c.circle(f"c.before.recognizable.{i}",(x,y),3,color="primary")
    c.circle("c.before.escape",(117,48),3,color="supplement")
    for i,(x,y) in enumerate([(145,55),(155,48)]):
        c.circle(f"c.after.escape.{i}",(x,y),3,color="supplement")
    c.edge("c.selection",(123,53),(137,53),kind="conditional",source="c.before",target="c.after")
    c.text("c.before_label","易识别者减少",(110,38),size=8.5)
    c.text("c.after_label","低 CD19 等\n逃逸者可能留存",(150,37),size=8.5)
    c.text("c.boundary","群体变化不等于必然复发",(128,25),size=8.5)
    c.note("还需监测炎症反应与神经系统毒性；示意细胞数不表示疗效、毒性或复发概率。",y=8)
    return c.result()


def main():
    from production_utils import export_figure
    result = build_figure()
    fig = result.figure
    OUT = Path(__file__).resolve().parent
    fig.savefig(OUT / "F29_cart_continues_in_body.pdf", metadata={"CreationDate": None, "ModDate": None})
    return export_figure(result, ROOT, OUT / "F29_cart_continues_in_body.pdf")


if __name__ == "__main__":
    main()
