# Object Gallery

This document explains the mathematical objects currently implemented
in the projection lab.

All objects are sampled as point clouds and projected to 2D.
They are educational models, not full physical simulations.

## 1. Hypercube

Command:

    PYTHONPATH=src python3 -m projection_lab.cli cube \
      --dim 6 --steps 4 --seed 1 --out examples/cube6d.svg

Mathematical idea: a grid in [0, 1]^n.

For dim=6 and steps=4, the number of points is 4^6 = 4096.

Pedagogical value: simple high-dimensional domain; shows how a
regular lattice becomes a projected cloud; useful to compare seeds
and projection planes.

Limitations: it is a sampled grid, not a continuous hypercube;
projection loses adjacency and metric information.

## 2. Random domain

Command:

    PYTHONPATH=src python3 -m projection_lab.cli domain \
      --dim 11 --samples 2500 --seed 2 --out examples/domain11d.svg

Mathematical idea: uniform random points in a hyperrectangle
[low, high]^n. Default: [-1, 1]^11.

Pedagogical value: shows how high-dimensional randomness appears
in 2D; useful as a baseline before more structured objects.

Limitations: no geometry beyond the sampling domain; not a manifold.

## 3. Flat torus fundamental domain

Command:

    PYTHONPATH=src python3 -m projection_lab.cli torus \
      --dim 6 --samples 2000 --seed 5 --out examples/torus6d.svg

Mathematical idea: points in [0, 1)^n interpreted as a fundamental
domain of R^n / Z^n.

Pedagogical value: introduces quotient spaces; shows a compact flat
torus toy model.

Limitations: the renderer does not draw identifications at boundaries;
it is not a curved Calabi-Yau torus fibration.

## 4. Unit n-sphere

Command:

    PYTHONPATH=src python3 -m projection_lab.cli sphere \
      --dim 4 --samples 2000 --seed 7 --out examples/sphere4d.svg

Mathematical idea: points satisfying approximately
x1^2 + x2^2 + ... + xn^2 = 1.

Pedagogical value: simple compact curved object; useful to test
projection of symmetric sets.

Limitations: sampled point cloud, not mesh; no geodesics or
curvature rendering.

## 5. Calabi-Yau-like Fermat patch

Command:

    PYTHONPATH=src python3 -m projection_lab.cli cy-patch \
      --degree 5 --resolution 14 --seed 3 --out examples/cy_patch.svg

Mathematical idea: a parametrized patch related to Fermat-type
complex equations such as z1^n + z2^n = 1, represented in real
coordinates as (Re(z1), Im(z1), Re(z2), Im(z2)) in R^4.

Pedagogical value: connects to popular Calabi-Yau visualizations;
shows smooth folded structure in projected 2D.

Important limitation: this is NOT a full compact Calabi-Yau
threefold. It is an educational 4D patch/parametrization projected
to 2D.

## 6. Slice grid

Command:

    PYTHONPATH=src python3 -m projection_lab.cli slice \
      --dim 6 --steps 8 --fixed 3=0.25,4=0.75 --seed 4 \
      --out examples/slice6d.svg

Mathematical idea: a grid in R^dim where some coordinates are frozen.

Pedagogical value: explains tomographic intuition; reduces complexity
before projection; useful for classroom comparison of different cuts.

Limitations: the slice is a discrete grid; frozen coordinates are not
visualized directly unless encoded by color or metadata.

## 7. Clifford torus

Command:

    PYTHONPATH=src python3 -m projection_lab.cli clifford-torus \
      --samples-u 48 --samples-v 48 --seed 5 \
      --out examples/clifford_torus.svg

Mathematical idea: a torus embedded in 4D:

    (u, v) -> (r cos u, r sin u, r cos v, r sin v)

with u, v in [0, 2pi). If r = 1/sqrt(2), the torus lies on the
unit 3-sphere S^3.

Pedagogical value: shows a smooth 2D surface in 4D; illustrates
product geometry S^1 x S^1; useful for explaining hidden coordinates
and projection loss; bridges simple tori, spheres and
higher-dimensional compact objects.

Limitations: it is not a Calabi-Yau threefold; it is a point cloud,
not a mesh with normals or lighting.

## How to read any object image

For every generated SVG, ask:

1. What is the original dimension?
2. What object was sampled?
3. What seed defined the projection plane?
4. What coordinate is encoded as color?
5. What information was lost in projection?
6. Is this a full object, a patch, a slice or a sampled domain?

If the answer is not explicit, the image is decorative.
In this repository, the goal is that the answer is explicit.
