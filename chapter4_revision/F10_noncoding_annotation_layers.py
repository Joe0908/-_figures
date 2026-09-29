"""Noncoding genome annotations as overlapping dimensions, not a pie chart."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from book_style import STYLE, rc_settings, font_properties, PALETTE, mix_color
import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import FancyBboxPatch

OUT = Path(__file__).resolve().parent / "outputs"
W,H=170,106

def make():
    with mpl.rc_context(rc_settings()):
        fig=Figure(figsize=(W/25.4,H/25.4),dpi=STYLE.dpi);FigureCanvasAgg(fig)
        ax=fig.add_axes([0,0,1,1]);ax.set(xlim=(0,W),ylim=(0,H),aspect="equal");ax.set_axis_off()
        P=PALETTE
        def t(x,y,s,size=9.5,ha="left",color=P.neutral):
            ax.text(x,y,s,fontproperties=font_properties(size),ha=ha,va="center",color=color)
        def box(x,y,w,h,c,txt,fill=.10):
            ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=1.2",linewidth=.8,
                         edgecolor=c,facecolor=mix_color(c,"white",fill)))
            t(x+w/2,y+h/2,txt,9,ha="center")
        t(7,96,"看非编码 DNA：位置、来源与作用是三种不同的提问",11.5)
        t(7,79,"按位置",9.5,color=P.primary)
        box(36,72,54,14,P.primary,"基因内部：内含子等")
        box(96,72,64,14,P.primary,"基因之间的区域")
        t(7,56,"按来源",9.5,color=P.secondary)
        box(36,49,124,14,P.secondary,"重复序列；其中许多来自转座元件")
        t(98,44,"经典方法可识别的转座元件来源序列约占全基因组 45%",8.5,ha="center",color=STYLE.muted)
        t(7,33,"按作用",9.5,color=P.accent)
        box(36,26,55,14,P.accent,"调控区域")
        box(97,26,63,14,P.supplement,"产生非编码 RNA 的区域")
        t(7,13,"同一段 DNA 可以同时属于不同注释；框的面积与位置不代表全基因组比例。",8.5,color=STYLE.muted)
        for ext in ("png","pdf","svg"):
            p=OUT/ext/f"F10_noncoding_annotation_layers.{ext}"
            p.parent.mkdir(parents=True,exist_ok=True)
            fig.savefig(p,dpi=STYLE.dpi,metadata={"Date":None} if ext=="svg" else None)
        return fig

if __name__=="__main__":make()
