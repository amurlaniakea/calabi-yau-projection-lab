"""Fubini-Study induced metric diagnostics for the quintic threefold chart.

IMPORTANT: This module computes APPROXIMATE diagnostics of the
Fubini-Study metric induced on the tangent space of the quintic
affine chart. It does NOT compute:

- Ricci-flat Calabi-Yau metrics;
- solutions to the complex Monge-Ampere equation;
- Donaldson's algorithm or any numerical metric solver;
- cohomology groups from scratch;
- string spectra or compactification dynamics.

The output is a diagnostic tool for education and research
prototyping, clearly labeled as an approximation.

Mathematical background:

The quintic threefold X in CP^4 is defined by:

    Z0^5 + Z1^5 + Z2^5 + Z3^5 + Z4^5 = 0

In the affine chart Z4 = 1, with coordinates z0, z1, z2, z3 in C:

    z0^5 + z1^5 + z2^5 + z3^5 + 1 = 0

Each point lives in R^8 = (Re z0, Im z0, Re z1, Im z1, Re z2, Im z2, Re z3, Im z3).

The Fubini-Study metric on CP^4 (up to normalization) restricted to
the affine chart C^4 is:

    ds^2 = sum_k |dz_k|^2 / (1 + |z|^2)
           - |sum_k conj(z_k) dz_k|^2 / (1 + |z|^2)^2

In real coordinates (x0, y0, x1, y1, x2, y2, x3, y3), this gives
an 8x8 symmetric positive-definite matrix G_FS.

The tangent space T_p X at a point p on the quintic is the 6D
subspace of R^8 orthogonal to the two real normals:

    n1 = grad(Re(F))
    n2 = grad(Im(F))

where F = z0^5 + z1^5 + z2^5 + z3^5 + 1.

By Cauchy-Riemann, n1 and n2 are orthogonal and have equal norm.

The induced metric on T_p X is:

    G_induced[i][j] = t_i^T G_FS t_j

where {t_1, ..., t_6} is an orthonormal basis of T_p X.

Diagnostics reported:

- trace(G_induced): sum of eigenvalues;
- det(G_induced): product of eigenvalues;
- mean_eigenvalue = trace / 6;
- geo_mean_eigenvalue = det^(1/6);
- condition_number_approx = max_diag / min_diag.

These are NOT rigorous curvature computations. They are simple
scalar indicators of how the FS metric behaves on the tangent
space of the quintic chart.
"""

import math
from typing import List, Tuple, Dict, Any

Vector = List[float]
Matrix = List[List[float]]


def _z_pow5_components(x: float, y: float) -> Tuple[float, float]:
    """Return (Re(z^5), Im(z^5)) for z = x + iy."""
    x2 = x * x
    y2 = y * y
    x3 = x2 * x
    y3 = y2 * y
    x4 = x2 * x2
    y4 = y2 * y2
    re = x4 * x - 10.0 * x3 * y2 + 5.0 * x * y4
    im = 5.0 * x4 * y - 10.0 * x2 * y3 + y4 * y
    return (re, im)


def _z_pow5_grad_components(x: float, y: float) -> Tuple[float, float, float, float]:
    """Return (dRe/dx, dRe/dy, dIm/dx, dIm/dy) for z^5."""
    x2 = x * x
    y2 = y * y
    x3 = x2 * x
    y3 = y2 * y
    x4 = x2 * x2
    y4 = y2 * y2
    d_re_dx = 5.0 * x4 - 30.0 * x2 * y2 + 5.0 * y4
    d_re_dy = -20.0 * x3 * y + 20.0 * x * y3
    d_im_dx = 20.0 * x3 * y - 20.0 * x * y3
    d_im_dy = 5.0 * x4 - 30.0 * x2 * y2 + 5.0 * y4
    return (d_re_dx, d_re_dy, d_im_dx, d_im_dy)


def fs_metric_matrix(point: Vector) -> Matrix:
    """Compute the 8x8 Fubini-Study metric matrix at a point in R^8 (C^4).

    The metric is:
        G = I/(1+r^2) - (v v^T + w w^T)/(1+r^2)^2

    where v = (x0, y0, x1, y1, x2, y2, x3, y3)
          w = (-y0, x0, -y1, x1, -y2, x2, -y3, x3)
          r^2 = sum of squares of point coordinates.
    """
    if len(point) != 8:
        raise ValueError("point must have 8 components")
    if not all(math.isfinite(c) for c in point):
        raise ValueError("point must have finite components")

    r2 = sum(c * c for c in point)
    denom = 1.0 + r2
    denom2 = denom * denom

    v = point[:]
    w = []
    for k in range(4):
        w.append(-point[2 * k + 1])
        w.append(point[2 * k])

    G = []
    for i in range(8):
        row = []
        for j in range(8):
            val = (1.0 if i == j else 0.0) / denom
            val -= (v[i] * v[j] + w[i] * w[j]) / denom2
            row.append(val)
        G.append(row)
    return G


def quintic_normals(point: Vector) -> Tuple[Vector, Vector]:
    """Compute the two real normal vectors to the quintic at a point in R^8.

    Returns (n1, n2) where:
        n1 = grad(Re(F))
        n2 = grad(Im(F))

    By Cauchy-Riemann, n1 . n2 = 0 and |n1| = |n2|.
    """
    if len(point) != 8:
        raise ValueError("point must have 8 components")

    n1 = [0.0] * 8
    n2 = [0.0] * 8

    for k in range(4):
        x = point[2 * k]
        y = point[2 * k + 1]
        dr_dx, dr_dy, di_dx, di_dy = _z_pow5_grad_components(x, y)
        n1[2 * k] = dr_dx
        n1[2 * k + 1] = dr_dy
        n2[2 * k] = di_dx
        n2[2 * k + 1] = di_dy

    return (n1, n2)


