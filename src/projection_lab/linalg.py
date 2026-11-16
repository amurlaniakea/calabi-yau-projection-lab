
from __future__ import annotations

import math
from typing import List, Sequence

Vector = List[float]


def validate_vector(v: Sequence[float]) -> Vector:
    out: Vector = []
    for x in v:
        xf = float(x)
        if math.isnan(xf) or math.isinf(xf):
            raise ValueError("Vector contains NaN or Inf")
        out.append(xf)
    return out


def dot(a: Sequence[float], b: Sequence[float]) -> float:
    if len(a) != len(b):
        raise ValueError("Vectors must have same length")
    return sum(float(x) * float(y) for x, y in zip(a, b))


def norm(v: Sequence[float]) -> float:
    return math.sqrt(dot(v, v))


def normalize(v: Sequence[float]) -> Vector:
    w = validate_vector(v)
    nv = norm(w)
    if nv < 1e-15:
        raise ValueError("Cannot normalize zero vector")
    return [x / nv for x in w]


def gram_schmidt(vectors: Sequence[Sequence[float]]) -> List[Vector]:
    ortho: List[Vector] = []
    for v in vectors:
        w = validate_vector(v)
        for u in ortho:
            coeff = dot(w, u)
            w = [wi - coeff * ui for wi, ui in zip(w, u)]
        nv = norm(w)
        if nv < 1e-12:
            raise ValueError("Input vectors are linearly dependent")
        ortho.append([xi / nv for xi in w])
    return ortho


def is_orthonormal(basis: Sequence[Sequence[float]], tol: float = 1e-9) -> bool:
    for i, u in enumerate(basis):
        if abs(dot(u, u) - 1.0) > tol:
            return False
        for j in range(i + 1, len(basis)):
            if abs(dot(u, basis[j])) > tol:
                return False
    return True
