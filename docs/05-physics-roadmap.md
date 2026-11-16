# Physics-Oriented Roadmap

## Current status (v1.x)

Zero-dependency educational projection laboratory with exact
topological invariants for Fermat families.

Provides:

- reproducible 2D projections of higher-dimensional point clouds;
- slices with frozen coordinates;
- Calabi-Yau-like Fermat patches in R^4;
- Clifford torus in R^4;
- exact Hodge numbers and Euler characteristic for known
  Fermat hypersurfaces using integer combinatorics;
- 30 tests as evidence.

Does NOT yet compute:

- Ricci-flat Calabi-Yau metrics;
- Fubini-Study induced metric tensors;
- tangent spaces or Christoffel symbols;
- cohomology groups from scratch;
- string spectra or compactification dynamics.

## Intended evolution

### Level 1 (current): exact discrete invariants

Hodge numbers, Euler characteristic, Calabi-Yau condition check.
Integer arithmetic. Zero dependencies. Fully testable.

### Level 2 (next): local threefold charts

Sample a 6D affine chart of the quintic:

    z0^5 + z1^5 + z2^5 + z3^5 + 1 = 0

    z3 = (-1 - z0^5 - z1^5 - z2^5)^(1/5)

Project R^6 -> R^2. Document branch selection and residual checks.

### Level 3 (future): Fubini-Study metric diagnostics

Compute approximate induced metric, tangent basis, scalar curvature
proxy. Always label as:

    Fubini-Study induced approximation, not Ricci-flat CY metric

### Level 4 (sibling repo): Donaldson / ML metrics

A separate repository (e.g. calabi-yau-metric-lab) would use
NumPy/SciPy or JAX for:

- Donaldson algorithm iterations;
- complex Monge-Ampere solvers;
- ML-based Calabi-Yau metric approximation.

This repository stays zero-dependency.

## Explicit limitations for physics use

This repository does not:

- compute Ricci-flat metrics;
- verify Calabi-Yau condition numerically beyond algebraic metadata;
- compute cohomology groups from scratch;
- calculate full string spectra;
- simulate compactification dynamics;
- model M-theory on G2 manifolds;
- replace computer algebra systems for algebraic geometry.

## Honest positioning

> A zero-dependency, reproducible educational laboratory for
> higher-dimensional projections, Calabi-Yau-like patches, local
> algebraic charts and exact topological invariants.
> Useful for teaching, outreach and visual prototyping.
> Not a full theoretical physics engine.
