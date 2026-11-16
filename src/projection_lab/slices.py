
from __future__ import annotations

from itertools import product
from typing import Dict, List, Optional

from .manifolds import MAX_POINTS, Vector


def parse_fixed(spec: str) -> Dict[int, float]:
    fixed: Dict[int, float] = {}
    if not spec or not spec.strip():
        return fixed

    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "=" not in part:
            raise ValueError(f"Invalid fixed coordinate: {part!r}. Use idx=value, e.g. 3=0.2")
        k, v = part.split("=", 1)
        fixed[int(k.strip())] = float(v.strip())

    return fixed


def sample_slice_grid(
    dim: int = 6,
    fixed: Optional[Dict[int, float]] = None,
    steps: int = 8,
) -> List[Vector]:
    if dim < 3:
        raise ValueError("dim must be >= 3 for a slice with at least 2 free dimensions")

    fixed = dict(fixed) if fixed else {}

    for idx in fixed:
        if idx < 0 or idx >= dim:
            raise ValueError(f"Fixed index {idx} out of range for dim {dim}")

    free = [i for i in range(dim) if i not in fixed]

    if len(free) < 2:
        raise ValueError("Slice must leave at least 2 free dimensions")

    if steps < 2:
        raise ValueError("steps must be >= 2")

    total = steps ** len(free)
    if total > MAX_POINTS:
        raise ValueError(f"Too many slice points ({total}); limit is {MAX_POINTS}")

    step = 1.0 / (steps - 1)
    points: List[Vector] = []

    for coords in product(range(steps), repeat=len(free)):
        p = [0.0] * dim
        for idx, val in fixed.items():
            p[idx] = float(val)
        for idx, c in zip(free, coords):
            p[idx] = c * step
        points.append(p)

    return points
