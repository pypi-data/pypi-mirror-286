"""
Symmetry tests.

Author: Dennis Lönard
"""

import unittest

from nvtools import Symmetry, Vector


class TestSymmetry(unittest.TestCase):
    """Symmetry tests."""

    def test_td_symmetry(self):
        """Test Td symmetry."""
        v = Vector(1, 1, 1)
        td = Symmetry("Td")

        new_vs = list(td.apply(v))

        self.assertEqual(len(new_vs), 24)

    def test_oh_symmetry(self):
        """Test Oh symmetry."""
        v = Vector(1, 1, 1)
        oh = Symmetry("Oh")

        new_vs = list(oh.apply(v))

        self.assertEqual(len(new_vs), 48)
