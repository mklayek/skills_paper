"""Color palettes for explain-slide-pptx.

Each palette sets every color on a slide:
  frame     page border            title_hl  highlighted word in the title
  intro     intro strip color      panels    one color per panel (outline, pill, key words, bullets)
  examples  Example-box color per panel (keep it different from that panel's color)
  text      body text color        subtitle  subtitle / credit gray
  fill      "outline" = white boxes, "tint" = boxes filled with a light tint of their color
Add a new palette by copying one entry. Keep panel colors dark enough for white pill text.
"""

PALETTES = {
    "classic": {"frame": "0B2A55", "title_hl": "B91C1C", "intro": "0B2A55",
                "panels": ["1D4ED8", "B91C1C", "15803D", "6D28D9"],
                "examples": ["C2410C", "C2410C", "6D28D9", "0E7490"],
                "text": "111111", "subtitle": "4B5563", "fill": "outline"},
    "ocean": {"frame": "0B3C5D", "title_hl": "0E7490", "intro": "0B3C5D",
              "panels": ["0E7490", "1D4ED8", "0369A1", "4338CA"],
              "examples": ["C2410C", "B45309", "BE185D", "C2410C"],
              "text": "0F172A", "subtitle": "475569", "fill": "outline"},
    "sunset": {"frame": "7C2D12", "title_hl": "C2410C", "intro": "7C2D12",
               "panels": ["C2410C", "BE185D", "B45309", "9F1239"],
               "examples": ["1D4ED8", "0E7490", "4338CA", "15803D"],
               "text": "1C1917", "subtitle": "57534E", "fill": "outline"},
    "forest": {"frame": "14532D", "title_hl": "15803D", "intro": "14532D",
               "panels": ["15803D", "0F766E", "4D7C0F", "166534"],
               "examples": ["B45309", "C2410C", "9F1239", "1D4ED8"],
               "text": "14201A", "subtitle": "4B5563", "fill": "outline"},
    "berry": {"frame": "4C1D95", "title_hl": "BE185D", "intro": "4C1D95",
              "panels": ["6D28D9", "BE185D", "A21CAF", "4338CA"],
              "examples": ["0E7490", "15803D", "C2410C", "0E7490"],
              "text": "1E1B2E", "subtitle": "5B5670", "fill": "outline"},
    "slate": {"frame": "1F2937", "title_hl": "0F766E", "intro": "1F2937",
              "panels": ["334155", "0F766E", "9A3412", "1E40AF"],
              "examples": ["B45309", "9F1239", "0E7490", "15803D"],
              "text": "111827", "subtitle": "4B5563", "fill": "outline"},
    # tinted versions: same colors, boxes filled with a light tint
    "classic-tint": {"base": "classic", "fill": "tint"},
    "ocean-tint": {"base": "ocean", "fill": "tint"},
    "sunset-tint": {"base": "sunset", "fill": "tint"},
    "forest-tint": {"base": "forest", "fill": "tint"},
    "berry-tint": {"base": "berry", "fill": "tint"},
    # dark-text variant: body text in deep navy instead of black
    "classic-navytext": {"base": "classic", "text": "0B2A55"},
}

CYCLE = ["classic", "ocean", "sunset", "forest", "berry", "slate"]


def get(name):
    """Resolve a palette name (following "base") into a full dict."""
    p = dict(PALETTES[name])
    if "base" in p:
        full = get(p.pop("base"))
        full.update(p)
        return full
    return p


def tint(hex6, amount=0.92):
    """Light tint of a color: amount 0 = the color, 1 = white."""
    r, g, b = (int(hex6[i:i + 2], 16) for i in (0, 2, 4))
    mix = lambda c: round(c + (255 - c) * amount)
    return "%02X%02X%02X" % (mix(r), mix(g), mix(b))
