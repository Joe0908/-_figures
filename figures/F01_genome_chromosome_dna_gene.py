"""F01: genome, chromosome, DNA and gene. Run this file without arguments."""
from dataclasses import dataclass
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import matplotlib as mpl
from book_style import STYLE, PALETTE, COLOR_TUNING, mix_color, rc_settings
from matplotlib.lines import Line2D
from matplotlib.text import Text
from layout_utils import Box, BuildResult, new_canvas
from visual_grammar import boundary, bracket, dna_region, label, line, organised_dna, zoom_frame, zoom_link

OUT = Path(__file__).resolve().parent


@dataclass(frozen=True)
class F01Layout:
    cell_center: tuple = (32, 59)
    cell_size: tuple = (49, 45)
    nucleus_center: tuple = (33, 59)
    nucleus_size: tuple = (30, 28)
    chromosome_box: Box = Box(84, 62, 73, 15)
    chromosome_selection: Box = Box(35, 56, 12, 10)
    dna_selection: Box = Box(109, 60, 13, 18)
    dna_box: Box = Box(83, 33, 76, 4.5)
    gene_x_mm: float = 108
    gene_width_mm: float = 26
    gene_label_y_mm: float = 22


LAYOUT = F01Layout()


def apply_f01_colors(result, palette=PALETTE, tuning=COLOR_TUNING):
    """Color existing Artists only. No object, text or layout edits."""
    a = result.artists
    tint = lambda color, weight: mix_color(color, palette.background, weight)
    muted = tint(palette.neutral, tuning.muted_weight)
    dna_secondary = tint(palette.primary, tuning.secondary_dna_weight)
    result.figure.set_facecolor(palette.background)
    result.axes.set_facecolor(palette.background)
    for name, item in a.items():
        if isinstance(item, Text):
            item.set_color(palette.neutral)
        elif isinstance(item, Line2D):
            item.set_color(muted if item._running_life_role == "zoom" else palette.primary)

    a["F01.cell.boundary"].set_edgecolor(palette.secondary)
    a["F01.cell.boundary"].set_facecolor(tint(palette.secondary, tuning.cell_fill_weight))
    a["F01.nucleus.boundary"].set_edgecolor(tint(palette.primary, tuning.nucleus_edge_weight))
    a["F01.nucleus.boundary"].set_facecolor(tint(palette.primary, tuning.nucleus_fill_weight))
    for name, item in a.items():
        if name.startswith("F01.nucleus.other.") or ".pair." in name:
            item.set_color(dna_secondary)
        if item._running_life_role == "protein":
            item.set_edgecolor(palette.supplement)
            item.set_facecolor(tint(palette.supplement, tuning.protein_fill_weight))
        if item._running_life_role == "zoom" and not isinstance(item, Line2D):
            item.set_edgecolor(muted)

    for name in ("F01.genome.set_bracket", "F01.genome.label_leader"):
        a[name].set_color(palette.neutral)
    a["F01.organised_dna.leader"].set_color(palette.primary)
    a["F01.protein.leader"].set_color(palette.supplement)
    a["F01.scope.note"].set_color(muted)
    a["F01.zoom.chromosome.label"].set_color(muted)
    a["F01.dna.gene_region"].set_facecolor(tint(palette.accent, tuning.gene_fill_weight))
    a["F01.dna.gene_region"].set_edgecolor(palette.accent)
    for name in ("F01.dna.gene.upper", "F01.dna.gene.lower", "F01.gene.bracket", "F01.gene.label"):
        a[name].set_color(palette.accent)
    # Keep interior base-pair strokes in the same DNA color family. The warm
    # rectangle and overlaid rails mark a region, not a separate substance.
    result.spec["color_system"] = {
        "version": "1.0", "palette": palette.__dict__, "tuning": tuning.__dict__,
        "scope": "Color-only application; existing geometry, text and relationships preserved.",
    }
    return result


