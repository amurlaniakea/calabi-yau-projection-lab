
# Explicit Limitations

## 1. 2D projection is lossy

A projection from `R^6` or `R^11` to `R^2` cannot preserve all geometric information. Many distinct high-dimensional points may project to the same 2D point.

## 2. Not a physics simulator

This repository does not simulate string theory, M-theory, compactification dynamics, branes, or quantum fields.

## 3. Not a full Calabi–Yau threefold renderer

The `cy-patch` object is a Calabi–Yau-like Fermat patch in `R^4`, commonly used for visualization. It is not a complete compact Calabi–Yau threefold with full metric and topology.

## 4. Float64 precision

The implementation uses standard binary floating-point numbers. Precision limits are explicit and must be respected in reproducibility claims.

## 5. Point clouds are not meshes by default

The MVP renders point clouds. Mesh topology, normals, lighting and surface continuity are future work.

## 6. No external runtime dependencies

The core uses only Python standard library and browser-native APIs. GitHub Actions is development infrastructure, not a runtime dependency.

## 7. Visual encoding is interpretive

Color, opacity and animation can encode hidden coordinates, but they do not constitute a faithful human perception of 6D/11D geometry.

## 8. Not a fractal engine

Calabi–Yau-like objects implemented here are smooth parametrized patches or point clouds. They are not fractals, strange attractors or escape-time algorithms.
