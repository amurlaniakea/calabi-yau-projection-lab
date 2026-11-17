import math
import unittest

from projection_lab.manifolds import sample_quintic_threefold_chart
from projection_lab.metrics import (
    batch_diagnostics,
    fs_metric_matrix,
    induced_metric,
    metric_diagnostics,
    quintic_normals,
    tangent_basis,
)


class TestMetrics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pts = sample_quintic_threefold_chart(grid=3, branch=0)
        cls.p0 = cls.pts[0]

    def test_fs_metric_symmetry(self):
        G = fs_metric_matrix(self.p0)
        for i in range(8):
            for j in range(8):
                self.assertAlmostEqual(G[i][j], G[j][i], places=12)

    def test_fs_metric_positive_trace(self):
        G = fs_metric_matrix(self.p0)
        trace = sum(G[i][i] for i in range(8))
        self.assertGreater(trace, 0.0)

    def test_normals_orthogonal(self):
        n1, n2 = quintic_normals(self.p0)
        dot = sum(a * b for a, b in zip(n1, n2))
        self.assertLess(abs(dot), 1e-10)

    def test_normals_equal_norm(self):
        n1, n2 = quintic_normals(self.p0)
        norm1 = math.sqrt(sum(a * a for a in n1))
        norm2 = math.sqrt(sum(a * a for a in n2))
        self.assertAlmostEqual(norm1, norm2, places=10)

    def test_tangent_basis_orthonormal(self):
        n1, n2 = quintic_normals(self.p0)
        T = tangent_basis(self.p0, (n1, n2))
        self.assertEqual(len(T), 6)
        for i in range(6):
            norm = math.sqrt(sum(x * x for x in T[i]))
            self.assertAlmostEqual(norm, 1.0, places=10)
            for j in range(i + 1, 6):
                dot = sum(a * b for a, b in zip(T[i], T[j]))
                self.assertLess(abs(dot), 1e-10)

    def test_tangent_orthogonal_to_normals(self):
        n1, n2 = quintic_normals(self.p0)
        T = tangent_basis(self.p0, (n1, n2))
        for t in T:
            d1 = sum(a * b for a, b in zip(t, n1))
            d2 = sum(a * b for a, b in zip(t, n2))
            self.assertLess(abs(d1), 1e-10)
            self.assertLess(abs(d2), 1e-10)

    def test_induced_metric_symmetry(self):
        G = induced_metric(self.p0)
        for i in range(6):
            for j in range(6):
                self.assertAlmostEqual(G[i][j], G[j][i], places=10)

    def test_induced_metric_positive(self):
        d = metric_diagnostics(self.p0)
        self.assertGreater(d["trace"], 0.0)
        self.assertGreater(d["det"], 0.0)
        self.assertTrue(d["positive_definite_proxy"])

    def test_batch_diagnostics_finite(self):
        b = batch_diagnostics(self.pts[:20])
        self.assertTrue(math.isfinite(b["trace_mean"]))
        self.assertTrue(math.isfinite(b["det_mean"]))
        self.assertGreater(b["positive_definite_fraction"], 0.9)

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            fs_metric_matrix([1.0] * 7)
        with self.assertRaises(ValueError):
            fs_metric_matrix([float("nan")] * 8)


if __name__ == "__main__":
    unittest.main()
