"""
Test IO.

Author: Dennis Lönard
"""

import os
import pathlib
import tempfile
import unittest
from unittest.mock import patch

import h5py
import numpy as np

from nvtools import H5Loader


class TestIO(unittest.TestCase):
    """Test IO."""

    def setUp(self):
        """Set up."""
        tests_folder = pathlib.Path(__file__).parent
        self.odmr = np.genfromtxt(pathlib.Path(tests_folder, "test_data", "test_odmr_full.csv"), delimiter="\n")

        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".h5")
        self.file_path = self.temp_file.name
        with h5py.File(self.file_path, "w") as file:
            file.create_dataset("Iterators/Iterator", data=np.array([1, 2]))

            file.create_dataset("Meta Info/Iterators", data="Iterator: 1/2")
            file.create_dataset("Meta Info/Parameters/Sweep Start Frequency in MHz", data=np.array(2600.0))
            file.create_dataset("Meta Info/Parameters/Sweep Stop Frequency in MHz", data=np.array(3150.0))
            file.create_dataset("Meta Info/Parameters/Samples", data=np.array(5500.0))

            file.create_dataset("Observables/X/0", data=self.odmr)
            file.create_dataset("Observables/X/1", data=self.odmr)

        self.loader = H5Loader(self.file_path)

    def tearDown(self):
        """Tear down."""
        self.temp_file.close()
        os.remove(self.file_path)

    @patch("builtins.print")
    def test_print_contents(self, mock_print):
        """Test print contents."""
        self.loader.print_contents()

    @patch("builtins.print")
    def test_load_odmr_lia(self, mock_print):
        """Test load ODMR LIA."""
        data = self.loader.load_odmr_lia()

        self.assertTrue(np.allclose(data.x_data, np.linspace(2600, 3150, 5500)))
        self.assertTrue(np.allclose(data.observables["X"], self.odmr))
