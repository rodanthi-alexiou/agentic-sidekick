#!/usr/bin/env python3
"""
Cathode Atlas — retro-technical partner-journey banner.
Renders a single-page CRT/oscilloscope-style banner of the 5-stage delivery
sequence (Base -> Standardize -> Plan -> Land -> Deploy) with the PLAN stage live.

Design philosophy: images/cathode-atlas-philosophy.md
Output: images/story-journey-banner-retro.png
"""
from __future__ import annotations
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

# ----------------------------------------------------------------------------- paths
FONTS = Path(r"c:\Users\ralexiou\.copilot\installed-plugins\anthropic-agent-skills"
             r"\document-skills\skills\canvas-design\canvas-fonts")
OUT = Path(__file__).resolve().parents[1] / "images" / "story-journey-banner-retro.png"

# ----------------------------------------------------------------------------- canvas
SS = 2                      # supersample factor
W, H = 2400, 940           # final size
CW, CH = W * SS, H * SS     # working size

# ----------------------------------------------------------------------------- palette
BG          = (8, 14, 16)        # near-black cool ground
GRID_FINE   = (18, 32, 34)
GRID_BOLD   = (26, 48, 50)
PHOS        = (63, 182, 168)     # phosphor green-teal (structure)
PHOS_BRIGHT = (125, 243, 209)    # bright phosphor
PHOS_DIM    = (46, 96, 92)       # dim structure
AMBER       = (242, 180, 65)     # live / current reading (rationed)
AMBER_BRT   = (255, 209, 122)
INK         = (212, 234, 228)    # near-white text
MUTE        = (74, 102, 110)     # metadata


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / name), size * SS)


# fonts
f_pixel_xl = font("PixelifySans-Medium.ttf", 58)   # big station numerals
f_pixel_lg = font("PixelifySans-Medium.ttf", 74)
f_silk_s   = font("Silkscreen-Regular.ttf", 13)    # micro tags
f_silk_xs  = font("Silkscreen-Regular.ttf", 11)
f_mono_b   = font("JetBrainsMono-Bold.ttf", 26)    # station names
f_mono_bn  = font("JetBrainsMono-Bold.ttf", 22)
f_mono     = font("JetBrainsMono-Regular.ttf", 17) # sublabels / logs
f_mono_s   = font("JetBrainsMono-Regular.ttf", 14)
f_tek      = font("Tektur-Medium.ttf", 30)         # title
f_tek_s    = font("Tektur-Regular.ttf", 16)


def s(v: float) -> int:
    """scale a final-resolution coordinate to working resolution."""
    return int(round(v * SS))


# ============================================================================= layers
base = Image.new("RGB", (CW, CH), BG)
glow = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))   # bloom layer
d = ImageDraw.Draw(base, "RGBA")
dg = ImageDraw.Draw(glow, "RGBA")


def text_c(draw, xy, txt, fnt, fill, anchor="mm", spacing=0):
    draw.text((s(xy[0]), s(xy[1])), txt, font=fnt, fill=fill, anchor=anchor)


# ----------------------------------------------------------------------------- grid
def draw_grid():
    step = 40
    for x in range(0, W + 1, step):
        c = GRID_BOLD if x % 200 == 0 else GRID_FINE
        d.line([(s(x), 0), (s(x), CH)], fill=c, width=1)
    for y in range(0, H + 1, step):
        c = GRID_BOLD if y % 200 == 0 else GRID_FINE
        d.line([(0, s(y)), (CW, s(y))], fill=c, width=1)


draw_grid()

# ----------------------------------------------------------------------------- frame
MARGIN = 64
fx0, fy0, fx1, fy1 = MARGIN, MARGIN, W - MARGIN, H - MARGIN
d.rectangle([s(fx0), s(fy0), s(fx1), s(fy1)], outline=PHOS_DIM, width=s(1.5))
inset = 8
d.rectangle([s(fx0 + inset), s(fy0 + inset), s(fx1 - inset), s(fy1 - inset)],
            outline=GRID_BOLD, width=1)

# corner registration crosses
def reg_cross(cx, cy, r=14):
    d.line([(s(cx - r), s(cy)), (s(cx + r), s(cy))], fill=PHOS, width=s(1.5))
    d.line([(s(cx), s(cy - r)), (s(cx), s(cy + r))], fill=PHOS, width=s(1.5))
for (cx, cy) in [(fx0, fy0), (fx1, fy0), (fx0, fy1), (fx1, fy1)]:
    reg_cross(cx, cy)

# ----------------------------------------------------------------------------- top rail
top_y = fy0 + 46
text_c(d, (fx0 + 30, top_y), "AI\u00B7WORKLOAD\u00B7PLANNER", f_silk_s, PHOS, anchor="lm")
# right side: version + live cursor
rt = "PARTNER JOURNEY \u00B7 v2026.06"
text_c(d, (fx1 - 64, top_y), rt, f_silk_s, MUTE, anchor="rm")
# blinking cursor block
cur_w, cur_h = 22, 24
d.rectangle([s(fx1 - 52), s(top_y - cur_h / 2), s(fx1 - 52 + cur_w), s(top_y + cur_h / 2)],
            fill=PHOS_BRIGHT)
