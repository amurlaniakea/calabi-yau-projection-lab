
from __future__ import annotations

import cmath
import math
import random
from itertools import product
from typing import List, Sequence

Vector = List[float]
MAX_POINTS = 100_000


def _finite_point(p: Sequence[float], limit: float = 1e9) -> bool:
    return all(math.isfinite(x) and abs(x) <= limit for x in p)


def _check_total(total: int) -> None:
    if total > MAX_POINTS:
        raise ValueError(f"Too many points ({total}); limit is {MAX_POINTS}. Reduce steps/samples/resolution.")


def sample_hypercube(dim: int = 6, steps: int = 4) -> List[Vector]:
    if dim < 2 or steps < 2:
        raise ValueError("dim and steps must be >= 2")

    total = steps ** dim
    _check_total(total)

    step = 1.0 / (steps - 1)
    return [[c * step for c in coords] for coords in product(range(steps), repeat=dim)]


def sample_random_domain(
    dim: int = 11,
    samples: int = 2000,
    seed: int = 0,
    low: float = -1.0,
    high: float = 1.0,
) -> List[Vector]:
    if dim < 2:
        raise ValueError("dim must be >= 2")
    if samples < 1 or samples > MAX_POINTS:
        raise ValueError(f"samples must be between 1 and {MAX_POINTS}")
    if low >= high:
        raise ValueError("low must be < high")

    rng = random.Random(seed)
    return [[rng.uniform(low, high) for _ in range(dim)] for _ in range(samples)]


def sample_flat_torus(dim: int = 6, samples: int = 2000, seed: int = 0) -> List[Vector]:
    return sample_random_domain(dim=dim, samples=samples, seed=seed, low=0.0, high=1.0)


def sample_nd_sphere(dim: int = 4, samples: int = 2000, seed: int = 0) -> List[Vector]:
    if dim < 2:
        raise ValueError("dim must be >= 2")
    if samples < 1 or samples > MAX_POINTS:
        raise ValueError(f"samples must be between 1 and {MAX_POINTS}")

    rng = random.Random(seed)
    points: List[Vector] = []

    for _ in range(samples):
        v = [rng.gauss(0.0, 1.0) for _ in range(dim)]
        n = math.sqrt(sum(x * x for x in v))
        if n > 1e-12:
            points.append([x / n for x in v])

    return points


def sample_calabi_yau_like_patch(degree: int = 5, resolution: int = 16) -> List[Vector]:
    # Generate a 4D real point cloud for a Fermat-type Calabi-Yau-like patch.
    # This is an educational patch/parametrization, not a full compact Calabi-Yau threefold.
    if degree < 2 or degree > 12:
        raise ValueError("degree must be between 2 and 12")
    if resolution < 2 or resolution > 80:
        raise ValueError("resolution must be between 2 and 80")

    total = degree * degree * (resolution + 1) * (resolution + 1)
    _check_total(total)

    points: List[Vector] = []
    eps = 1e-9
    u0, u1 = 0.0, math.pi / 2.0 - eps
    v0, v1 = -math.pi / 2.0 + eps, math.pi / 2.0 - eps
    exponent = 2.0 / float(degree)

    for k1 in range(degree):
        phase1 = cmath.exp(2j * math.pi * k1 / degree)
        for k2 in range(degree):
            phase2 = cmath.exp(2j * math.pi * k2 / degree)
            for i in range(resolution + 1):
                u = u0 + (u1 - u0) * (i / resolution)
                for j in range(resolution + 1):
                    v = v0 + (v1 - v0) * (j / resolution)
                    xi = complex(u, v)

                    try:
                        c = cmath.cos(xi)
                        s = cmath.sin(xi)
                        z1 = phase1 * (c ** exponent)
                        z2 = phase2 * (s ** exponent)
                    except (ValueError, OverflowError, ZeroDivisionError):
                        continue

                    p = [z1.real, z1.imag, z2.real, z2.imag]
                    if _finite_point(p, 1e6):
                        points.append(p)

    if not points:
        raise RuntimeError("Generated no finite points")

    return points


def point_dimension(points: Sequence[Sequence[float]]) -> int:
    if not points:
        raise ValueError("Empty point cloud")
    return len(points[0])

def sample_clifford_torus(
    samples_u: int = 64,
    samples_v: int = 64,
    radius: float = 1.0 / math.sqrt(2.0),
) -> List[Vector]:
    """Sample a Clifford torus embedded in R^4.

    For radius = 1/sqrt(2), the torus lies on the unit 3-sphere S^3:

        (r cos u, r sin u, r cos v, r sin v)

    with u, v in [0, 2pi).

    This is an educational smooth 2D surface in 4D,
    not a Calabi-Yau threefold.
    """
    if samples_u < 2 or samples_v < 2:
        raise ValueError("samples_u and samples_v must be >= 2")

    if samples_u > MAX_POINTS or samples_v > MAX_POINTS:
        raise ValueError(
            f"samples_u and samples_v must be <= {MAX_POINTS}"
        )

    total = samples_u * samples_v
    _check_total(total)

    rf = float(radius)
    if not math.isfinite(rf) or rf <= 0.0:
        raise ValueError("radius must be finite and > 0")

    points: List[Vector] = []
    two_pi = 2.0 * math.pi

    for i in range(samples_u):
        u = two_pi * (i / samples_u)
        cu = rf * math.cos(u)
        su = rf * math.sin(u)

        for j in range(samples_v):
            v = two_pi * (j / samples_v)
            pt = [cu, su, rf * math.cos(v), rf * math.sin(v)]

            if _finite_point(pt, 1e6):
                points.append(pt)

    if not points:
        raise RuntimeError("Generated no finite points")

    return points

