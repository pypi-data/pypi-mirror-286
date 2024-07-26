"""
Plotter tests.

Author: Dennis Lönard
"""

import pathlib
import unittest
from unittest.mock import patch

import numpy as np

from nvtools import *


class TestODMRPlotter(unittest.TestCase):
    """ODMR plotter tests."""

    def setUp(self):
        """Set up."""
        self.plotter = ODMRPlotter()

    @patch("builtins.print")
    @patch("matplotlib.pyplot.show")
    def test_plot_from_spectrum(self, mock_show, mock_print):
        """Test plot from spectrum."""
        mw_frequency = np.linspace(2600, 3150, 5500)
        tests_folder = pathlib.Path(__file__).parent
        odmr = np.genfromtxt(pathlib.Path(tests_folder, "test_data", "test_odmr_full.csv"), delimiter="\n")

        fit_results, b_field = self.plotter.plot_from_spectrum(mw_frequency, odmr)

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
