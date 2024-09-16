from skyfield.sgp4lib import EarthSatellite
import numpy as np
from copy import copy
import sys

sys.path.append("../")
from utils import Utils


class SatteliteDummy:
    def __init__(self, label):
        self.label = label

        self.tle_elem = None
        self.satellite_my = None

        self.x_axis = np.array([1, 0, 0], dtype=np.float32)
        self.y_axis = np.array([0, 1, 0], dtype=np.float32)
        self.z_axis = np.array([0, 0, 1], dtype=np.float32)

        self.rotation_matrix = np.column_stack((self.x_axis,
                                                self.y_axis,
                                                self.z_axis))

    @property
    def get_x_axis(self):
        return self.x_axis

    @property
    def get_y_axis(self):
        return self.y_axis

    @property
    def get_z_axis(self):
        return self.z_axis

    def update_rotation_by_r_matric(self, R_matrix):
        self.x_axis = np.dot(R_matrix, self.x_axis)
        self.y_axis = np.dot(R_matrix, self.y_axis)
        self.z_axis = np.dot(R_matrix, self.z_axis)

    def get_current_position(self):
        return self.position_vector

    def get_sattelite_orientation(self):
        return self.initial_rotation_matrix

    def set_sattelite_orientation_by_r_matrix(self, r_matrix):
        self.rotation_matrix = r_matrix
        self.update_rotation_by_r_matric(r_matrix)

    def load_sattelite(self, tle, ts):
        self.satellite_my = EarthSatellite(*tle, self.label, ts)
        self.load_tle(tle)

    def load_tle(self, tle):
        self.tle_elem = tle

    def at(self, t):
        if self.satellite_my is None:
            raise Exception("Satellite data not loaded")

        geocentric = self.satellite_my.at(t)
        exact_position = geocentric.position.km
        self.position_vector = copy(exact_position)

        return geocentric, exact_position

    def __call__(self):
        return self.satellite_my