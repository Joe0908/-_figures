"""F30: 从工具工作到患者持续获益. Native semantic Artists; importing writes no files."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from shared_shapes import Drawing


LAYOUT={"height":140,"columns":(8,62,116),"rows":(85,42),"card_w":46,"card_h":37}
GATES=[
    ("1  正确递送","工具到对的\n细胞了吗？","测位置与细胞身份"),
    ("2  分子改变","目标分子\n真的改变了吗？","测预期与非预期变化"),
    ("3  细胞功能","细胞真的\n重新工作了吗？","测功能与行为"),
    ("4  关键细胞覆盖","多少正确细胞\n在什么位置恢复？","测数量、位置与能力"),
    ("5  组织功能","整体工作能力\n够了吗？","测组织功能与阈值"),
    ("6  患者持续获益","症状、负担和生活\n能持续改善吗？","测患者结局与持续性"),
]


def build_figure():
    c=Drawing("F30",height=LAYOUT["height"])
    c.heading("title","六道门，各自都要拿出证据",(6,130.5))
    for i,(heading,question,evidence) in enumerate(GATES):
        x=LAYOUT["columns"][i%3]; y=LAYOUT["rows"][i//3]
        c.rect(f"gate.{i+1}.boundary",(x,y),46,37,color="primary",weight=.06)
        c.text(f"gate.{i+1}.heading",heading,(x+4,y+29),ha="left",size=9.5)
        c.text(f"gate.{i+1}.question",question,(x+23,y+19),size=9.5)
        c.circle(f"gate.{i+1}.observation_port",(x+4,y+5),1.2,color="supplement",fill="supplement")
        c.text(f"gate.{i+1}.evidence",evidence,(x+8,y+5),ha="left",size=8.5,color="supplement")
    for row,y in enumerate(LAYOUT["rows"]):
        for col in [0,1]:
            c.edge(f"reading_order.{row}.{col}",(LAYOUT["columns"][col]+46,y+19),(LAYOUT["columns"][col+1],y+19),kind="order",source=f"gate.{row*3+col+1}",target=f"gate.{row*3+col+2}")
    c.rect("duration.rail",(6,24),158,10,color="secondary",weight=.09)
    c.text("duration.question","每道门都问时间：疾病需要改变多久，获益是否持续？",(85,29),size=9)
    c.rect("safety.rail",(6,12),158,10,color="accent",weight=.08)
    c.text("safety.question","每道门都看安全：非预期改变、身体负担与长期风险",(85,17),size=9)
    c.note("比例要说明分母与测量对象；前一门通过，不保证后一门通过。连线仅表示阅读顺序。",y=8)
    c.spec["independent_gates"]=["correct_delivery","molecular_change","cell_function","critical_cell_coverage","tissue_function","sustained_patient_benefit"]
    return c.result()


def main():
    from production_utils import export_figure
    result = build_figure()
    fig = result.figure
    OUT = Path(__file__).resolve().parent
    fig.savefig(OUT / "F30_six_gates_patient_benefit.pdf", metadata={"CreationDate": None, "ModDate": None})
    return export_figure(result, ROOT, OUT / "F30_six_gates_patient_benefit.pdf")


if __name__ == "__main__":
    main()
