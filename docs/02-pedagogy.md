# Pedagogical Guide

## Purpose

This repository is a teaching instrument for linear algebra,
higher-dimensional geometry, topology intuition and reproducible
scientific visualization.

It helps students understand what a 2D image of a 6D or 11D object
actually means.

## Learning objectives

After using this repository, a student should be able to:

1. Explain an orthogonal projection as a linear map:

    pi: R^n -> R^2

2. Understand that a projection loses information.

3. Explain why many distinct high-dimensional points can project
   to the same 2D point.

4. Distinguish between:
   - the mathematical object;
   - a sampled point cloud;
   - a 2D projection;
   - a visual interpretation.

5. Use slices / cuts as a way to inspect higher-dimensional objects.

6. Understand color, opacity or animation as encodings of hidden
   coordinates.

7. Differentiate smooth manifolds from fractals and strange attractors.

8. Reproduce an image from a seed and understand why the seed matters.

## Classroom analogies

### Shadow analogy

A 3D object casts a 2D shadow. Similarly, a 6D or 11D object can
cast a 2D shadow through a linear projection. The shadow is useful,
but it is not the object.

### Slice analogy

A 3D apple passing through a 2D plane appears to a flat being as
a sequence of circles. Similarly, a 6D object can be inspected
through lower-dimensional slices.

### Camera analogy

The orthonormal basis used for projection acts like a choice of
camera plane in high-dimensional space. Changing the seed changes
the camera. The object can stay the same while the image changes.

### Color as hidden coordinate

When projecting R^n -> R^2, there are n - 2 hidden coordinates.
The renderer can encode one hidden coordinate as color. This is
informative, but it is still an interpretation.

## Common misconceptions

### "This is a photo of a Calabi-Yau"

No. A 2D image cannot be a faithful photograph of a 6D object.
It is a projection, slice, sampling or visual encoding.

### "Calabi-Yau shapes are fractals"

No. Calabi-Yau varieties are smooth geometric objects, not fractals.
Fractals have self-similarity and often fractional dimension.
Calabi-Yau threefolds have integer dimension: complex 3, real 6.

### "More colors mean more physics"

No. Color may encode a coordinate, radius, index or arbitrary scalar.
It does not automatically represent physical truth.

### "If the image is pretty, it is scientifically valid"

No. The repository prioritizes reproducibility and explicit
limitations over decorative output.

### "Any projection preserves shape"

No. Orthogonal projection preserves some linear structure, but not
full metric, topology or curvature information.

## Suggested classroom activities

### Activity 1: Compare projections

Generate the same 6D hypercube with different seeds:

    PYTHONPATH=src python3 -m projection_lab.cli cube \
      --dim 6 --steps 4 --seed 1 \
      --out examples/cube6d_seed1.svg

    PYTHONPATH=src python3 -m projection_lab.cli cube \
      --dim 6 --steps 4 --seed 2 \
      --out examples/cube6d_seed2.svg

Ask students:

- Is the object changing?
- Is the projection plane changing?
- Why do the images differ?
- What information is lost?

### Activity 2: Explore slices

    PYTHONPATH=src python3 -m projection_lab.cli slice \
      --dim 6 --steps 8 --fixed 3=0.0,4=0.0 --seed 10 \
      --out examples/slice6d_fixed00.svg

    PYTHONPATH=src python3 -m projection_lab.cli slice \
      --dim 6 --steps 8 --fixed 3=0.5,4=0.5 --seed 10 \
      --out examples/slice6d_fixed55.svg

Ask: what does freezing a coordinate mean? How is this similar
to a medical scan?

### Activity 3: Color encoding

    PYTHONPATH=src python3 -m projection_lab.cli cube \
      --dim 6 --steps 4 --seed 1 --color-by auto \
      --out examples/cube6d_auto.svg

    PYTHONPATH=src python3 -m projection_lab.cli cube \
      --dim 6 --steps 4 --seed 1 --color-by radius \
      --out examples/cube6d_radius.svg

Ask: what scalar is being colored? Does color change the geometry?

## Minimal mathematical summary

Given a point x = (x1, x2, ..., xn) in R^n and an orthonormal
basis of a 2-plane u1, u2 in R^n, the projection is:

    y1 = dot(x, u1)
    y2 = dot(x, u2)

So y = (y1, y2) in R^2.

Different bases produce different images. That is why the
repository stores object type, dimension, seed, basis seed,
point count, color mode and SHA-256 of the SVG.

## Resumen en espanol

Este repositorio es una herramienta docente para entender
proyecciones de alta dimension.

No muestra la forma real de un objeto 6D u 11D. Muestra sombras,
cortes y codificaciones visuales reproducibles.

Sirve para ensenar: proyeccion lineal, perdida de informacion,
cortes/slices, coordenadas ocultas, diferencia entre variedad
suave y fractal, reproducibilidad cientifica, intuicion geometrica
en dimensiones superiores.