def build_figure(style=STYLE, layout=LAYOUT, palette=PALETTE, tuning=COLOR_TUNING):
    """Return a native Figure plus stable handles; do not write files here."""
    with mpl.rc_context(rc_settings()):
        fig, ax = new_canvas(style)
        a = {}
        left_x = style.margin_mm
        right_x = 72 + style.major_gap_mm
        label(ax, a, "F01.panel.set", "整套与所在位置", (left_x, 90.5), size=style.heading_pt, style=style)

        boundary(ax, a, "F01.cell.boundary", layout.cell_center, layout.cell_size, style=style)
        boundary(ax, a, "F01.nucleus.boundary", layout.nucleus_center, layout.nucleus_size, style=style)
        label(ax, a, "F01.cell.label", "有核细胞", (left_x + style.minor_gap_mm, 84), style=style)
        label(ax, a, "F01.nucleus.label", "细胞核", (32, 76), ha="center", size=style.secondary_pt, style=style)
        for i, b in enumerate((Box(22, 60, 9, 7), Box(22, 51, 10, 7), Box(33, 49, 9, 6))):
            organised_dna(ax, a, f"F01.nucleus.other.{i}", b, muted=True, style=style)
        organised_dna(ax, a, "F01.chromosome_example", Box(36, 57, 10, 8), style=style)
        zoom_frame(ax, a, "F01.zoom.chromosome.frame", layout.chromosome_selection, style=style)
        bracket(ax, a, "F01.genome.set_bracket", 19, 48, 43, style=style)
        line(ax, a, "F01.genome.label_leader", [(33.5, 43), (33.5, 33)], width=style.boundary_pt, style=style)
        label(ax, a, "F01.genome.label", "基因组", (33.5, 28.5), size=style.heading_pt, ha="center", style=style)
        label(ax, a, "F01.genome.definition", "整套DNA信息", (33.5, 22), ha="center", style=style)

        s = layout.chromosome_selection
        b = layout.chromosome_box
        zoom_link(ax, a, "F01.zoom.chromosome.link", [(s.right, s.top), (s.right, s.y)],
                  [(b.x, b.top), (b.x, b.y)], style=style)
        label(ax, a, "F01.zoom.chromosome.label", "放大", (64, 76), ha="center", size=style.note_pt, style=style)
        label(ax, a, "F01.chromosome.label", "一条染色体", (right_x, 90.5), size=style.heading_pt, style=style)
        label(ax, a, "F01.chromosome.definition", "长DNA与相关蛋白组织在一起", (right_x, 84.5), size=style.secondary_pt, style=style)
        organised_dna(ax, a, "F01.organised_chromosome", b, detailed=True, style=style)
        label(ax, a, "F01.organised_dna.label", "长DNA", (92, 55.5), ha="center", size=style.note_pt, style=style)
        line(ax, a, "F01.organised_dna.leader", [(100, 63.3), (92, 59)], width=style.boundary_pt, color=style.muted, style=style)
        label(ax, a, "F01.protein.label", "相关蛋白", (151, 55.5), ha="center", size=style.note_pt, style=style)
        line(ax, a, "F01.protein.leader", [(b.x + b.w * 5 / 6, b.y + b.h / 2), (151, 59)],
             width=style.boundary_pt, color=style.muted, style=style)
        zoom_frame(ax, a, "F01.zoom.dna.frame", layout.dna_selection, style=style)
        q = layout.dna_selection
        d = layout.dna_box
        zoom_link(ax, a, "F01.zoom.dna.link", [(q.x, q.y), (q.right, q.y)],
                  [(d.x, d.top + style.label_gap_mm), (d.right, d.top + style.label_gap_mm)], style=style)
        label(ax, a, "F01.dna.label", "DNA的一段", (d.cx, 45), size=style.label_pt, ha="center", style=style)
        dna_region(ax, a, "F01.dna", d, layout.gene_x_mm, layout.gene_width_mm, style=style)
        gx, gw = layout.gene_x_mm, layout.gene_width_mm
        bracket(ax, a, "F01.gene.bracket", gx, gx + gw, d.y - style.minor_gap_mm, style=style)
        label(ax, a, "F01.gene.label", "基因 HBB", (gx + gw / 2, layout.gene_label_y_mm),
              ha="center", size=style.heading_pt, style=style)
        label(ax, a, "F01.gene.definition", "DNA上的一个区域", (gx + gw / 2, 16), ha="center", style=style)
        label(ax, a, "F01.scope.note", "示意：聚焦核内DNA的组织；染色体只画部分。放大与尺寸均非真实比例。",
              (left_x, 8), size=style.note_pt, color=style.muted, style=style)
        result = BuildResult(fig, ax, a, {
            "figure_id": "F01",
            "title": "基因组 染色体 DNA 和基因的关系",
            "source_paragraphs": ["P0034–P0042", "P0044", "P0053–P0064"],
            "quantitative": False,
            "relationships": [
                {"kind": "containment", "source": "F01.cell.boundary", "target": "F01.nucleus.boundary", "evidence": "P0034–P0036"},
                {"kind": "collection", "source": "F01.genome.set_bracket", "target": "F01.genome.label", "evidence": "P0041–P0042"},
                {"kind": "conceptual_zoom", "source": "F01.chromosome_example.dna", "target": "F01.organised_chromosome.dna", "evidence": "P0037–P0039"},
                {"kind": "organisation", "source": "F01.organised_chromosome.dna", "target": "F01.chromosome.label", "evidence": "P0036–P0038,P0042"},
                {"kind": "conceptual_zoom", "source": "F01.zoom.dna.frame", "target": "F01.dna.backbone.upper", "evidence": "P0039–P0040"},
                {"kind": "region_on_sequence", "source": "F01.dna.gene_region", "target": "F01.dna.backbone.upper", "evidence": "P0039–P0040"},
            ],
            "layout": {k: str(v) for k, v in layout.__dict__.items()},
            "limits": "Conceptual, not to scale; only some nuclear chromosomes shown; no actual HBB sequence or base-pair count represented.",
        })
        return apply_f01_colors(result, palette, tuning)


def main():
    from export_utils import export_figure, preflight
    with mpl.rc_context(rc_settings()):
        result = build_figure()
        report = preflight(result)
        fig = result.figure
        # Explicit, adjacent, static PDF name for Tavotto's figure contract.
        fig.savefig(OUT / "F01_genome_chromosome_dna_gene.pdf", metadata={"CreationDate": None, "ModDate": None})
        return export_figure(result, report, ROOT, OUT / "F01_genome_chromosome_dna_gene.pdf")


if __name__ == "__main__":
    main()
