"""F22: 同样风险翻倍，不同绝对风险. Native semantic Artists; importing writes no files."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from shared_shapes import Drawing


LAYOUT = {"height": 116, "grid_x": (12, 53), "grid_y": (63, 24), "step": 2.9, "radius": .90}


def hundred(c, name, x, y, positive):
    # Fixed denominator: exactly 100 equally sized marks in every group.
    for i in range(100):
        xx = x + (i % 10) * LAYOUT["step"]
        yy = y + (9 - i // 10) * LAYOUT["step"]
        active = i < positive
        c.circle(f"{name}.person.{i:03d}", (xx, yy), LAYOUT["radius"],
                 color="accent" if active else "muted", fill="accent" if active else "background")


def build_figure():
    c = Drawing("F22", height=LAYOUT["height"])
    c.heading("scope", "假设示例 · 未来十年 · 每组 100 人", (6,106.5))
    for row,(a,b,delta,y) in enumerate([(1,2,1,63),(10,20,10,24)]):
        for col,n in enumerate([a,b]):
            x=LAYOUT["grid_x"][col]
            hundred(c,f"comparison.{row}.group.{col}",x,y,n)
            c.text(f"comparison.{row}.risk.{col}",f"{n}/100（{n}%）",(x+13.05,y+33),size=10)
        c.text(f"comparison.{row}.relative","相对风险 ×2",(116,y+20),size=11.5)
        c.text(f"comparison.{row}.absolute",f"绝对增加 {delta} 个百分点",(116,y+8),size=10,color="accent")
        c.bracket(f"comparison.{row}.shared_denominator",11,80,y-3,color="muted")
    c.note("实心点表示假设的患病人数；不是实际疾病数据，也不能点名某个人的结局。",y=8)
    c.spec["risk_examples"]={"hypothetical":True,"period_years":10,"denominator":100,"pairs":[[1,2],[10,20]],"absolute_percentage_points":[1,10]}
    return c.result()


def main():
    from production_utils import export_figure
    result = build_figure()
    fig = result.figure
    OUT = Path(__file__).resolve().parent
    fig.savefig(OUT / "F22_relative_absolute_risk.pdf", metadata={"CreationDate": None, "ModDate": None})
    return export_figure(result, ROOT, OUT / "F22_relative_absolute_risk.pdf")


if __name__ == "__main__":
    main()
