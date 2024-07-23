"""This module contains return type of hydrology as a
wrapper for running the model
"""
# from typing import Final
import pandas as pd
from pandas import DataFrame, Series

@pd.api.extensions.register_dataframe_accessor("hydro")
class HydroDataFrame:
    def __init__(self, storage: DataFrame, fluxes: DataFrame):
        self._storage: DataFrame = storage
        self._fluxes: DataFrame = fluxes

    @property
    def streamflow(self) -> Series:
        """Return the streamflow from this dataset

        Returns:
            Series: The streamflow from all sections of this catchment
        """
        raise NotImplementedError()