dg.rectangle([s(fx1 - 52), s(top_y - cur_h / 2), s(fx1 - 52 + cur_w), s(top_y + cur_h / 2)],
             fill=(125, 243, 209, 180))
# rule under top rail
rule_y = top_y + 34
d.line([(s(fx0 + 22), s(rule_y)), (s(fx1 - 22), s(rule_y))], fill=PHOS_DIM, width=1)
# tiny tick marks on the rule
for i in range(0, 41):
    x = fx0 + 22 + (fx1 - fx0 - 44) * i / 40
    h = 7 if i % 5 == 0 else 4
    d.line([(s(x), s(rule_y)), (s(x), s(rule_y + h))], fill=GRID_BOLD, width=1)

# ----------------------------------------------------------------------------- title
title_y = rule_y + 60
text_c(d, (W / 2, title_y), "THE  PARTNER  JOURNEY", f_tek, INK, anchor="mm")
text_c(d, (W / 2, title_y + 34), "end-to-end delivery sequence \u2014 five stages",
       f_mono_s, MUTE, anchor="mm")

# ============================================================================= flow band
stages = [
    ("01", "BASE",        "fundamentals",    "0x01"),
    ("02", "STANDARDIZE", "skills \u00B7 rubrics", "0x02"),
    ("03", "PLAN",        "00\u201308 pack",      "0x03"),
    ("04", "LAND",        "landing zone",    "0x04"),
    ("05", "DEPLOY",      "agentic IaC",     "0x05"),
]
LIVE = 2  # index of current stage (PLAN)

cx0, cx1 = 230, W - 230
centers = [cx0 + (cx1 - cx0) * i / 4 for i in range(5)]
node_y = title_y + 240
R = 66
R_LIVE = 88

# --- connecting bus line through node centers ----------------------------------
for i in range(4):
    xa = centers[i] + R + 14
    xb = centers[i + 1] - R - 14
    # dashed segment
    dash = 16
    x = xa
    while x < xb:
        seg_end = min(x + dash, xb)
        col = AMBER if i < LIVE else PHOS_DIM
        d.line([(s(x), s(node_y)), (s(seg_end), s(node_y))], fill=col, width=s(2))
        x += dash * 2
    # data packets (small squares)
    for k in range(3):
        px = xa + (xb - xa) * (k + 0.5) / 3
        col = AMBER if i < LIVE else PHOS
        d.rectangle([s(px - 3), s(node_y - 3), s(px + 3), s(node_y + 3)], fill=col)
    # arrowhead
    ax = xb
    col = AMBER if i < LIVE else PHOS
    d.polygon([(s(ax), s(node_y)), (s(ax - 12), s(node_y - 7)),
               (s(ax - 12), s(node_y + 7))], fill=col)

# --- nodes ---------------------------------------------------------------------
for i, (num, name, sub, hexc) in enumerate(stages):
    cx = centers[i]
    live = (i == LIVE)
    done = (i < LIVE)
    r = R_LIVE if live else R
    ring = AMBER if live else (PHOS if done else PHOS_DIM)
    numcol = AMBER_BRT if live else (PHOS_BRIGHT if done else PHOS)

    # outer ring + glow
    d.ellipse([s(cx - r), s(node_y - r), s(cx + r), s(node_y + r)],
              outline=ring, width=s(3 if live else 2))
    if live:
        dg.ellipse([s(cx - r), s(node_y - r), s(cx + r), s(node_y + r)],
                   outline=(242, 180, 65, 200), width=s(6))
    elif done:
        dg.ellipse([s(cx - r), s(node_y - r), s(cx + r), s(node_y + r)],
                   outline=(63, 182, 168, 90), width=s(3))
    # inner thin ring
    d.ellipse([s(cx - r + 9), s(node_y - r + 9), s(cx + r - 9), s(node_y + r - 9)],
              outline=GRID_BOLD, width=1)
    # tick ring (dial marks)
    for a in range(0, 360, 30):
        rad = math.radians(a)
        r1 = r - 3
        r2 = r - 11
        x1, y1 = cx + r1 * math.cos(rad), node_y + r1 * math.sin(rad)
        x2, y2 = cx + r2 * math.cos(rad), node_y + r2 * math.sin(rad)
        d.line([(s(x1), s(y1)), (s(x2), s(y2))],
               fill=(ring if not live else AMBER), width=1)

    # station numeral
    text_c(d, (cx, node_y - 2), num, f_pixel_lg if live else f_pixel_xl, numcol, anchor="mm")
    if live:
        text_c(dg, (cx, node_y - 2), num, f_pixel_lg, (255, 209, 122, 150), anchor="mm")

    # hex tag above
    tag_col = AMBER if live else MUTE
    text_c(d, (cx, node_y - r - 30), hexc, f_silk_xs, tag_col, anchor="mm")

    # name below
    nf = f_mono_b if not (len(name) > 9) else f_mono_bn
    name_col = AMBER_BRT if live else INK
    text_c(d, (cx, node_y + r + 40), name, nf, name_col, anchor="mm")
    # sublabel
    text_c(d, (cx, node_y + r + 70), sub, f_mono_s, MUTE, anchor="mm")

    # status pip
    pip = "[OK]" if done else ("[>]" if live else "[  ]")
    pip_col = PHOS if done else (AMBER if live else PHOS_DIM)
    text_c(d, (cx, node_y + r + 96), pip, f_mono_s, pip_col, anchor="mm")

