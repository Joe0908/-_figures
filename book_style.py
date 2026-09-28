"""Shared book tokens used by F01. All geometry is in millimetres."""
from dataclasses import dataclass
from pathlib import Path

from matplotlib import font_manager, ft2font
from matplotlib.colors import to_rgb, to_hex


@dataclass(frozen=True)
class BookPalette:
    name: str
    primary: str
    secondary: str
    accent: str
    supplement: str
    neutral: str
    background: str = "#FFFFFF"


PALETTES = {
    "sea_copper": BookPalette("海青与铜", "#2F6174", "#6B8B7A", "#A6633F", "#827592", "#26353E"),
    "slate_sand": BookPalette("石蓝与砂金", "#425B76", "#66877E", "#946D2E", "#907A85", "#2D3540"),
    "pine_clay": BookPalette("松绿与绛砂", "#416F67", "#6D8095", "#A45D59", "#8D865D", "#2F3B38"),
}
PALETTE = PALETTES["sea_copper"]


@dataclass(frozen=True)
class ColorTuning:
    # Opaque sRGB mixtures; these are pigment weights, not Artist alpha.
    cell_fill_weight: float = 0.08
    nucleus_fill_weight: float = 0.10
    nucleus_edge_weight: float = 0.76
    secondary_dna_weight: float = 0.75
    protein_fill_weight: float = 0.16
    gene_fill_weight: float = 0.18
    muted_weight: float = 0.70


COLOR_TUNING = ColorTuning()


def mix_color(foreground, background, weight):
    """Return an opaque color; never alter geometry or transparency."""
    if not 0 <= weight <= 1:
        raise ValueError("Color weight must lie between 0 and 1")
    return to_hex(tuple(weight * a + (1 - weight) * b
                        for a, b in zip(to_rgb(foreground), to_rgb(background))))


@dataclass(frozen=True)
class BookStyle:
    width_mm: float = 170
    height_mm: float = 100
    dpi: int = 600
    margin_mm: float = 6
    label_pt: float = 9.5
    secondary_pt: float = 9
    note_pt: float = 8.5
    heading_pt: float = 11.5
    line_pt: float = 1.1
    boundary_pt: float = 0.8
    emphasis_pt: float = 1.5
    node_padding_mm: float = 2.2
    label_gap_mm: float = 2
    major_gap_mm: float = 8
    minor_gap_mm: float = 5
    radius_mm: float = 1.2
    ink: str = PALETTE.neutral
    muted: str = mix_color(PALETTE.neutral, PALETTE.background, COLOR_TUNING.muted_weight)
    border: str = mix_color(PALETTE.primary, PALETTE.background, COLOR_TUNING.nucleus_edge_weight)
    panel: str = mix_color(PALETTE.secondary, PALETTE.background, COLOR_TUNING.cell_fill_weight)
    region_fill: str = mix_color(PALETTE.accent, PALETTE.background, COLOR_TUNING.gene_fill_weight)


STYLE = BookStyle()
FONT_PATH = Path(__file__).resolve().parent / "fonts" / "NotoSansSC-Regular.ttf"


def font_properties(size=STYLE.label_pt):
    if not FONT_PATH.is_file():
        raise FileNotFoundError(f"Required bundled font is missing: {FONT_PATH}")
    return font_manager.FontProperties(fname=FONT_PATH, size=size)


def rc_settings():
    """Return a local rc_context; importing this module changes no style."""
    prop = font_properties()
    font_manager.fontManager.addfont(str(FONT_PATH))
    return {
        "font.family": [prop.get_name(), "DejaVu Sans"],
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "svg.hashsalt": "running-life-f01-v1",
        "savefig.facecolor": "auto",
        "figure.facecolor": PALETTE.background,
        "axes.unicode_minus": False,
    }


def missing_glyphs(text):
    cmap = ft2font.FT2Font(str(FONT_PATH)).get_charmap()
    return sorted({c for c in text if not c.isspace() and ord(c) not in cmap})
