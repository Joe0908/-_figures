"""Small physical-layout and geometry checks actually used by F01."""
from dataclasses import dataclass
from itertools import combinations
import math

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.text import Text
from matplotlib.path import Path

from book_style import STYLE, missing_glyphs


@dataclass(frozen=True)
class Box:
    x: float
    y: float
    w: float
    h: float

    @property
    def right(self):
        return self.x + self.w

    @property
    def top(self):
        return self.y + self.h

    @property
    def cx(self):
        return self.x + self.w / 2


@dataclass
class BuildResult:
    figure: Figure
    axes: object
    artists: dict
    spec: dict


def new_canvas(style=STYLE):
    fig = Figure(figsize=(style.width_mm / 25.4, style.height_mm / 25.4), dpi=style.dpi)
    FigureCanvasAgg(fig)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set(xlim=(0, style.width_mm), ylim=(0, style.height_mm), aspect="equal")
    ax.set_axis_off()
    return fig, ax


def register(artists, name, artist, role):
    if name in artists:
        raise ValueError(f"Duplicate semantic ID: {name}")
    artist.set_gid(name)
    artist.set_clip_on(False)
    artist._running_life_role = role
    artists[name] = artist
    return artist


def check_layout(result, style=STYLE):
    """Measure real rendered text and path borders, not just layout anchors.

    Interior overlap with a containing boundary/highlight is intentional.
    Closed boundaries are checked as strokes, not solid filled rectangles.
    This checker cannot establish scientific correctness or reader comprehension.
    """
    fig = result.figure
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    px_per_mm = fig.dpi / 25.4
    canvas = fig.bbox
    errors = []
    text_boxes = {}
    extents = {}
    for name, artist in result.artists.items():
        if not artist.get_visible():
            continue
        if artist.get_gid() != name:
            errors.append({"kind": "semantic_id_mismatch", "ids": [name]})
        box = artist.get_window_extent(renderer)
        if not all(math.isfinite(v) for v in box.extents):
            errors.append({"kind": "invalid_extent", "ids": [name]})
            continue
        extents[name] = [round(float(v / px_per_mm), 4) for v in box.extents]
        stroke = getattr(artist, "get_linewidth", lambda: 0)() * fig.dpi / 72 / 2
        check = box.padded(stroke)
        if check.x0 < canvas.x0 or check.y0 < canvas.y0 or check.x1 > canvas.x1 or check.y1 > canvas.y1:
            errors.append({"kind": "outside_canvas", "ids": [name]})
        if isinstance(artist, Text):
            text_boxes[name] = box
            if missing_glyphs(artist.get_text()):
                errors.append({"kind": "missing_glyph", "ids": [name]})
            if artist.get_fontsize() < 8.5:
                errors.append({"kind": "font_too_small", "ids": [name]})
            # 0.05 mm accounts for raster rounding at a 6 mm safety boundary.
            m = (style.margin_mm - 0.05) * px_per_mm
            if box.x0 < m or box.y0 < m or box.x1 > canvas.x1 - m or box.y1 > canvas.y1 - m:
                errors.append({"kind": "text_safety_margin", "ids": [name]})

    minimum_text_gap_mm = 0.8
    for (a, ba), (b, bb) in combinations(text_boxes.items(), 2):
        if ba.padded(minimum_text_gap_mm * px_per_mm / 2).overlaps(bb.padded(minimum_text_gap_mm * px_per_mm / 2)):
            errors.append({"kind": "text_collision_or_gap", "ids": [a, b]})
    for name, artist in result.artists.items():
        if not artist.get_visible() or not isinstance(artist, (Line2D, Patch)):
            continue
        if getattr(artist, "_running_life_role", "") == "region_fill":
            continue  # The region is intentionally behind the DNA rails.
        path = artist.get_path().transformed(artist.get_transform())
        # CLOSEPOLY's stored vertex is a dummy, often (0, 0). Normalize it
        # to the subpath origin so intersection checks do not invent a stroke
        # from an arrowhead to the canvas corner.
        if path.codes is not None and Path.CLOSEPOLY in path.codes:
            vertices = path.vertices.copy()
            origin = None
            for i, code in enumerate(path.codes):
                if code == Path.MOVETO:
                    origin = vertices[i].copy()
                elif code == Path.CLOSEPOLY and origin is not None:
                    vertices[i] = origin
            path = Path(vertices, path.codes)
        padding = 0.35 * px_per_mm + artist.get_linewidth() * fig.dpi / 72 / 2
        for text_name, box in text_boxes.items():
            if path.intersects_bbox(box.padded(padding), filled=False):
                errors.append({"kind": "stroke_crosses_text", "ids": [name, text_name]})
    return {
        "passed": not errors,
        "errors": errors,
        "artist_count": len(result.artists),
        "text_count": len(text_boxes),
        "minimum_text_gap_mm": minimum_text_gap_mm,
        "text_line_clearance_mm": 0.35,
        "extents_mm": extents,
        "limits": "Stroke/path and rendered text checks; intentional containment is allowed. Visual review is still required.",
    }