def _dot(a: Vector, b: Vector) -> float:
    return sum(x * y for x, y in zip(a, b))


def _norm(a: Vector) -> float:
    return math.sqrt(_dot(a, a))


def _gram_schmidt(vectors: List[Vector]) -> List[Vector]:
    ortho = []
    for v in vectors:
        w = v[:]
        for u in ortho:
            c = _dot(w, u)
            for i in range(len(w)):
                w[i] -= c * u[i]
        n = _norm(w)
        if n > 1e-12:
            ortho.append([x / n for x in w])
    return ortho


def tangent_basis(point: Vector, normals: Tuple[Vector, Vector]) -> List[Vector]:
    """Build an orthonormal 6D tangent basis orthogonal to the two normals.

    Uses Gram-Schmidt on the 8 standard basis vectors projected
    onto the orthogonal complement of span(n1, n2).
    """
    n1, n2 = normals
    basis = []
    for i in range(8):
        e = [0.0] * 8
        e[i] = 1.0
        # Project out n1 and n2
        c1 = _dot(e, n1) / (_dot(n1, n1) + 1e-30)
        c2 = _dot(e, n2) / (_dot(n2, n2) + 1e-30)
        for j in range(8):
            e[j] -= c1 * n1[j] + c2 * n2[j]
        basis.append(e)
    ortho = _gram_schmidt(basis)
    if len(ortho) < 6:
        raise RuntimeError("Could not build 6D tangent basis")
    return ortho[:6]


def induced_metric(point: Vector) -> Matrix:
    """Compute the 6x6 induced FS metric on the quintic tangent space."""
    G_fs = fs_metric_matrix(point)
    n1, n2 = quintic_normals(point)
    T = tangent_basis(point, (n1, n2))

    G_ind = []
    for i in range(6):
        row = []
        for j in range(6):
            val = 0.0
            for a in range(8):
                for b in range(8):
                    val += T[i][a] * G_fs[a][b] * T[j][b]
            row.append(val)
        G_ind.append(row)
    return G_ind


def _det_6x6(M: Matrix) -> float:
    """Compute determinant of a 6x6 matrix via LU decomposition with partial pivoting."""
    n = 6
    A = [row[:] for row in M]
    det = 1.0
    for col in range(n):
        # Partial pivoting
        max_val = abs(A[col][col])
        max_row = col
        for row in range(col + 1, n):
            if abs(A[row][col]) > max_val:
                max_val = abs(A[row][col])
                max_row = row
        if max_val < 1e-15:
            return 0.0
        if max_row != col:
            A[col], A[max_row] = A[max_row], A[col]
            det *= -1.0
        det *= A[col][col]
        pivot = A[col][col]
        for row in range(col + 1, n):
            factor = A[row][col] / pivot
            for j in range(col, n):
                A[row][j] -= factor * A[col][j]
    return det


def metric_diagnostics(point: Vector) -> Dict[str, Any]:
    """Compute diagnostic scalars for the induced FS metric at a point."""
    G = induced_metric(point)
    trace = sum(G[i][i] for i in range(6))
    det = _det_6x6(G)
    diag = [G[i][i] for i in range(6)]
    min_diag = min(diag)
    max_diag = max(diag)
    mean_eig = trace / 6.0
    geo_mean_eig = abs(det) ** (1.0 / 6.0) if det > 0 else 0.0
    cond = max_diag / min_diag if min_diag > 1e-15 else float('inf')

    # Check symmetry
    sym_err = 0.0
    for i in range(6):
        for j in range(i + 1, 6):
            sym_err = max(sym_err, abs(G[i][j] - G[j][i]))

    return {
        "trace": trace,
        "det": det,
        "mean_eigenvalue": mean_eig,
        "geo_mean_eigenvalue": geo_mean_eig,
        "min_diagonal": min_diag,
        "max_diagonal": max_diag,
        "condition_number_approx": cond,
        "symmetry_error": sym_err,
        "positive_definite_proxy": trace > 0 and det > 0 and min_diag > 0,
    }


def batch_diagnostics(points: List[Vector]) -> Dict[str, Any]:
    """Aggregate metric diagnostics over a point cloud."""
    if not points:
        raise ValueError("points list is empty")

    traces = []
    dets = []
    geos = []
    conds = []
    sym_errs = []
    pd_count = 0

    for p in points:
        d = metric_diagnostics(p)
        traces.append(d["trace"])
        dets.append(d["det"])
        geos.append(d["geo_mean_eigenvalue"])
        conds.append(d["condition_number_approx"])
        sym_errs.append(d["symmetry_error"])
        if d["positive_definite_proxy"]:
            pd_count += 1

    n = len(points)
    return {
        "points": n,
        "positive_definite_count": pd_count,
        "positive_definite_fraction": pd_count / n,
        "trace_mean": sum(traces) / n,
        "trace_min": min(traces),
        "trace_max": max(traces),
        "det_mean": sum(dets) / n,
        "det_min": min(dets),
        "det_max": max(dets),
        "geo_mean_eigenvalue_mean": sum(geos) / n,
        "geo_mean_eigenvalue_min": min(geos),
        "geo_mean_eigenvalue_max": max(geos),
        "condition_number_mean": sum(conds) / n,
        "condition_number_max": max(conds),
        "symmetry_error_max": max(sym_errs),
    }
