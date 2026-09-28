"""Only F01's containment, conceptual zoom, packaging and sequence region."""
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Rectangle

from book_style import STYLE, font_properties
from layout_utils import register


def label(ax, artists, name, text, xy, *, size=None, ha="left", color=None, style=STYLE):
    item = ax.text(*xy, text, fontproperties=font_properties(size or style.label_pt),
                   ha=ha, va="center", linespacing=1.25, color=color or style.ink, zorder=10)
    return register(artists, name, item, "text")


def line(ax, artists, name, points, *, role="structure", color=None, width=None, dashed=False, style=STYLE):
    x, y = np.asarray(points).T
    item = Line2D(x, y, color=color or style.ink, linewidth=width or style.line_pt,
                  solid_capstyle="round", dash_capstyle="butt", zorder=4)
    if dashed:
        item.set_linestyle((0, (3, 2)))
    ax.add_line(item)
    return register(artists, name, item, role)


def boundary(ax, artists, name, center, size, *, style=STYLE):
    item = Ellipse(center, *size, edgecolor=style.muted, facecolor="none", linewidth=style.boundary_pt, zorder=1)
    ax.add_patch(item)
    return register(artists, name, item, "containment")


def zoom_frame(ax, artists, name, box, *, style=STYLE):
    item = FancyBboxPatch((box.x, box.y), box.w, box.h,
                         boxstyle=f"round,pad=0,rounding_size={style.radius_mm}",
                         edgecolor=style.muted, facecolor="none", linewidth=style.boundary_pt,
                         linestyle=(0, (3, 2)), zorder=3)
    ax.add_patch(item)
    return register(artists, name, item, "zoom")


def zoom_link(ax, artists, name, source_pair, target_pair, *, style=STYLE):
    return [line(ax, artists, f"{name}.{i}", [a, b], role="zoom", color=style.muted,
                 width=style.boundary_pt, dashed=True, style=style)
            for i, (a, b) in enumerate(zip(source_pair, target_pair))]


def bracket(ax, artists, name, x0, x1, y, *, depth=1.5, style=STYLE):
    return line(ax, artists, name, [(x0, y + depth), (x0, y), (x1, y), (x1, y + depth)],
                role="set_or_region", width=style.boundary_pt, style=style)


def organised_dna(ax, artists, name, box, *, detailed=False, muted=False, style=STYLE):
    """A continuous folded DNA trace; protein circles are explicitly labelled.

    This is a chromatin abstraction, not nucleosome stoichiometry or geometry.
    """
    t = np.linspace(0, 1, 500)
    x = box.x + box.w * t
    y = box.y + box.h / 2 + (box.h / 2 - style.node_padding_mm / 2) * np.sin(t * 6 * np.pi)
    if detailed:
        for i, fraction in enumerate((1 / 6, 1 / 2, 5 / 6)):
            c = Circle((box.x + box.w * fraction, box.y + box.h / 2), 2.1,
                       facecolor=style.region_fill, edgecolor=style.muted,
                       linewidth=style.boundary_pt, zorder=2)
            ax.add_patch(c)
            register(artists, f"{name}.protein.{i}", c, "protein")
    return line(ax, artists, f"{name}.dna", np.column_stack((x, y)),
                color=style.muted if muted else style.ink,
                width=style.boundary_pt if muted else style.emphasis_pt, style=style)


def dna_region(ax, artists, name, box, region_x, region_width, *, style=STYLE):
    if not box.x < region_x < region_x + region_width < box.right:
        raise ValueError("Gene must be an internal region of the continuous DNA segment")
    fill = Rectangle((region_x, box.y - 0.6), region_width, box.h + 1.2,
                     facecolor=style.region_fill, edgecolor=style.muted,
                     linewidth=style.boundary_pt, zorder=1)
    ax.add_patch(fill)
    register(artists, f"{name}.gene_region", fill, "region_fill")
    for rail, y in (("upper", box.top), ("lower", box.y)):
        line(ax, artists, f"{name}.backbone.{rail}", [(box.x, y), (box.right, y)], style=style)
        line(ax, artists, f"{name}.gene.{rail}", [(region_x, y), (region_x + region_width, y)],
             width=style.emphasis_pt, style=style)
        # Separate continuation dashes never turn into termination arrowheads.
        for side, x in (("left", box.x - 2.5), ("right", box.right + 1)):
            line(ax, artists, f"{name}.continuation.{rail}.{side}", [(x, y), (x + 1.5, y)],
                 width=style.boundary_pt, style=style)
    for i, x in enumerate(np.arange(box.x + 1.5, box.right, 2.3)):
        line(ax, artists, f"{name}.pair.{i:02d}", [(x, box.y), (x, box.top)],
             color=style.ink if region_x <= x <= region_x + region_width else style.muted,
             width=style.boundary_pt, style=style)
    return fill