def _complex_nth_root(z_re, z_im, n, branch):
    r = math.hypot(z_re, z_im)
    if r == 0.0:
        return (0.0, 0.0)
    theta = math.atan2(z_im, z_re)
    if theta < 0.0:
        theta += 2.0 * math.pi
    rn = r ** (1.0 / n)
    theta_n = (theta + 2.0 * math.pi * branch) / n
    return (rn * math.cos(theta_n), rn * math.sin(theta_n))


def sample_quintic_threefold_chart(
    grid: int = 4,
    branch: int = 0,
    radius_max: float = 1.0,
) -> List[Vector]:
    """Sample a local affine chart of the quintic Calabi-Yau threefold.

    Equation in CP^4: Z0^5 + Z1^5 + Z2^5 + Z3^5 + Z4^5 = 0.
    Affine chart Z4 = 1: z0^5 + z1^5 + z2^5 + z3^5 + 1 = 0.

    Parametrize (z0, z1, z2) on a polar grid in the disk |z| <= radius_max,
    solve z3 = (-1 - z0^5 - z1^5 - z2^5)^(1/5) using the given branch.

    Returns points in R^8:
        (Re z0, Im z0, Re z1, Im z1, Re z2, Im z2, Re z3, Im z3)

    This is a LOCAL chart, not the global variety. It does not cover
    points where Z4 = 0. Five branches give five local patches.
    """
    if grid < 2:
        raise ValueError("grid must be >= 2")
    if not (0 <= branch <= 4):
        raise ValueError("branch must be in [0, 4]")
    if radius_max <= 0.0 or not math.isfinite(radius_max):
        raise ValueError("radius_max must be finite and > 0")

    total = grid ** 6
    if total > MAX_POINTS:
        raise ValueError(
            f"grid too large: {total} points > {MAX_POINTS}"
        )

    radii = [radius_max * (i + 0.5) / grid for i in range(grid)]
    angles = [2.0 * math.pi * j / grid for j in range(grid)]

    points: List[Vector] = []

    for r0 in radii:
        for a0 in angles:
            z0_re = r0 * math.cos(a0)
            z0_im = r0 * math.sin(a0)
            for r1 in radii:
                for a1 in angles:
                    z1_re = r1 * math.cos(a1)
                    z1_im = r1 * math.sin(a1)
                    for r2 in radii:
                        for a2 in angles:
                            z2_re = r2 * math.cos(a2)
                            z2_im = r2 * math.sin(a2)
                            rhs_re = -1.0 - (z0_re**5 - 10*z0_re**3*z0_im**2 + 5*z0_re*z0_im**4)
                            rhs_re -= (z1_re**5 - 10*z1_re**3*z1_im**2 + 5*z1_re*z1_im**4)
                            rhs_re -= (z2_re**5 - 10*z2_re**3*z2_im**2 + 5*z2_re*z2_im**4)
                            rhs_im = -(5*z0_re**4*z0_im - 10*z0_re**2*z0_im**3 + z0_im**5)
                            rhs_im -= (5*z1_re**4*z1_im - 10*z1_re**2*z1_im**3 + z1_im**5)
                            rhs_im -= (5*z2_re**4*z2_im - 10*z2_re**2*z2_im**3 + z2_im**5)
                            z3_re, z3_im = _complex_nth_root(rhs_re, rhs_im, 5, branch)
                            res_re = (z0_re**5 - 10*z0_re**3*z0_im**2 + 5*z0_re*z0_im**4)
                            res_re += (z1_re**5 - 10*z1_re**3*z1_im**2 + 5*z1_re*z1_im**4)
                            res_re += (z2_re**5 - 10*z2_re**3*z2_im**2 + 5*z2_re*z2_im**4)
                            res_re += (z3_re**5 - 10*z3_re**3*z3_im**2 + 5*z3_re*z3_im**4)
                            res_re += 1.0
                            res_im = (5*z0_re**4*z0_im - 10*z0_re**2*z0_im**3 + z0_im**5)
                            res_im += (5*z1_re**4*z1_im - 10*z1_re**2*z1_im**3 + z1_im**5)
                            res_im += (5*z2_re**4*z2_im - 10*z2_re**2*z2_im**3 + z2_im**5)
                            res_im += (5*z3_re**4*z3_im - 10*z3_re**2*z3_im**3 + z3_im**5)
                            if math.hypot(res_re, res_im) > 1e-9:
                                continue
                            pt = [z0_re, z0_im, z1_re, z1_im,
                                  z2_re, z2_im, z3_re, z3_im]
                            if all(math.isfinite(x) for x in pt):
                                points.append(pt)

    if not points:
        raise RuntimeError("Generated no finite points on the quintic chart")

    return points

