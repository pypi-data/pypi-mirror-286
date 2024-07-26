"""Fit utils."""

import numpy as np


def r_squared(f, x, y, popt):
    """Calculate R^2 value of fit curve."""
    res = y - f(x, *popt)
    ss_res = np.sum(np.power(res, 2))
    ss_tot = np.sum(np.power(y - np.mean(y), 2))

    return 1 - (ss_res / ss_tot)
