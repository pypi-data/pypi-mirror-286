"""This module contains objective functions used for model calibration
"""
from typing import Final
from numpy import float64
from pandas import Series

def nse(meas: Series, sim: Series) -> float:
    """Return the Nash-Sutcliffe Efficiency (NSE) of the simulated data

    Args:
        meas (Series): The measured data
        sim (Series): 

    Returns:
        float: The Nash-Sutcliffe efficiency of the simulation data
    """
    raise NotImplementedError()