"""NV tools."""

from pint import UnitRegistry

unit = UnitRegistry()

from .fit.odmr import ODMRFitter  # NOQA E402
from .io import H5Loader  # NOQA E402
from .plot import ODMRPlotter  # NOQA E402
from .solver import Solver  # NOQA E402
from .symmetry import Symmetry  # NOQA E402
from .vector import NVVector, Vector  # NOQA E402

__all__ = [
    "unit",
    "ODMRFitter",
    "Solver",
    "ODMRPlotter",
    "H5Loader",
    "Symmetry",
    "Vector",
    "NVVector",
]

VERBOSE = True
EXPORT = False
SHOW_PLOTS = True
LATEX = False
ODMR_MODEL = None

D_SPLITTING = 2870
E_SPLITTING = 5
GAMMA = (28.032 * unit.MHz / unit.mT).plus_minus(0.004)
