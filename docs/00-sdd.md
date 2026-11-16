
# Software Design Document (SDD)

## 1. Mission

Provide a zero-dependency, auditable and reproducible laboratory for studying how higher-dimensional geometric objects can be projected, sliced and visually encoded in 2D.

## 2. Scope

The repository implements:

- deterministic linear projections `R^n -> R^2`;
- orthonormal basis generation from integer seeds;
- simple manifold/domain samplers:
  - hypercube;
  - random domain;
  - flat torus fundamental domain;
  - unit n-sphere;
  - Calabi–Yau-like Fermat patch in `R^4`;
- coordinate-frozen slices;
- SVG scatter rendering with color encoding;
- SHA-256 reproducibility checks;
- local HTML/Canvas educational demo.

## 3. Non-goals

This project does not:

- simulate string theory;
- simulate M-theory;
- compute true Calabi–Yau threefold metrics;
- preserve Riemannian/Kähler geometry under 2D projection;
- claim that a 2D image is the “real shape” of a 6D/11D object;
- use external runtime dependencies such as NumPy, Three.js, React, WebGL wrappers or CDNs.

## 4. Architectural principles

### 4.1 Zero unnecessary dependencies

Runtime code uses only:

- Python standard library;
- browser-native HTML/CSS/JavaScript.

### 4.2 Explicit limits

Every generator has explicit maximum point counts and parameter ranges.

### 4.3 Determinism

Randomness is seeded. The same seed and parameters produce the same basis, points, SVG and hash.

### 4.4 Tests as evidence

Mathematical invariants are tested:

- orthonormality;
- linearity of projection;
- finite output;
- reproducible SVG hash;
- slice coordinate freezing.

### 4.5 Separation of concerns

    math -> sampling -> projection -> rendering -> CLI/web

## 5. Module map

| Module | Responsibility |
|---|---|
| `linalg.py` | Dot product, norm, normalization, Gram-Schmidt |
| `basis.py` | Deterministic orthonormal bases |
| `project.py` | Point and point-cloud projection |
| `manifolds.py` | Object generators |
| `slices.py` | Fixed-coordinate slices |
| `render_svg.py` | Reproducible SVG renderer |
| `cli.py` | Command line interface |
| `docs/index.html` | Local interactive demo |

## 6. Core mathematical model

Given `x in R^n` and an orthonormal basis `{u1, u2}` of a 2-plane in `R^n`:

    y1 = dot(x, u1)
    y2 = dot(x, u2)

The pair `(y1, y2)` is the orthogonal projection of `x` onto that plane.

Different bases produce different projections. Therefore the basis seed is part of the reproducibility metadata.

## 7. Calabi–Yau-like patch

The current `cy-patch` generator uses a Fermat-type parametrization in complex coordinates:

    z1^n + z2^n = 1

represented as a real point cloud in `R^4`:

    (Re(z1), Im(z1), Re(z2), Im(z2))

This is an educational patch/visualization, not a full compact Calabi–Yau threefold.

## 8. Roadmap

### Phase 1 — MVP

- deterministic projection core;
- SVG renderer;
- tests;
- CLI;
- local demo.

### Phase 2 — richer slices

- 3D slices from 6D objects;
- mesh/edge rendering;
- more color encodings.

### Phase 3 — Grassmannian exploration

- compare many projection planes;
- measure overlap, density, variance;
- visualize projection stability.

### Phase 4 — optional advanced branch

- GPU/WebGL experimental branch, isolated from zero-dependency core;
- higher-precision arithmetic;
- full algebraic patch documentation.
