"""Exact topological invariants for Fermat-type hypersurfaces.

Integer combinatorics only. No floating point. No external deps.
Not a metric computation. Not cohomology from scratch.
"""
from __future__ import annotations

from typing import Dict, Tuple


def is_calabi_yau(degree: int, ambient_dim: int) -> bool:
    """Calabi-Yau condition for a hypersurface in CP^n: d = n + 1."""
    return degree == ambient_dim + 1


_HODGE: Dict[Tuple[int, int], Dict[str, int]] = {
    (3, 2): {"h00": 1, "h10": 1, "h11": 1},
    (4, 3): {"h00": 1, "h10": 0, "h20": 1, "h11": 20, "h21": 0, "h22": 1},
    (5, 4): {"h00": 1, "h10": 0, "h20": 0, "h30": 1,
             "h11": 1, "h21": 101, "h22": 1, "h31": 0, "h32": 0, "h33": 1},
    (3, 3): {"h00": 1, "h10": 0, "h20": 0, "h11": 7, "h21": 0, "h22": 1},
}


def hodge_numbers_fermat(degree: int, ambient_dim: int) -> Dict[str, int]:
    """Return exact Hodge numbers for known Fermat hypersurfaces.

    Supported: (3,2), (4,3), (5,4), (3,3).
    Raises ValueError for unsupported combinations.
    """
    key = (degree, ambient_dim)
    if key not in _HODGE:
        supported = ", ".join(f"(d={d},n={n})" for d, n in sorted(_HODGE))
        raise ValueError(
            f"Unsupported (degree={degree}, ambient={ambient_dim}). "
            f"Supported: {supported}"
        )
    return dict(_HODGE[key])


def euler_characteristic(hodge: Dict[str, int]) -> int:
    """Topological Euler characteristic from Hodge numbers.

    chi = sum_{p,q} (-1)^{p+q} h^{p,q}

    Exact integer arithmetic.
    """
    chi = 0
    for key, value in hodge.items():
        if len(key) == 3 and key.startswith("h"):
            p, q = int(key[1]), int(key[2])
            factor = 1 if p == q else 2
            chi += ((-1) ** (p + q)) * value * factor
    return chi


def classify_fermat(degree: int, ambient_dim: int) -> Dict[str, object]:
    """Full classification record for a Fermat-type hypersurface.

    Returns dict with degree, ambient_dim, complex_dim, real_dim,
    is_calabi_yau, hodge_numbers, euler_characteristic, note.
    """
    cdim = ambient_dim - 1
    out: Dict[str, object] = {
        "degree": degree,
        "ambient_dim": ambient_dim,
        "complex_dim": cdim,
        "real_dim": 2 * cdim,
        "is_calabi_yau": is_calabi_yau(degree, ambient_dim),
    }
    try:
        h = hodge_numbers_fermat(degree, ambient_dim)
        out["hodge_numbers"] = h
        out["euler_characteristic"] = euler_characteristic(h)
        out["note"] = "Exact integer combinatorics. Not a metric computation."
    except ValueError as exc:
        out["hodge_numbers"] = None
        out["euler_characteristic"] = None
        out["note"] = str(exc)
    return out
