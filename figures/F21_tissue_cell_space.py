"""F21: 从组织平均值到细胞与空间. Native semantic Artists; importing writes no files."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from shared_shapes import Drawing


LAYOUT = {"height": 126, "source": (69, 92, 32, 22), "panels": [(6, 28, 49, 43), (61, 28, 48, 43), (115, 28, 49, 43)]}
CELL = {"癌": "primary", "免": "secondary", "间": "supplement"}


def cell(c, name, kind, xy, r=3.2):
    c.circle(name + ".shape", xy, r, color=CELL[kind])
    c.text(name + ".identity", kind, xy, size=8.5)


def build_figure():
    c = Drawing("F21", height=LAYOUT["height"])
    c.heading("title", "同一块组织，保留不同的信息", (6, 116.5))
    c.rect("source.tissue", (69, 92), 32, 22, color="secondary", weight=.07)
    for i, (x, y, k) in enumerate([(76,107,"癌"),(85,107,"免"),(94,107,"癌"),(76,98,"间"),(85,98,"癌"),(94,98,"免")]):
        cell(c, f"source.cell.{i}", k, (x, y))
    c.text("source.label", "示例组织", (110, 103), ha="left")
    for i,(k,word) in enumerate([("癌","癌细胞"),("免","免疫细胞"),("间","间质细胞")]):
        cell(c, f"legend.{i}", k, (10, 106-i*10))
        c.text(f"legend.label.{i}", word, (17,106-i*10), ha="left", size=8.5)
    for i,(x,y,w,h) in enumerate(LAYOUT["panels"]):
        c.rect(f"measure.{i}.frame",(x,y),w,h,color="supplement",fill=False)
    for i, (end, label) in enumerate([((30,79),"群体组学"),((85,79),"单细胞组学"),((140,79),"空间组学")]):
        c.edge(f"sampling.{i}",(76+9*i,92),end,kind="observe",source="source.tissue",target=f"measure.{i}.frame")
        c.text(f"measure.{i}.heading", label, (end[0],74), size=10)
    c.text("bulk.question", "发生了什么？", (30.5,63), size=10)
    for i,k in enumerate(["癌","免","间"]):
        cell(c,f"bulk.token.{i}",k,(20+i*10,50))
    c.bracket("bulk.aggregate",16,44,43,color="supplement")
    c.text("bulk.result","混合后的总体信号",(30.5,35),size=8.5)
    c.text("single.question", "谁发生变化？", (85,63), size=10)
    for i,(x,y,k) in enumerate([(70,51,"癌"),(84,49,"免"),(100,52,"癌"),(75,40,"间"),(94,40,"免")]):
        cell(c,f"single.cell.{i}",k,(x,y))
    c.text("single.result","身份和状态",(85,31.5),size=8.5)
    c.text("space.question", "变化在哪里？", (139.5,63), size=10)
    c.rect("space.coordinates",(123,35),33,21,color="secondary",fill=False,radius=0)
    for i,(x,y,k) in enumerate([(129,50,"癌"),(139,50,"免"),(150,50,"癌"),(129,40,"间"),(139,40,"癌"),(150,40,"免")]):
        cell(c,f"space.cell.{i}",k,(x,y),r=3.3)
    c.text("space.result","保留原位关系",(139.5,31),size=8.5)
    c.note("相似平均值，可能来自单个细胞状态改变，也可能来自细胞组成改变。", y=18, name="mean.ambiguity")
    c.note("示意分布；空间测量未必达到单细胞分辨率，相邻也不等于通讯。", y=8)
    return c.result()


def main():
    from production_utils import export_figure
    result = build_figure()
    fig = result.figure
    OUT = Path(__file__).resolve().parent
    fig.savefig(OUT / "F21_tissue_cell_space.pdf", metadata={"CreationDate": None, "ModDate": None})
    return export_figure(result, ROOT, OUT / "F21_tissue_cell_space.pdf")


if __name__ == "__main__":
    main()
