"""Small helpers that draw the decorative parts of the pages as HTML / SVG.

Nothing in here touches your data. It only makes shapes: torn paper strips, a sun
circle, a pink spiral wallpaper, and the torn edge for photos.
Every shape uses a fixed random seed, so a page looks the same every time.
"""

import math
import random


def _points(pairs):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pairs)


def torn_strip(width, top, bottom, seed, step=14, amp=3.5):
    """One strip of 'torn paper': an upper edge and a lower edge, both a bit ragged."""
    rng = random.Random(seed)
    xs = list(range(0, width + step, step))
    upper = [(x, top(x) + rng.uniform(-amp, amp)) for x in xs]
    lower = [(x, bottom(x) + rng.uniform(-amp, amp)) for x in reversed(xs)]
    return _points(upper + lower)


def collage_svg(colours, width=1200, height=560, seed=3, small=False):
    """The sun and three torn strips rising to the right.

    colours = [sun, back strip, middle strip, front strip]
    """
    sun, back, middle, front = colours
    amp = 2.0 if small else 4.0
    step = 22 if small else 14

    def line(x):
        return height * 0.92 - 0.30 * x + 0.05 * height * math.sin(x / (width * 0.14))

    thick = height * 0.24
    strips = [
        (back, lambda x: line(x) - thick * 1.35, lambda x: line(x) - thick * 0.15, seed),
        (middle, lambda x: line(x) - thick * 0.55, lambda x: line(x) + thick * 0.65, seed + 1),
        (front, lambda x: line(x) + thick * 0.20, lambda x: line(x) + thick * 1.60, seed + 2),
    ]
    shapes = "".join(
        f'<polygon points="{torn_strip(width, top, bottom, s, step, amp)}" fill="{colour}"/>'
        for colour, top, bottom, s in strips
    )
    radius = height * 0.20
    return (
        f'<svg class="collage" viewBox="0 0 {width} {height}" preserveAspectRatio="xMaxYMid slice" '
        f'xmlns="http://www.w3.org/2000/svg">'
        f'<circle cx="{width * 0.72:.0f}" cy="{height * 0.30:.0f}" r="{radius:.0f}" fill="{sun}"/>'
        f'<g style="filter: drop-shadow(0 5px 6px rgba(0,0,0,0.22))">{shapes}</g></svg>'
    )


def spiral_svg(light, dark, width=1600, height=700, seed=5):
    """A swirl of two pinks with little stars, used as the wallpaper behind the title.

    light = background colour, dark = the colour of the spiral band.
    """
    rng = random.Random(seed)
    cx, cy = width * 0.5, height * 0.5
    band = 66                              # width of the dark band
    gap = band * 2                         # distance between two turns of the spiral
    spread = gap / (2 * math.pi)           # how fast the spiral grows
    reach = math.hypot(cx, cy) + band      # far enough to cover the corners
    points, angle = [], 0.0
    while spread * angle < reach:
        wobble = 1 + 0.035 * math.sin(angle * 3)
        radius = spread * angle * wobble
        points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
        angle += 0.06
    swirl = f'<polyline points="{_points(points)}" fill="none" stroke="{dark}" stroke-width="{band}" stroke-linecap="round" stroke-linejoin="round"/>'

    stars = ""
    for _ in range(46):                    # four-pointed sparkles
        x, y, size = rng.uniform(0, width), rng.uniform(0, height), rng.uniform(5, 15)
        stars += (f'<path d="M{x:.0f} {y - size:.0f} Q{x:.0f} {y:.0f} {x + size:.0f} {y:.0f} '
                  f'Q{x:.0f} {y:.0f} {x:.0f} {y + size:.0f} Q{x:.0f} {y:.0f} {x - size:.0f} {y:.0f} '
                  f'Q{x:.0f} {y:.0f} {x:.0f} {y - size:.0f}Z" fill="#fff" opacity="{rng.uniform(0.6, 0.95):.2f}"/>')
    for _ in range(170):                   # tiny dots
        stars += (f'<circle cx="{rng.uniform(0, width):.0f}" cy="{rng.uniform(0, height):.0f}" '
                  f'r="{rng.uniform(1, 2.6):.1f}" fill="#fff" opacity="{rng.uniform(0.4, 0.9):.2f}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'preserveAspectRatio="xMidYMid slice"><rect width="{width}" height="{height}" fill="{light}"/>'
            f'{swirl}{stars}</svg>')


def torn_clip(seed=11):
    """A CSS clip-path with slightly ragged edges, used to make photos look torn out."""
    rng = random.Random(seed)
    top = [(x, rng.uniform(0, 1.6)) for x in range(0, 101, 6)]
    right = [(100 - rng.uniform(0, 1.4), y) for y in range(6, 100, 8)]
    bottom = [(x, 100 - rng.uniform(0, 1.8)) for x in range(100, -1, -6)]
    left = [(rng.uniform(0, 1.4), y) for y in range(94, 0, -8)]
    pairs = top + right + bottom + left
    return "polygon(" + ", ".join(f"{x:.1f}% {y:.1f}%" for x, y in pairs) + ")"


def nav_html(step):
    """The thin bar along the top of every page."""
    return (
        '<div class="nav"><span class="logo">PEARLFECT</span>'
        f'<span class="step">0{step} / 03</span></div>'
    )
