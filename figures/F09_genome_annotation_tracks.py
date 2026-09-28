"""F09: genome_annotation_tracks. Coordinates in mm; all objects remain editable."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shared_shapes import Drawing
from production_utils import export_figure
OUT = Path(__file__).resolve().parent

def build_figure():
    c=Drawing("F09",126)
    c.heading("heading","沿同一段 DNA，可从不同角度标注",(6,116))
    c.dna("dna",49,96,110)
    labels=[('蛋白质编码',[(68,9),(100,10)],'primary'),
            ('基因内部非编码',[(55,13),(77,23),(110,11)],'secondary'),
            ('非编码 RNA',[(130,24)],'secondary'),
            ('调控作用',[(52,15),(114,14)],'accent'),
            ('重复／结构',[(87,14),(133,21)],'supplement'),
            ('作用仍待研究',[(72,14),(120,11)],'muted')]
    for i,(label,regions,col) in enumerate(labels):
        y=82-i*11
        c.text(f"track.label.{i}",label,(6,y+2.5),ha="left",size=8.5)
        c.line(f"track.baseline.{i}",[(49,y+2.5),(159,y+2.5)],width=.6,color="muted")
        for j,(x,w) in enumerate(regions):
            c.rect(f"track.region.{i}.{j}",(x,y),w,5,color=col,weight=.3,radius=0)
    c.text("meaning","注释可以交叠；非编码不等于没有作用，也不等于每段都有已知功能。",(85,18),size=8.5)
    c.note("抽象注释示意，不对应真实位点；长度、间距与各类占比均不按比例。",y=8)
    return c.result()


def main():
    result=build_figure()
    fig=result.figure
    fig.savefig(OUT / "F09_genome_annotation_tracks.pdf", metadata={"CreationDate":None,"ModDate":None})
    return export_figure(result,ROOT,OUT / "F09_genome_annotation_tracks.pdf")

if __name__=="__main__":
    main()
