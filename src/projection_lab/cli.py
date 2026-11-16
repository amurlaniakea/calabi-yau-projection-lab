
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import List, Optional, Sequence

from .basis import orthonormal_basis
from .manifolds import (
    sample_calabi_yau_like_patch,
    sample_clifford_torus,
    sample_flat_torus,
    sample_hypercube,
    sample_nd_sphere,
    sample_random_domain,
)
from .project import project_points
from .render_svg import render_scatter_svg, sha256_text
from .slices import parse_fixed, sample_slice_grid
from .topology import classify_fermat


def _write_text(path: str, text: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def _values_for(points: Sequence[Sequence[float]], color_by: str, dim: int) -> Optional[List[float]]:
    if color_by == "none":
        return None

    if color_by == "radius":
        return [math.sqrt(sum(x * x for x in p)) for p in points]

    if color_by == "auto":
        idx = dim - 1
    else:
        try:
            idx = int(color_by)
        except ValueError as exc:
            raise ValueError("--color-by must be auto, none, radius, or an index") from exc

    if idx < 0 or idx >= dim:
        raise ValueError(f"color index {idx} out of range")

    return [p[idx] for p in points]


def _add_common(sub: argparse.ArgumentParser) -> None:
    sub.add_argument("--out", required=True, help="Output SVG path")
    sub.add_argument("--meta", default=None, help="Optional JSON metadata path")
    sub.add_argument("--width", type=int, default=900)
    sub.add_argument("--height", type=int, default=900)
    sub.add_argument("--margin", type=int, default=48)
    sub.add_argument("--radius", type=float, default=2.0)
    sub.add_argument("--seed", type=int, default=0)
    sub.add_argument("--basis-seed", type=int, default=None)
    sub.add_argument("--color-by", default="auto", help="auto|none|radius|index")


def _finish(args, points, dim: int, object_name: str, extra_metadata: Optional[dict] = None) -> None:
    basis_seed = args.basis_seed if args.basis_seed is not None else args.seed
    basis = orthonormal_basis(dim, 2, basis_seed)
    projected = project_points(points, basis)
    values = _values_for(points, args.color_by, dim)

    metadata = {
        "object": object_name,
        "dim": dim,
        "seed": args.seed,
        "basis_seed": basis_seed,
        "points": len(points),
        "color_by": args.color_by,
    }

    if extra_metadata:
        metadata.update(extra_metadata)

    svg = render_scatter_svg(
        projected,
        values=values,
        width=args.width,
        height=args.height,
        margin=args.margin,
        point_radius=args.radius,
        metadata=metadata,
    )

    _write_text(args.out, svg)
    digest = sha256_text(svg)

    if args.meta:
        payload = dict(metadata)
        payload["svg_sha256"] = digest
        payload["output"] = args.out
        _write_text(args.meta, json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(f"Wrote {args.out}")
    print(f"Points: {len(points)} Dim: {dim} SHA256: {digest}")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="projection-lab",
        description="Zero-dependency higher-dimensional projection lab",
    )
    subs = parser.add_subparsers(dest="command", required=True)

    p = subs.add_parser("cube", help="Hypercube grid in R^dim")
    _add_common(p)
    p.add_argument("--dim", type=int, default=6)
    p.add_argument("--steps", type=int, default=4)
    p.set_defaults(
        func=lambda a: _finish(
            a,
            sample_hypercube(a.dim, a.steps),
            a.dim,
            "hypercube",
            {"steps": a.steps},
        )
    )

    p = subs.add_parser("domain", help="Random domain in R^dim")
    _add_common(p)
    p.add_argument("--dim", type=int, default=11)
    p.add_argument("--samples", type=int, default=2000)
    p.set_defaults(
        func=lambda a: _finish(
            a,
            sample_random_domain(a.dim, a.samples, a.seed),
            a.dim,
            "random_domain",
            {"samples": a.samples},
        )
    )

    p = subs.add_parser("torus", help="Flat torus fundamental domain [0,1)^dim")
    _add_common(p)
    p.add_argument("--dim", type=int, default=6)
    p.add_argument("--samples", type=int, default=2000)
    p.set_defaults(
        func=lambda a: _finish(
            a,
            sample_flat_torus(a.dim, a.samples, a.seed),
            a.dim,
            "flat_torus",
            {"samples": a.samples},
        )
    )

    p = subs.add_parser("sphere", help="Unit n-sphere sample")
    _add_common(p)
    p.add_argument("--dim", type=int, default=4)
    p.add_argument("--samples", type=int, default=2000)
    p.set_defaults(
        func=lambda a: _finish(
            a,
            sample_nd_sphere(a.dim, a.samples, a.seed),
            a.dim,
            "nd_sphere",
            {"samples": a.samples},
        )
    )

    p = subs.add_parser("cy-patch", help="Calabi-Yau-like Fermat patch in R^4")
    _add_common(p)
    p.add_argument("--degree", type=int, default=5)
    p.add_argument("--resolution", type=int, default=16)
    p.set_defaults(
        func=lambda a: _finish(
            a,
            sample_calabi_yau_like_patch(a.degree, a.resolution),
            4,
            "calabi_yau_like_patch",
            {"degree": a.degree, "resolution": a.resolution},
        )
    )

    p = subs.add_parser("slice", help="Grid slice with fixed coordinates")
    _add_common(p)
    p.add_argument("--dim", type=int, default=6)
    p.add_argument("--steps", type=int, default=8)
    p.add_argument("--fixed", default="", help="e.g. 3=0.2,4=0.7")
    p.set_defaults(
        func=lambda a: _finish(
            a,
            sample_slice_grid(a.dim, parse_fixed(a.fixed), a.steps),
            a.dim,
            "slice_grid",
            {"steps": a.steps, "fixed": a.fixed},
        )
    )

    p = subs.add_parser("clifford-torus", help="Clifford torus in R^4")
    _add_common(p)
    p.add_argument("--samples-u", type=int, default=64)
    p.add_argument("--samples-v", type=int, default=64)
    p.add_argument("--torus-radius", type=float, default=1.0 / math.sqrt(2.0))
    p.set_defaults(
        func=lambda a: _finish(
            a,
            sample_clifford_torus(a.samples_u, a.samples_v, a.torus_radius),
            4,
            "clifford_torus",
            {"samples_u": a.samples_u, "samples_v": a.samples_v, "radius": a.radius},
        )
    )

    p = subs.add_parser("topology", help="Exact Hodge numbers for Fermat hypersurfaces")
    p.add_argument("--degree", type=int, required=True)
    p.add_argument("--ambient", type=int, required=True)
    p.add_argument("--out", default=None, help="Optional JSON output path")
    p.set_defaults(func=lambda a: _topology_cmd(a))

    args = parser.parse_args(argv)
    args.func(args)
    return 0


def _topology_cmd(args) -> None:
    result = classify_fermat(args.degree, args.ambient)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.out:
        _write_text(args.out, payload)
        print(f"Wrote {args.out}")
    print(payload)


if __name__ == "__main__":
    raise SystemExit(main())
