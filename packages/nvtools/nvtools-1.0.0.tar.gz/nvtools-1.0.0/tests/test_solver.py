"""
Solver tests.

Author: Dennis Lönard
"""

import math
import pathlib
import unittest
from unittest.mock import patch

import numpy as np

from nvtools import *
from nvtools.solver import BField


class TestSolver(unittest.TestCase):
    """Solver tests."""

    def setUp(self):
        """Set up."""
        self.solver = Solver()

    @patch("builtins.print")
    def test_field_from_resonances(self, mock_print):
        """Test field from resonances."""
        b_abs, theta = self.solver.field_from_resonances(2865 * unit.MHz, 2875 * unit.MHz)

        self.assertEqual(b_abs, 0.0)
        self.assertTrue(math.isnan(theta.magnitude))

    @patch("builtins.print")
    def test_resonances_from_field(self, mock_print):
        """Test resonances from field."""
        fu, fl = self.solver.resonances_from_field(0.0 * unit.mT, 0.0 * unit.rad)

        self.assertAlmostEqual(fu.magnitude.nominal_value, 2875, places=3)
        self.assertAlmostEqual(fl.magnitude.nominal_value, 2865, places=3)

    @patch("builtins.print")
    def test_field_from_spectrum(self, mock_print):
        """Test field from spectrum."""
        mw_frequency = np.linspace(2600, 3150, 5500)
        tests_folder = pathlib.Path(__file__).parent
        odmr = np.genfromtxt(pathlib.Path(tests_folder, "test_data", "test_odmr_full.csv"), delimiter="\n")

        fit_results, b_field = self.solver.field_from_spectrum(mw_frequency, odmr)

        expected_b_abs = [
            8.103429120802481,
            8.158523646990679,
            8.133861783029143,
            8.143313654674017,
        ]
        expected_theta = [
            0.45509349883803824,
            0.8481239437403075,
            1.2457574411113799,
            1.4871191658428629,
        ]

        for i in range(4):
            self.assertAlmostEqual(b_field.b_abs[i].magnitude.nominal_value, expected_b_abs[i], places=3)
            self.assertAlmostEqual(b_field.theta[i].magnitude.nominal_value, expected_theta[i], places=3)

    def test_mean_field(self):
        """Test mean field."""
        b_field = BField([1.0, 1.1, 1.2, 1.3], [0.1, 0.2, 0.3, 0.4], Vector("x"))

        self.assertAlmostEqual(b_field.mean_field, np.mean(b_field.b_abs), places=3)
