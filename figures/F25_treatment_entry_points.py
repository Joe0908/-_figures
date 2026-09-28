"""F25: 生命链条上的不同治疗入口. Native semantic Artists; importing writes no files."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from shared_shapes import Drawing


LAYOUT = {"height":140,"rows":(112,82,52,22),"columns":{"dna":35,"rna":65,"protein":102,"cell":133,"organism":154}}


def preserved_dna(c,name,y):
    c.dna(name,27,y+3,16,gap=3,rungs=False)
    c.text(name+".caption","原序列保留",(35,y-4),size=8.5,color="muted")


def intervention(c,name,x,y,label):
    c.text(name+".verb",label,(x,y+13),size=9,color="accent")
    c.edge(name+".port",(x,y+9.5),(x,y+6.5),kind="intervention",source=name+".treatment",target=name+".target")


def build_figure():
    c=Drawing("F25",height=LAYOUT["height"])
    for name,x in LAYOUT["columns"].items():
        label={"dna":"DNA","rna":"RNA","protein":"蛋白及作用","cell":"细胞","organism":"组织与个体"}[name]
        c.text("navigation."+name,label,(x,131.5),size=8.5,color="muted")
    for i,y in enumerate(LAYOUT["rows"][:-1]):
        c.line(f"case.separator.{i}",[(6,y-13),(164,y-13)],color="muted",width=.45,role="panel_separator")
    y=112
    c.text("sma.case","SMA",(6,y+1),ha="left",size=9.5)
    c.text("sma.drug","nusinersen",(6,y-6),ha="left",size=8.5)
    preserved_dna(c,"sma.dna",y)
    rna=c.node("sma.rna","SMN2 剪接\n保留外显子7",(65,y),w=29,h=13,size=8.5)
    protein=c.node("sma.protein","完整 SMN\n增加",(102,y),w=29,h=13,size=8.5)
    outcome=c.node("sma.downstream","神经系统\n功能目标",(146,y),w=35,h=13,color="secondary",size=8.5)
    intervention(c,"sma.intervention",65,y,"调整剪接")
    c.edge("sma.template",rna["right"],protein["left"],kind="template",source="sma.rna",target="sma.protein")
    c.edge("sma.downstream_effect",protein["right"],outcome["left"],kind="conditional",source="sma.protein",target="sma.downstream")
    y=82
    c.text("ttr.case","遗传性 TTR\n淀粉样变",(6,y+2),ha="left",size=8.5)
    c.text("ttr.drug","patisiran",(6,y-8),ha="left",size=8.5)
    preserved_dna(c,"ttr.dna",y)
    rna=c.node("ttr.rna","TTR mRNA\n降解增加",(65,y),w=29,h=13,size=8.5)
    protein=c.node("ttr.protein","TTR 产生\n减少",(102,y),w=29,h=13,size=8.5)
    outcome=c.node("ttr.downstream","异常沉积\n相关过程",(146,y),w=35,h=13,color="secondary",size=8.5)
    intervention(c,"ttr.intervention",65,y,"减少 RNA")
    c.edge("ttr.template",rna["right"],protein["left"],kind="template",source="ttr.rna",target="ttr.protein")
    c.edge("ttr.downstream_effect",protein["right"],outcome["left"],kind="conditional",source="ttr.protein",target="ttr.downstream")
    y=52
    c.text("egfr.case","特定 EGFR\n改变的肺癌",(6,y+2),ha="left",size=8.5)
    c.text("egfr.drug","osimertinib",(6,y-8),ha="left",size=8.5)
    preserved_dna(c,"egfr.dna",y)
    c.text("egfr.rna","仍可产生",(65,y),size=8.5,color="muted")
    protein=c.node("egfr.protein","异常 EGFR\n功能受抑",(102,y),w=29,h=13,size=8.5)
    outcome=c.node("egfr.downstream","生长行为\n可能改变",(146,y),w=35,h=13,color="secondary",size=8.5)
    intervention(c,"egfr.intervention",102,y,"抑制功能")
    c.edge("egfr.downstream_effect",protein["right"],outcome["left"],kind="conditional",source="egfr.protein",target="egfr.downstream")
    y=22
    c.text("pku.case","PKU",(6,y+2),ha="left",size=9.5)
    c.text("pku.management","营养管理",(6,y-5),ha="left",size=8.5)
    preserved_dna(c,"pku.dna",y)
    c.text("pku.rna","未改写",(65,y),size=8.5,color="muted")
    c.node("pku.pah","PAH 功能\n仍不足",(102,y),w=29,h=13,color="secondary",size=8.5)
    c.node("pku.input","苯丙氨酸\n输入受控",(146,y),w=35,h=13,color="secondary",size=8.5)
    intervention(c,"pku.intervention",146,y,"管理系统输入")
    c.note("四个独立病例；入口取决于递送、持续性与风险。PKU 管理输入，并非完全去除。",y=8)
    return c.result()


def main():
    from production_utils import export_figure
    result = build_figure()
    fig = result.figure
    OUT = Path(__file__).resolve().parent
    fig.savefig(OUT / "F25_treatment_entry_points.pdf", metadata={"CreationDate": None, "ModDate": None})
    return export_figure(result, ROOT, OUT / "F25_treatment_entry_points.pdf")


if __name__ == "__main__":
    main()
