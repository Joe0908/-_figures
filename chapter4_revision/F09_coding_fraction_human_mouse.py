"""Human and mouse coding fraction, using the Running Life palette and type."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from book_style import STYLE, rc_settings, font_properties, PALETTE, mix_color
import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import Rectangle

OUT = Path(__file__).resolve().parent / "outputs"
W, H = 170, 88

def make():
    with mpl.rc_context(rc_settings()):
        fig = Figure(figsize=(W / 25.4, H / 25.4), dpi=STYLE.dpi)
        FigureCanvasAgg(fig)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set(xlim=(0, W), ylim=(0, H), aspect="equal")
        ax.set_axis_off()
        ink, blue, copper = PALETTE.neutral, PALETTE.primary, PALETTE.accent
        pale = mix_color(blue, "white", .09)
        def t(x,y,s,size=9.5,ha="left",color=ink):
            ax.text(x,y,s,fontproperties=font_properties(size),ha=ha,va="center",color=color)
        t(7,77,"蛋白质编码序列只占很小一部分",11.5)
        x0, width, height = 29, 128, 8
        for y, species in [(56,"人"),(35,"小鼠")]:
            t(7,y+4,species,10)
            ax.add_patch(Rectangle((x0,y),width,height,facecolor=pale,edgecolor=blue,linewidth=.8))
            ax.add_patch(Rectangle((x0,y),width*.015,height,facecolor=copper,edgecolor=copper,linewidth=.7))
            ax.plot([x0+width*.015/2,x0+width*.015/2],[y,y-3.3],color=copper,lw=.8)
            t(x0+3,y-7,"约 1.5% 编码蛋白质",8.5,color=copper)
            t(158,y+4,"其余约 98.5%",9,ha="right")
        t(7,10,"每条长条代表一套核基因组；比例为约数，口径限于直接决定氨基酸顺序的序列。",8.5,color=STYLE.muted)
        for ext in ("png","pdf","svg"):
            p=OUT/ext/f"F09_coding_fraction_human_mouse.{ext}"
            p.parent.mkdir(parents=True,exist_ok=True)
            fig.savefig(p,dpi=STYLE.dpi,metadata={"Date":None} if ext=="svg" else None)
        return fig

if __name__=="__main__": make()
