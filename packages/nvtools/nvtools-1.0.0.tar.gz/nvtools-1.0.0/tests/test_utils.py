"""
Utils tests.

Author: Dennis Lönard
"""

import unittest
from unittest.mock import patch

from nvtools.utils import critical, success, warning


class TestUtils(unittest.TestCase):
    """Test utils."""

    @patch("builtins.print")
    def test_warning(self, mock_print):
        """Test warning."""
        warning("test")

    @patch("builtins.print")
    def test_critical(self, mock_print):
        """Test warning."""
        critical("test")

    @patch("builtins.print")
    def test_success(self, mock_print):
        """Test warning."""
        success("test")
