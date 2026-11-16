
from __future__ import annotations

import math
import unittest

from projection_lab.basis import orthonormal_basis
from projection_lab.linalg import dot, gram_schmidt, is_orthonormal, norm, normalize
from projection_lab.manifolds import (
    sample_calabi_yau_like_patch,
    sample_hypercube,
    sample_nd_sphere,
    sample_random_domain,
)
from projection_lab.project import project_point, project_points
from projection_lab.render_svg import render_scatter_svg, sha256_text
from projection_lab.slices import parse_fixed, sample_slice_grid


class TestLinalg(unittest.TestCase):
    def test_dot(self):
        self.assertAlmostEqual(dot([1, 2, 3], [4, 5, 6]), 32.0)

    def test_norm(self):
        self.assertAlmostEqual(norm([3, 4]), 5.0)

    def test_normalize(self):
        v = normalize([3, 4])
        self.assertAlmostEqual(norm(v), 1.0)

    def test_normalize_zero_raises(self):
        with self.assertRaises(ValueError):
            normalize([0, 0])

    def test_gram_schmidt_is_orthonormal(self):
        basis = gram_schmidt([[1, 1, 0], [1, 0, 1], [0, 1, 1]])
        self.assertTrue(is_orthonormal(basis))


class TestBasis(unittest.TestCase):
    def test_deterministic(self):
        b1 = orthonormal_basis(6, 2, seed=123)
        b2 = orthonormal_basis(6, 2, seed=123)
        self.assertEqual(b1, b2)

    def test_orthonormal(self):
        b = orthonormal_basis(11, 2, seed=9)
        self.assertTrue(is_orthonormal(b))

    def test_invalid_dim(self):
        with self.assertRaises(ValueError):
            orthonormal_basis(1, 1, seed=0)


class TestProjection(unittest.TestCase):
    def test_zero_point(self):
        b = orthonormal_basis(6, 2, seed=1)
        p = project_point([0.0] * 6, b)
        self.assertEqual(p, [0.0, 0.0])

    def test_basis_vector_projects_to_unit(self):
        b = orthonormal_basis(6, 2, seed=2)
        self.assertAlmostEqual(project_point(b[0], b)[0], 1.0)
        self.assertAlmostEqual(project_point(b[0], b)[1], 0.0)

    def test_linearity(self):
        b = orthonormal_basis(6, 2, seed=3)
        x = [1, 2, 3, 4, 5, 6]
        y = [-1, 0.5, 2, -3, 1, 0]
        s = [xi + yi for xi, yi in zip(x, y)]

        px = project_point(x, b)
        py = project_point(y, b)
        ps = project_point(s, b)

        for a, bb, c in zip(px, py, ps):
            self.assertAlmostEqual(a + bb, c)


class TestManifolds(unittest.TestCase):
    def test_hypercube_count(self):
        pts = sample_hypercube(6, 3)
        self.assertEqual(len(pts), 3 ** 6)
        self.assertEqual(len(pts[0]), 6)

    def test_random_domain_finite(self):
        pts = sample_random_domain(11, 100, seed=5)
        self.assertEqual(len(pts), 100)
        for p in pts:
            self.assertTrue(all(math.isfinite(x) for x in p))

    def test_sphere_unit_norm(self):
        pts = sample_nd_sphere(4, 50, seed=7)
        for p in pts:
            self.assertAlmostEqual(norm(p), 1.0, places=10)

    def test_calabi_yau_like_patch_dimension_and_finiteness(self):
        pts = sample_calabi_yau_like_patch(3, 4)
        self.assertGreater(len(pts), 0)
        for p in pts:
            self.assertEqual(len(p), 4)
            self.assertTrue(all(math.isfinite(x) for x in p))


class TestSlices(unittest.TestCase):
    def test_parse_fixed(self):
        fixed = parse_fixed("3=0.25,4=0.75")
        self.assertEqual(fixed, {3: 0.25, 4: 0.75})

    def test_slice_freezes_coordinates(self):
        pts = sample_slice_grid(6, {3: 0.25, 4: 0.75}, 3)
        self.assertEqual(len(pts), 3 ** 4)
        for p in pts:
            self.assertAlmostEqual(p[3], 0.25)
            self.assertAlmostEqual(p[4], 0.75)


class TestRender(unittest.TestCase):
    def test_svg_contains_header(self):
        svg = render_scatter_svg([[0, 0], [1, 1]], metadata={"seed": 1})
        self.assertIn("<svg", svg)
        self.assertIn("seed=1", svg)

    def test_rejects_nan(self):
        with self.assertRaises(ValueError):
            render_scatter_svg([[float("nan"), 0]])

    def test_hash_stable(self):
        pts = sample_hypercube(6, 3)
        basis = orthonormal_basis(6, 2, 7)
        proj = project_points(pts, basis)
        vals = [p[5] for p in pts]

        svg1 = render_scatter_svg(proj, vals, metadata={"seed": 7})
        svg2 = render_scatter_svg(proj, vals, metadata={"seed": 7})

        self.assertEqual(sha256_text(svg1), sha256_text(svg2))


if __name__ == "__main__":
    unittest.main()
