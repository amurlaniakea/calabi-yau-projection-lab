
# Calabi–Yau Projection Lab

![CI](https://github.com/amurlaniakea/calabi-yau-projection-lab/actions/workflows/ci.yml/badge.svg)

«Tecnósfera al servicio de la Biósfera.»  
«La Paz Es El Camino.»

A professional, zero-dependency laboratory for projecting, slicing and visually encoding higher-dimensional geometric objects onto 2D planes.

> **Scope:** mathematical visualization, reproducibility and education.  
> This is **not** a string theory simulator, **not** a fractal engine, and **not** a claim that a 2D image is the “true form” of a 6D/11D object.

## What it does

- Orthogonal projections `R^n -> R^2` using deterministic orthonormal bases.
- Toy manifolds and domains:
  - 6D hypercube grid.
  - 11D random domain.
  - Flat torus fundamental domain.
  - Unit n-sphere sample.
  - Calabi–Yau-like Fermat patch in `R^4`.
- Slices with frozen coordinates.
- Reproducible SVG output and SHA-256 hashes.
- Local interactive HTML/Canvas demo, no CDN, no framework.
- Tests as evidence.

## Architecture

    calabi-yau-projection-lab/
    ├── src/projection_lab/
    │   ├── linalg.py          # dot, norm, Gram-Schmidt
    │   ├── basis.py           # deterministic orthonormal bases
    │   ├── project.py         # R^n -> R^2 projection
    │   ├── manifolds.py       # hypercube, torus, sphere, CY-like patch
    │   ├── slices.py          # fixed-coordinate slices
    │   ├── render_svg.py      # reproducible SVG renderer
    │   └── cli.py             # command line interface
    ├── tests/
    │   └── test_core.py
    ├── docs/
    │   ├── index.html         # zero-dependency local demo
    │   ├── 00-sdd.md          # Software Design Document
    │   └── 01-limitations.md  # explicit non-goals and limits
    ├── examples/
    ├── Makefile
    └── .github/workflows/ci.yml

## Quickstart

From WSL:

    cd ~/calabi-yau-projection-lab
    make test
    make examples

Open the local demo:

    explorer.exe "$(wslpath -w docs/index.html)"

Example CLI:

    PYTHONPATH=src python3 -m projection_lab.cli cube --dim 6 --steps 4 --seed 1 --out examples/cube6d.svg

    PYTHONPATH=src python3 -m projection_lab.cli domain --dim 11 --samples 2500 --seed 2 --out examples/domain11d.svg

    PYTHONPATH=src python3 -m projection_lab.cli cy-patch --degree 5 --resolution 14 --seed 3 --out examples/cy_patch.svg

## Reproducibility contract

Every generated SVG includes deterministic metadata:

- object type
- dimension
- seed
- basis seed
- point count
- color mode

The same inputs produce the same SVG and the same SHA-256 hash.

## Limits

See `docs/01-limitations.md`.

In short:

- A 2D projection loses information.
- The Calabi–Yau-like patch is not a full compact Calabi–Yau threefold.
- Float64 precision is explicit.
- No physics claims are made.
- No external runtime dependencies are used.

## License

AGPL-3.0-or-later.

© 2026 Pedro Sordo Martínez <amurlaniakea@gmail.com>

<details>
<summary>Resumen en español</summary>

Laboratorio reproducible de proyecciones geométricas de alta dimensión.

Permite proyectar objetos de `R^6`, `R^11` y parches tipo Calabi–Yau en planos 2D mediante bases ortonormales deterministas, cortes/slices y codificación visual de dimensiones ocultas.

No es un simulador de teoría de cuerdas. No es un motor de fractales. No afirma que una imagen 2D sea la forma real de un objeto 6D u 11D.

Incluye:

- núcleo matemático en Python sin dependencias externas;
- render SVG reproducible;
- tests como evidencia;
- demo local HTML/Canvas sin CDN;
- documentación de límites explícitos;
- licencia AGPL-3.0-or-later.

</details>
