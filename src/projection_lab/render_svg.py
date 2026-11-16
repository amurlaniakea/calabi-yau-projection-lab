
from __future__ import annotations

import hashlib
import math
from typing import Dict, List, Optional, Sequence, Tuple


def _escape_xml(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _hsl_to_rgb(h: float, s: float, l: float) -> Tuple[int, int, int]:
    h = h % 1.0

    if s == 0:
        r = g = b = l
    else:
        def hue2rgb(p: float, q: float, t: float) -> float:
            if t < 0:
                t += 1
            if t > 1:
                t -= 1
            if t < 1 / 6:
                return p + (q - p) * 6 * t
            if t < 1 / 2:
                return q
            if t < 2 / 3:
                return p + (q - p) * (2 / 3 - t) * 6
            return p

        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = hue2rgb(p, q, h + 1 / 3)
        g = hue2rgb(p, q, h)
        b = hue2rgb(p, q, h - 1 / 3)

    return (
        max(0, min(255, int(round(r * 255)))),
        max(0, min(255, int(round(g * 255)))),
        max(0, min(255, int(round(b * 255)))),
    )


def _color_from_t(t: float) -> str:
    t = max(0.0, min(1.0, t))
    h = 0.65 - 0.65 * t
    r, g, b = _hsl_to_rgb(h, 0.85, 0.55)
    return f"#{r:02x}{g:02x}{b:02x}"


def _normalize_values(values: Optional[Sequence[float]]) -> Optional[List[float]]:
    if values is None:
        return None

    vals = [float(v) for v in values]
    if not vals:
        return None

    if any(math.isnan(v) or math.isinf(v) for v in vals):
        raise ValueError("Color values contain NaN or Inf")

    mn, mx = min(vals), max(vals)
    if mx - mn < 1e-15:
        return [0.5 for _ in vals]

    return [(v - mn) / (mx - mn) for v in vals]


def _scale_points(
    points_2d: Sequence[Sequence[float]],
    width: int,
    height: int,
    margin: int,
) -> List[Tuple[float, float]]:
    xs = [p[0] for p in points_2d]
    ys = [p[1] for p in points_2d]

    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)

    rangex = maxx - minx if maxx > minx else 1.0
    rangey = maxy - miny if maxy > miny else 1.0

    availw = width - 2 * margin
    availh = height - 2 * margin

    if availw <= 0 or availh <= 0:
        raise ValueError("Width/height too small for margin")

    scale = min(availw / rangex, availh / rangey)
    offsetx = (availw - rangex * scale) / 2.0
    offsety = (availh - rangey * scale) / 2.0

    out: List[Tuple[float, float]] = []
    for x, y in points_2d:
        sx = margin + offsetx + (x - minx) * scale
        sy = height - margin - offsety - (y - miny) * scale
        out.append((sx, sy))

    return out


def render_scatter_svg(
    points_2d: Sequence[Sequence[float]],
    values: Optional[Sequence[float]] = None,
    width: int = 900,
    height: int = 900,
    margin: int = 48,
    point_radius: float = 2.0,
    background: str = "#0b0e14",
    metadata: Optional[Dict[str, object]] = None,
    title: str = "Higher-dimensional projection",
) -> str:
    if not points_2d:
        raise ValueError("No points to render")

    if len(points_2d) > 100_000:
        raise ValueError("Too many points for SVG; use <= 100000")

    cleaned: List[Tuple[float, float]] = []
    for p in points_2d:
        if len(p) != 2:
            raise ValueError("Projected points must be 2D")
        x = float(p[0])
        y = float(p[1])
        if math.isnan(x) or math.isinf(x) or math.isnan(y) or math.isinf(y):
            raise ValueError("Projected point contains NaN/Inf")
        cleaned.append((x, y))

    norm_values = _normalize_values(values)
    if norm_values is not None and len(norm_values) != len(cleaned):
        raise ValueError("values length must match points length")

    scaled = _scale_points(cleaned, width, height, margin)

    parts: List[str] = []
    parts.append('<?xml version="1.0" encoding="UTF-8"?>\n')
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">\n'
    )

    if metadata:
        items = "; ".join(
            f"{_escape_xml(str(k))}={_escape_xml(str(v))}"
            for k, v in sorted(metadata.items(), key=lambda kv: str(kv[0]))
        )
        parts.append(f"  <!-- {items} -->\n")

    parts.append(f"  <title>{_escape_xml(title)}</title>\n")
    parts.append(f'  <rect width="100%" height="100%" fill="{_escape_xml(background)}"/>\n')

    for i, (x, y) in enumerate(scaled):
        color = _color_from_t(norm_values[i]) if norm_values is not None else "#7fd1ff"
        parts.append(
            f'  <circle cx="{x:.3f}" cy="{y:.3f}" r="{point_radius}" '
            f'fill="{color}" fill-opacity="0.75"/>\n'
        )

    parts.append("</svg>\n")
    return "".join(parts)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
