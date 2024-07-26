"""
Vector tests.

Author: Dennis Lönard
"""

import unittest

import numpy as np

from nvtools import NVVector, Vector


class TestVector(unittest.TestCase):
    """Vector tests."""

    def setUp(self):
        """Set up."""
        self.x = Vector("x")
        self.y = Vector("y")
        self.z = Vector("z")

    def test_init(self):
        """Test init."""
        Vector(1, 0, 0)
        Vector([1, 0, 0])
        Vector(np.array([1, 0, 0]))

        self.assertRaises(ValueError, Vector, "nonsense")

    def test_nv(self):
        """Test nv unit vectors."""
        first = NVVector().vectors
        second = (
            Vector(1, 1, 1).normalize(),
            Vector(-1, -1, 1).normalize(),
            Vector(-1, 1, -1).normalize(),
            Vector(1, -1, -1).normalize(),
        )

        for i in range(4):
            self.assertEqual(first[i], second[i])

    def test_abs(self):
        """Test abs."""
        self.assertEqual(abs(self.x), 1)

    def test_str(self):
        """Test str."""
        self.assertEqual(self.x.__str__(), "Vector([1 0 0])")
        self.assertEqual(self.x.__repr__(), "Vector([1 0 0])")

    def test_len(self):
        """Test len."""
        self.assertEqual(len(self.x), 3)

    def test_dim(self):
        """Test dim."""
        self.assertEqual(self.x.dim, 3)

    def test_angle(self):
        """Test angle."""
        self.assertAlmostEqual(self.z.angle(self.y), np.pi / 2, places=3)

    def test_angle_normal(self):
        """Test angle normal."""
        self.assertAlmostEqual(self.z.angle_normal(self.y), 0, places=3)

    def test_scalar_product(self):
        """Test scalar product."""
        self.assertAlmostEqual(self.z.scalar_product(self.y), 0, places=3)
        self.assertAlmostEqual(self.z * self.y, 0, places=3)

    def test_cross_product(self):
        """Test cross product."""
        self.assertEqual(self.x.cross_product(self.y), self.z)
        self.assertEqual(self.x @ self.y, self.z)

    def test_neg(self):
        """Test negation."""
        self.assertEqual(-self.x, Vector(-1, 0, 0))

    def test_add(self):
        """Test addition."""
        self.assertEqual(self.x + self.y, Vector(1, 1, 0))

    def test_sub(self):
        """Test subtraction."""
        self.assertEqual(self.x - self.y, Vector(1, -1, 0))

    def test_mul(self):
        """Test multiplication."""
        self.assertEqual(2 * self.x, Vector(2, 0, 0))
        self.assertEqual(2.0 * self.x, Vector(2, 0, 0))
        self.assertEqual(self.x * 2, Vector(2, 0, 0))
        self.assertEqual(self.x * 2.0, Vector(2, 0, 0))

        def not_implemented_mul():
            return self.x * "a"

        def not_implemented_rmul():
            return "a" * self.x

        def not_implemented_matmul():
            return self.x @ "a"

        self.assertRaises(TypeError, not_implemented_mul)
        self.assertRaises(TypeError, not_implemented_rmul)
        self.assertRaises(TypeError, not_implemented_matmul)

    def test_xyz(self):
        """Test x, y, z."""
        self.assertEqual(self.x.x, 1)
        self.assertEqual(self.x.y, 0)
        self.assertEqual(self.x.z, 0)

    def test_iter(self):
        """Test iter."""
        self.assertEqual([v for v in iter(self.x)], [1, 0, 0])

    def test_rotate(self):
        """Test rotate."""
        self.assertEqual(self.x.rotate(self.y, np.pi / 2), -self.z)
