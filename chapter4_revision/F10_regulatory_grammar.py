"""Running Life F10: recognizable DNA elements and their arrangement.

The figure illustrates a possible change in regulatory opportunity, not a
deterministic sequence-to-expression rule. Chromatin and 3D contact are
deliberately outside the sequence panel.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from book_style import STYLE, PALETTE, font_properties, mix_color, rc_settings

import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import FancyBboxPatch

OUT = Path(__file__).resolve().parent / "outputs"
W, H = 170, 92


def make():
    with mpl.rc_context(rc_settings()):
        fig = Figure(figsize=(W / 25.4, H / 25.4), dpi=STYLE.dpi)
        FigureCanvasAgg(fig)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set(xlim=(0, W), ylim=(0, H), aspect="equal")
        ax.set_axis_off()
        p = PALETTE

        def label(x, y, s, size=9.5, ha="left", color=p.neutral):
            ax.text(x, y, s, fontproperties=font_properties(size),
                    ha=ha, va="center", color=color)

        def site(x, y, letter, color):
            ax.add_patch(FancyBboxPatch(
                (x - 6, y - 5), 12, 10,
                boxstyle="round,pad=0,rounding_size=1.2",
                linewidth=.9, edgecolor=color,
                facecolor=mix_color(color, "white", .15)))
            label(x, y, letter, 9, "center", color)

        label(7, 82, "相同的可识别元件，排列和间距可以不同", 11.5)
        label(7, 64, "排列一", 9.5, color=p.primary)
        label(7, 39, "排列二", 9.5, color=p.primary)

        for y in (64, 39):
            ax.plot([32, 131], [y, y], color=p.neutral, lw=1.1,
                    solid_capstyle="round", zorder=1)
            ax.plot([29, 31], [y, y], color=p.muted if hasattr(p, "muted") else STYLE.muted, lw=.8)
            ax.plot([132, 134], [y, y], color=STYLE.muted, lw=.8)
        for x, y, letter, color in (
            (46, 64, "A", p.primary), (75, 64, "B", p.accent),
            (104, 64, "C", p.secondary),
            (46, 39, "A", p.primary), (89, 39, "C", p.secondary),
            (118, 39, "B", p.accent)):
            site(x, y, letter, color)

        label(139, 64, "一种组合", 9, color=p.neutral)
        label(139, 39, "另一种组合", 9, color=p.neutral)
        label(7, 22, "这些组合可能改变调控蛋白共同作用的机会，进而改变转录输出。", 9)
        label(7, 10, "示意图：并非固定的开关；实际结果还取决于细胞提供的阅读环境。",
              8.5, color=STYLE.muted)

        for ext in ("png", "pdf", "svg"):
            path = OUT / ext / f"F10_regulatory_grammar.{ext}"
            path.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(path, dpi=STYLE.dpi,
                        metadata={"Date": None} if ext == "svg" else None)
        return fig


if __name__ == "__main__":
    make()