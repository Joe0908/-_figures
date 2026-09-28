"""F28: 修改原有序列与补充功能性副本. Native semantic Artists; importing writes no files."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from shared_shapes import Drawing


LAYOUT={"height":126,"columns":(44,126),"start_y":96,"result_y":55}


def build_figure():
    c=Drawing("F28",height=LAYOUT["height"])
    c.heading("edit.heading","修改原有序列",(8,116.5))
    c.heading("addition.heading","补充功能性副本",(90,116.5))
    for i,x in enumerate(LAYOUT["columns"]):
        c.ellipse(f"start.cell.{i}",(x,96),66,28,color="secondary")
        c.dna(f"start.original.{i}",x-21,98,42,gap=4,region=(x-5,9))
        c.text(f"start.label.{i}","原异常版本",(x,89),size=9)
        c.ellipse(f"result.cell.{i}",(x,55),68,44,color="secondary")
        c.edge(f"operation.{i}",(x,81),(x,77.5),kind="intervention",source=f"start.cell.{i}",target=f"result.cell.{i}")
    c.dna("edit.modified_original",23,63,42,gap=4,region=(39,9))
    c.text("edit.action","在原位置\n改写目标序列",(44,49),size=9.5)
    c.dna("addition.original_retained",105,64,42,gap=4,region=(121,9))
    c.text("addition.original_label","原异常版本仍在",(126,58),size=8.5)
    c.dna("addition.extra_information",109,42,34,gap=4,color="accent")
    c.text("addition.extra_label","额外功能性信息",(126,38.5),size=8.5,color="accent")
    conditions=c.node("shared.expression","RNA、蛋白质的表达与实际功能\n仍取决于递送、存活目标细胞及持续性",(85,22),w=147,h=15,color="secondary",size=9)
    c.edge("edit.expression_condition",(44,33),(44,29.5),kind="conditional",source="edit.modified_original",target="shared.expression")
    c.edge("addition.expression_condition",(126,33),(126,29.5),kind="conditional",source="addition.extra_information",target="shared.expression")
    c.note("新增信息不默认整合进染色体；两种路径无固定优劣，额外副本也未必能抵消有害产物。",y=8)
    return c.result()


def main():
    from production_utils import export_figure
    result = build_figure()
    fig = result.figure
    OUT = Path(__file__).resolve().parent
    fig.savefig(OUT / "F28_edit_or_add_functional_copy.pdf", metadata={"CreationDate": None, "ModDate": None})
    return export_figure(result, ROOT, OUT / "F28_edit_or_add_functional_copy.pdf")


if __name__ == "__main__":
    main()
