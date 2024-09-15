from skyfield.sgp4lib import EarthSatellite
import numpy as np

from scipy.spatial.transform import Rotation as R
from copy import copy
import sys

sys.path.append("../")
from utils import Utils


class SatteliteDummy:
    def __init__(self, label, orientation_quaternion = np.array((0.0,0.0,0.0))):
        self.label = label

        self.tle_elem = None
        self.satellite_my = None
        self.orientation_quaternion = orientation_quaternion

        self.x_axis = np.array([1, 0, 0 ], dtype=np.float32)
        self.y_axis = np.array([0, 1, 0], dtype=np.float32)
        self.z_axis = np.array([0, 0, 1], dtype=np.float32)

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
        self.x_axis = R_matrix.apply(self.x_axis)
        self.y_axis = R_matrix.apply(self.y_axis)
        self.z_axis = R_matrix.apply(self.z_axis)

    def update_axis_by_quaternion(self, quaterion):
        R_matrix = Utils.convert_quaternion_to_rotation_matrix(quaterion)
        self.x_axis = R_matrix.dot(self.x_axis)
        self.y_axis = R_matrix.dot(self.y_axis)
        self.z_axis = R_matrix.dot(self.z_axis)

    def get_current_position(self):
        return self.position_vector

    def get_sattelite_orientation(self):
        return self.orientation_quaternion

    def set_rotation_quaternion(self, orientation_quaternion):
        self.orientation_quaternion = orientation_quaternion
        self.update_axis_by_quaternion(orientation_quaternion)

    def set_rotation_by_euler_angles(self, eurel_ypr):
        r = R.from_euler('zyx', eurel_ypr)
        self.orientation_quaternion = r.as_quat()

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