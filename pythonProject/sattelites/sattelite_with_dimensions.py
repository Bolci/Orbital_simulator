from random import sample

from .sattelite_dummy import SatteliteDummy
import sys
from skyfield.timelib import Time
from skyfield.positionlib import Geocentric
from numpy.typing import NDArray
import numpy as np

sys.path.append("../")
from objects import Sphere


class SatteliteWithDimension(SatteliteDummy):
    def __init__(self, label, radius) -> None:
        super().__init__(label)
        self.radius = radius
        self.satt_object = Sphere.get_planet(radius)
        self.ini_position = np.array([0.,0.,0.])

    @property
    def get_radius(self) -> float:
        return self.radius

    def get_report_by_time(self, time: Time):
        sample = super().get_report_by_time(time)
        sample['Dimensions'] = self.get_radius
        return sample

    def at(self, t: Time) -> tuple[Geocentric, NDArray]:
        if self.satellite_my is None:
            raise Exception("Satellite data not loaded")

        geocentric, exact_position = super().at(t)

        return geocentric, exact_position


