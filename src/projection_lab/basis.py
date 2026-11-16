
from __future__ import annotations

import random
from typing import List

from .linalg import Vector, gram_schmidt


def orthonormal_basis(dim: int, count: int, seed: int = 0) -> List[Vector]:
    if not isinstance(dim, int) or dim < 2:
        raise ValueError("dim must be an integer >= 2")
    if not isinstance(count, int) or count < 1 or count > dim:
        raise ValueError("count must be an integer between 1 and dim")
    if not isinstance(seed, int):
        raise ValueError("seed must be an integer")

    rng = random.Random(seed)
    vectors = [[rng.gauss(0.0, 1.0) for _ in range(dim)] for _ in range(count)]
    return gram_schmidt(vectors)
