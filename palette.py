"""One palette entry point for the whole book; matches accepted F01."""
from book_style import PALETTE, PALETTES, COLOR_TUNING, mix_color

PRIMARY = PALETTE.primary
SECONDARY = PALETTE.secondary
ACCENT = PALETTE.accent
SUPPLEMENT = PALETTE.supplement
INK = PALETTE.neutral
BACKGROUND = PALETTE.background
MUTED = mix_color(INK, BACKGROUND, .70)


def tint(color, weight=.12):
    return mix_color(color, BACKGROUND, weight)


ROLES = {"primary": PRIMARY, "secondary": SECONDARY, "accent": ACCENT,
         "supplement": SUPPLEMENT, "ink": INK, "muted": MUTED,
         "background": BACKGROUND}


def resolve(color):
    return ROLES.get(color, color)
