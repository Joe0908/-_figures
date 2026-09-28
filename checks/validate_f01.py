"""Run meaningful positive/negative layout and editability checks, without saving mutations."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "figures"))

from matplotlib.lines import Line2D
from matplotlib.text import Text
from F01_genome_chromosome_dna_gene import build_figure
from layout_utils import check_layout, register
from export_utils import check_exports, STEM


def rejected(mutate, kind):
    b = build_figure()
    mutate(b)
    q = check_layout(b)
    assert any(e["kind"] == kind for e in q["errors"]), (kind, q)
    return kind


def main():
    b = build_figure()
    report = check_layout(b)
    assert report["passed"], report["errors"]
    assert not b.axes.images, "Core figure must not be an image"
    assert len(set(a.get_gid() for a in b.artists.values())) == len(b.artists)
    region = b.artists["F01.dna.gene_region"]
    for rail in ("upper", "lower"):
        x = b.artists[f"F01.dna.backbone.{rail}"].get_xdata()
        assert min(x) < region.get_x() < region.get_x() + region.get_width() < max(x)
    assert isinstance(b.artists["F01.gene.label"], Text)
    position = b.artists["F01.gene.label"].get_position()
    b.artists["F01.gene.label"].set_position((position[0] + 2, position[1]))
    assert check_layout(b)["passed"], "A 2 mm label micro-adjustment should remain editable"
    assert build_figure().artists["F01.gene.label"].get_position() == position
    negatives = [
        rejected(lambda v: v.artists["F01.gene.label"].set_position((-10, 20)), "outside_canvas"),
        rejected(lambda v: v.artists["F01.gene.label"].set_position(v.artists["F01.gene.definition"].get_position()), "text_collision_or_gap"),
        rejected(lambda v: v.artists["F01.gene.label"].set_fontsize(6), "font_too_small"),
        rejected(lambda v: v.artists["F01.gene.label"].set_gid("wrong"), "semantic_id_mismatch"),
    ]

    def crossing(v):
        x, y = v.artists["F01.gene.label"].get_position()
        line = Line2D([x - 20, x + 20], [y, y])
        v.axes.add_line(line)
        register(v.artists, "test.crossing", line, "structure")

    negatives.append(rejected(crossing, "stroke_crosses_text"))
    try:
        register(b.artists, "F01.gene.label", Text(), "text")
    except ValueError:
        negatives.append("duplicate_semantic_id")
    else:
        raise AssertionError("Duplicate semantic ID was accepted")
    paths = {fmt: ROOT / "outputs" / fmt / f"{STEM}.{fmt}" for fmt in ("png", "pdf", "svg")}
    exports = check_exports(paths, report["text_count"])
    result = {"baseline_passed": True, "native_edit_smoke_test": True,
              "negative_cases_rejected": negatives, "export_checks": exports,
              "not_a_reader_or_print_test": True}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == "__main__":
    main()
