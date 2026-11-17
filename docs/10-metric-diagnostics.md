# Fubini-Study Induced Metric Diagnostics

## What this is

This module computes **approximate diagnostics** of the Fubini-Study
metric induced on the tangent space of the quintic threefold affine
chart.

It is a **diagnostic tool**, not a metric solver.

## What this is NOT

- NOT a Ricci-flat Calabi-Yau metric.
- NOT a solution to the complex Monge-Ampere equation.
- NOT Donaldson's algorithm or any numerical metric method.
- NOT cohomology computed from scratch.
- NOT string spectra or compactification dynamics.
- NOT a replacement for PSM / pseudo-spectral methods.

## Mathematical setup

The quintic threefold in CP^4:

    Z0^5 + Z1^5 + Z2^5 + Z3^5 + Z4^5 = 0

Affine chart Z4 = 1:

    z0^5 + z1^5 + z2^5 + z3^5 + 1 = 0

Points live in R^8:

    (Re z0, Im z0, Re z1, Im z1, Re z2, Im z2, Re z3, Im z3)

The Fubini-Study metric on CP^4, restricted to the affine chart,
gives an 8x8 symmetric positive-definite matrix at each point.

The tangent space of the quintic at a point is the 6D subspace of
R^8 orthogonal to the two real normals of the defining equation.

By Cauchy-Riemann, those two normals are orthogonal and have equal
norm. The module checks this numerically.

The induced metric is computed by projecting the Fubini-Study metric
onto an orthonormal tangent basis.

## Diagnostics reported

For each point:

- trace of the induced 6x6 metric;
- determinant of the induced metric;
- mean eigenvalue proxy: trace / 6;
- geometric mean eigenvalue proxy: |det|^(1/6);
- minimum and maximum diagonal entries;
- approximate condition number: max diagonal / min diagonal;
- symmetry error: max absolute difference between G[i][j] and G[j][i];
- positive-definite proxy: trace > 0, det > 0 and min diagonal > 0.

For a batch of points:

- mean/min/max trace;
- mean/min/max determinant;
- mean/min/max geometric mean eigenvalue proxy;
- mean/max condition number;
- max symmetry error;
- fraction of points passing the positive-definite proxy.

## Interpretation

These quantities are heuristic indicators.

- A trace near 6 suggests the induced metric is approximately normalized
  in the chosen tangent basis.
- A determinant near 1 suggests approximate unit tangent volume.
- A condition number near 1 suggests approximate isotropy in the
  sampled tangent directions.
- Larger condition numbers or small determinants may indicate proximity
  to coordinate degeneracies or numerical stress regions.

This does NOT prove Ricci-flatness.

## CLI usage

The metric diagnostic command does not generate SVG. It generates JSON.

    PYTHONPATH=src python3 -m projection_lab.cli metric-diag \
      --grid 3 --branch 0 --seed 6 --sample 50 \
      --meta examples/metric_diag_quintic_g3_b0.json

If `--meta` is omitted, the JSON is printed to stdout.

## Makefile

    make metric-diag

## Tests

The metric layer is covered by 10 tests in:

    tests/test_metrics.py

They verify:

- Fubini-Study metric symmetry;
- positive trace of the ambient FS metric;
- orthogonality of the two real normals;
- equal norm of the two real normals;
- orthonormality of the tangent basis;
- tangent orthogonality to the normals;
- symmetry of the induced metric;
- positive-definite proxy of the induced metric;
- finiteness and basic positivity of batch diagnostics;
- rejection of invalid point length and NaN input.

## Relation to PSM / future work

A true Calabi-Yau metric requires solving a complex Monge-Ampere type
equation:

    (omega + i partial partial-bar phi)^3 = exp(f) omega^3

That is beyond the zero-dependency scope of this repository.

A future sibling repository, for example:

    calabi-yau-metric-lab

could use NumPy, SciPy, JAX or machine-learning assisted methods to
approximate Ricci-flat metrics.

This repository provides the clean geometric scaffolding:

- deterministic projections;
- exact Fermat topology;
- quintic affine chart;
- residual checks;
- branch exploration;
- tangent spaces;
- induced Fubini-Study diagnostics.

It deliberately stops before claiming Ricci-flatness.