# --- YOU ARE HERE marker over the live node ------------------------------------
lx = centers[LIVE]
marker_y = node_y - R_LIVE - 64
text_c(d, (lx, marker_y), "> YOU ARE HERE", f_silk_s, AMBER, anchor="mm")
d.line([(s(lx), s(marker_y + 14)), (s(lx), s(node_y - R_LIVE - 22))], fill=AMBER, width=s(2))
d.polygon([(s(lx), s(node_y - R_LIVE - 16)), (s(lx - 6), s(node_y - R_LIVE - 28)),
           (s(lx + 6), s(node_y - R_LIVE - 28))], fill=AMBER)

# ============================================================================= bottom readout
by = fy1 - 92
# progress bar (POST-style) : 3 of 5
bar_x0, bar_x1 = fx0 + 30, W / 2 - 40
seg_n = 20
filled = int(seg_n * (LIVE + 1) / 5)
sw = (bar_x1 - bar_x0) / seg_n
d.text((s(bar_x0), s(by - 26)), "INIT SEQUENCE", font=f_silk_xs, fill=MUTE, anchor="lm")
for k in range(seg_n):
    x = bar_x0 + k * sw
    col = AMBER if k < filled else GRID_BOLD
    d.rectangle([s(x + 1), s(by - 9), s(x + sw - 2), s(by + 9)], fill=col)
text_c(d, (bar_x1 + 24, by), "03 / 05", f_mono_b, AMBER_BRT, anchor="lm")

# log line on the right
log_x = W / 2 + 200
d.text((s(log_x), s(by - 26)), "CONSOLE", font=f_silk_xs, fill=MUTE, anchor="lm")
text_c(d, (log_x, by), ">_ planning the workload \u2014 grounded in microsoft learn",
       f_mono_s, PHOS, anchor="lm")
# blinking cursor at end of log
lw = d.textlength(">_ planning the workload \u2014 grounded in microsoft learn", font=f_mono_s)
d.rectangle([s(log_x) + lw + 6, s(by - 11), s(log_x) + lw + 6 + s(11), s(by + 11)],
            fill=PHOS_BRIGHT)

# bottom captions
text_c(d, (fx0 + 30, fy1 - 30), "FIG.01 \u2014 DELIVERY SEQUENCE", f_silk_xs, MUTE, anchor="lm")
text_c(d, (fx1 - 30, fy1 - 30), "AZURE \u00B7 AGENTIC AI", f_silk_xs, MUTE, anchor="rm")

# ============================================================================= compose glow
glow_blur = glow.filter(ImageFilter.GaussianBlur(radius=14 * SS))
base = base.convert("RGBA")
base = Image.alpha_composite(base, glow_blur)
base = Image.alpha_composite(base, glow)  # crisp bright cores on top of bloom
base = base.convert("RGB")

# ----------------------------------------------------------------------------- downsample
img = base.resize((W, H), Image.LANCZOS)

# ============================================================================= CRT effects (1x, crisp)
arr = np.asarray(img).astype(np.float32)

# scanlines: darken every other ~3px band
yy = np.arange(H)
scan = (0.90 + 0.10 * (np.sin(yy / 1.5 * math.pi) * 0.5 + 0.5))  # gentle
scan = np.clip(scan, 0.86, 1.0)[:, None, None]
arr *= scan

# vignette
xs = np.linspace(-1, 1, W)[None, :]
ys = np.linspace(-1, 1, H)[:, None]
d2 = (xs ** 2) * 0.9 + (ys ** 2) * 1.0
vig = 1.0 - np.clip(d2 - 0.15, 0, 1) * 0.38
arr *= vig[:, :, None]

# faint phosphor lift in greens for CRT warmth
arr[:, :, 1] *= 1.015

arr = np.clip(arr, 0, 255).astype(np.uint8)
img = Image.fromarray(arr, "RGB")

OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT, "PNG")
print(f"saved {OUT}  ({OUT.stat().st_size:,} bytes)  {img.size}")
