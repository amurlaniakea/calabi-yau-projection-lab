# Metadata and Data Contract

## Short answer

The JSON files generated beside SVG outputs are metadata manifests, not full point-cloud datasets.

They record how an output was produced. They do not currently export every point coordinate.

## What the JSON records

Typical fields include:

- object: mathematical object rendered.
- dim: ambient real dimension.
- grid: discretization parameter.
- branch: selected complex fifth-root branch for quintic chart.
- radius_max: maximum radius used in local polar grid.
- seed: projection/camera seed.
- basis_seed: seed for deterministic orthonormal basis.
- points: number of accepted points rendered.
- output: SVG path.
- svg_sha256: hash of generated SVG.

## What the JSON does not record

It does not currently contain:

- full 8D coordinates for every point;
- projected 2D coordinates for every point;
- per-point residual values;
- rejected or discarded candidate points;
- a machine-learning-ready dataset.

## Why this matters

The metadata is useful for reproducibility, auditing figures, comparing branches, classroom exercises and archival citation.

## Relationship to the web demo

The interactive demo can compute client-side telemetry such as maximum residual, discarded points, attempted points and active branch. That telemetry is visible in the browser. It is not yet fully exported into the CLI JSON metadata.

A future minor release may add a residual_check block to the JSON metadata.

## Future point export

A later release may add optional point-level exports, for example CSV or JSON files with per-point coordinates and residuals. This has not been implemented yet because it changes the data contract and should be versioned carefully.

## Gallery link semantics

In the static quintic branch gallery:

- full SVG (GitHub): human-viewable SVG file in the repository.
- metadata JSON (GitHub): human-viewable metadata manifest in the repository.
- raw JSON: machine-readable metadata file for curl, jq, Python or notebooks.

## Honesty boundary

This repository provides reproducible visual projections, local algebraic charts, exact Fermat topology for known families, approximate Fubini-Study metric diagnostics, and metadata manifests for generated outputs.

It does not provide Ricci-flat Calabi-Yau metrics, Monge-Ampere solvers, full point-cloud datasets by default, string theory simulations, or physical compactification predictions.
