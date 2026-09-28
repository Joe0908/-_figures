"""F08: propagation_and_buffering. Coordinates in mm; all objects remain editable."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shared_shapes import Drawing
from production_utils import export_figure
OUT = Path(__file__).resolve().parent

def build_figure():
    c=Drawing("F08",140)
    xs=[18,49,83,116,148]
    heads=['DNA','RNA','蛋白质及\n分子作用','细胞','组织与\n表现']
    for i,(x,label) in enumerate(zip(xs,heads)):
        c.text(f"head.{i}",label,(x,128),size=10.5)
    rows=[(106,['序列改变','密码子变','氨基酸未变',None,None]),
          (81,['序列改变','密码子变','氨基酸变\n功能仍保留',None,None]),
          (56,['序列改变','产物改变','作用改变','其他途径\n补偿',None]),
          (31,['序列改变','产物改变','作用改变','功能改变','功能余量\n仍足够'])]
    for r,(y,labels) in enumerate(rows):
        last=max(i for i,v in enumerate(labels) if v)
        for i,label in enumerate(labels):
            if label:
                c.node(f"r{r}.n{i}",label,(xs[i],y),w=24 if i!=2 else 28,h=16,color="secondary" if i==last else "primary",size=8.5)
                if i:
                    c.edge(f"r{r}.e{i}",(xs[i-1]+(14 if i==3 else 12)+1,y),(xs[i]-(14 if i==2 else 12)-1,y),kind="template" if i==1 or (i==2 and r<2) else "conditional")
    c.note("四行是独立示例。传播还取决于基因是否表达，以及氧、浓度、持续时间等条件。",y=15)
    c.note("同义变化在此仅指氨基酸顺序不变；缓冲不等于 DNA 恢复。线宽不表示效应大小。",y=8,name="scope.note2")
    return c.result()


def main():
    result=build_figure()
    fig=result.figure
    fig.savefig(OUT / "F08_propagation_and_buffering.pdf", metadata={"CreationDate":None,"ModDate":None})
    return export_figure(result,ROOT,OUT / "F08_propagation_and_buffering.pdf")

if __name__=="__main__":
    main()
