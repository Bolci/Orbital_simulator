from skyfield.sgp4lib import EarthSatellite
import numpy as np
from copy import copy
from abc import ABC, abstractmethod
from skyfield.timelib import Time, Timescale
from skyfield.positionlib import Geocentric
from typing import Optional
from numpy.typing import NDArray


import sys
sys.path.append("../")


class SatteliteAbstract(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def at(self, t: Time) -> Optional:
        pass


class SatteliteDummy(SatteliteAbstract):
    def __init__(self, label):
        self.label = label

        self.tle_elem = None
        self.satellite_my = None

        self._x_axis = np.array([1.0, 0.0, 0.0], dtype=np.float32)
        self._y_axis = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        self._z_axis = np.array([0.0, 0.0, 1.0], dtype=np.float32)

        self.rotation_matrix = np.column_stack((self._x_axis,
                                                self._y_axis,
                                                self._z_axis))
    @property
    def x_axis(self) -> NDArray[np.float32]:
        return self._x_axis

    @property
    def y_axis(self) -> NDArray[np.float32]:
        return self._y_axis

    @property
    def z_axis(self) -> NDArray[np.float32]:
        return self._z_axis

    @x_axis.setter
    def x_axis(self, x_axis: NDArray[np.float32]) -> None:
        self._x_axis = x_axis

    @y_axis.setter
    def y_axis(self, y_axis: NDArray[np.float32]) -> None:
        self._y_axis = y_axis

    @z_axis.setter
    def z_axis(self, z_axis: NDArray[np.float32]) -> None:
        self._z_axis = z_axis


    def update_rotation_by_r_matric(self, R_matrix: NDArray[np.float32]) -> None:
        self.x_axis = np.dot(R_matrix, self.x_axis)
        self.y_axis = np.dot(R_matrix, self.y_axis)
        self.z_axis = np.dot(R_matrix, self.z_axis)

    @property
    def get_current_position(self) -> NDArray[np.float32]:
        ''' Returns possition vector relative to earth central coordinate system'''
        return self.position_vector

    @property
    def get_sattelite_orientation(self) -> NDArray[np.float32]:
        return self.initial_rotation_matrix

    def set_sattelite_orientation_by_r_matrix(self, r_matrix: NDArray[np.float32]):
        self.rotation_matrix = r_matrix
        self.update_rotation_by_r_matric(r_matrix)

    def load_sattelite(self, tle: list[str, str], ts: Timescale) -> None:
        self.satellite_my = EarthSatellite(*tle, self.label, ts)
        self.load_tle(tle)

    def load_tle(self, tle: list[str, str]):
        self.tle_elem = tle

    def at(self, t: Time) -> tuple[Geocentric, NDArray]:
        if self.satellite_my is None:
            raise Exception("Satellite data not loaded")

        geocentric = self.satellite_my.at(t)
        exact_position = geocentric.position.km
        self.position_vector = copy(exact_position)


        return geocentric, exact_position

    def __call__(self) -> EarthSatellite:
        return self.satellite_my