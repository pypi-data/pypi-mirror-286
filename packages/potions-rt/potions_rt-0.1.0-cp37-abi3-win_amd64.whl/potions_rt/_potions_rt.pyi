from __future__ import annotations
from enum import Enum
from typing import List, Optional, Tuple
from dataclasses import dataclass
from numpy import float64
from numpy.typing import NDArray

# ==== Types ==== #
"""This module contains the bindings for types defined in 
Rust but need Python representations
"""
from __future__ import annotations
from enum import Enum
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class Forcing:
    """Container for meteorological forcing data"""

    precip: float
    temp: float
    pet: float

@dataclass
class ZoneType:
    """Base class for the hydrologic functional zone"""

    def forcing_flux(self, s: float, d: Forcing) -> float:
        """Hydrologic flux INTO the box from hydrometeorological forcing.
        This is intended to just be rain input or snow input. Takes the storage
        in the bucket and forcing data and returns the rate of water
        accumulation INTO the bucket.

        Args:
            s (float): storage (in millimeters) in this zone
            d (Forcing): forcing data at some step of the computation

        Returns:
            float: The rate of water flow into the bucket
        """

    def lateral_flux(self, s: float, d: Forcing) -> float:
        """Hydrologic flux OUT OF this bucket via lateral transport. Returns the
        rate of water transport OUT OF the bucket, so a positive value indicates
        flux out of the bucket.

        Some possible physical fluxes are snow melt, infiltration, or
        percolation

        Args:
            s (float): Water storage (in millimeters) in this zone
            d (Forcing): Forcing data for the flux calculation

        Returns:
            float: Rate of water flow out of this zone laterally
        """

    def vertical_flux(self, s: float, d: Forcing) -> float:
        """Hydrologic flux OUT OF this bucket via vertical transport. Returns the rate
        of vertical transport out of the bucket, so a positive value indicates water
        flow out of this bucket. The value must be nonnegative.

        Some physical examples of this flux are groundwater discharge from one
        box into one next to it or discharge from the hillslope to the stream.

        Args:
            s (float): Water storage (in millimeters) in this zone
            d (Forcing): Forcing data for the flux calculation

        Returns:
            float: The rate of water transport out of this zone vertically
        """

    def vaporization_flux(self, s: float, d: Forcing) -> float:
        """Vertical transport out of the bucket upwards via vaporization

        Some physical examples of this are snow ablation or evaportranspiration

        Args:
            s (float): Water storage (in millimeters) in this zone
            d (Forcing): Forcing data for the flux calculation

        Returns:
            float: Rate of water transport out of the bucket through vaporization
        """

    def mass_balance(self, s: float, d: Forcing) -> float:
        """Total rate of change of storage in the bucket

        Args:
            s (float): Water storage (in millimeters) in this bucket
            d (Forcing): Forcing data for the flux computation

        Returns:
            float: The rate (in millimeters per day) of water storage change in this bucket
        """

    def num_params(self) -> int:
        """Return the number of parameters in this zone

        Returns:
            int: Number of parameters that this zone contains
        """

    def parameters(self) -> List[float]:
        """Return a numpy array of parameters

        Returns:
            List[float]: The list of parameters contained in this model
        """

    def from_arr(self, arr: NDArray) -> ZoneType:
        """Construct a new zone of this type from an array of parameters

        Args:
            arr (NDArray): The array of parameters; must be one dimensional
            with the length equal to the number of parameters in this zone

        Returns:
            ZoneType: The new zone with parameters specified in `arr`
        """

@dataclass
class SnowZone(ZoneType):
    """
    Zone representing snow accumulation and melting processes
    """

    tt: float
    fmax: float

@dataclass
class SoilZone(ZoneType):
    tt: float
    fc: float
    lp: float
    beta: float
    k0: float

@dataclass
class ShallowZone(ZoneType):
    k1: float
    perc: float

@dataclass
class DeepZone(ZoneType):
    k2: float

@dataclass
class Layer:
    zones: List[ZoneType]

@dataclass
class Hillslope:
    layers: List[Layer]

@dataclass
class HydrologicModel:
    hillslopes: List[Hillslope]

@dataclass
class HBVModel:
    snow: SnowZone
    soil: SoilZone
    shallow: ShallowZone
    deep: DeepZone

class ConnectionType(Enum):
    Vertical = 0
    Lateral = 1

@dataclass
class Connection:
    ann_zone_id: int
    conn_type: ConnectionType

@dataclass
class AnnotatedZone:
    id: int
    lat_id: Optional[int]
    vert_id: Optional[int]
    zone: ZoneType
    inputs: List[Connection]
    scale: float
    zone_id: int
    layer_id: int
    hillslope_id: int

AnnotatedModel = List[AnnotatedZone]
AnnotatedHydrologicModel = AnnotatedModel

# ==== Functions ==== #

def run_hbv_model(
    model: HBVModel, init_state: NDArray, forcing: List[Forcing]
) -> Tuple[NDArray, NDArray]:
    """Run an HBV model at the daily time scale

    Args:
        model (HBVModel): The container of parameters for each of the zones in the model representation
        init_state (NDArray): Array of length 4 with the initial water storages of the snow, soil, shallow, and deep zones
        forcing (List[Forcing]): Forcing data for each step of the model

    Returns:
        tuple[NDArray, NDArray]: _description_
    """

def create_hbv_model(
    tt: float,
    fmax: float,
    fc: float,
    lp: float,
    beta: float,
    k0: float,
    thr: float,
    k1: float,
    perc: float,
    k2: float,
) -> HBVModel: ...
def hbv_model_from_numpy(arr: NDArray) -> HBVModel: ...
def hbv_model_to_numpy(model: HBVModel) -> NDArray: ...
def run_hydro_model(
    hydro_model, init_conditions: NDArray, forcing: List[List[Forcing]], dt: float
) -> tuple[NDArray, NDArray]: ...
def run_premade_hydro_model(
    ann_hyd_model: AnnotatedHydrologicModel,
    scales: List[List[float]],
    init_cond: NDArray[float64],
    forcing: List[List[Forcing]],
    dt: float,
) -> Tuple[NDArray, NDArray]: ...
