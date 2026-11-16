
from __future__ import annotations

from typing import List, Sequence

from .linalg import Vector, dot, validate_vector


def project_point(point: Sequence[float], basis: Sequence[Sequence[float]]) -> Vector:
    if not basis:
        raise ValueError("Basis must contain at least one vector")

    p = validate_vector(point)
    dim = len(basis[0])

    if len(p) != dim:
        raise ValueError("Point dimension does not match basis dimension")

    for u in basis:
        if len(u) != dim:
            raise ValueError("All basis vectors must have the same dimension")

    return [dot(p, u) for u in basis]


def project_points(points: Sequence[Sequence[float]], basis: Sequence[Sequence[float]]) -> List[Vector]:
    return [project_point(p, basis) for p in points]
