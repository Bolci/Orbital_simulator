from skyfield.sgp4lib import EarthSatellite
import numpy as np
from objects import Sphere
from utils import Utils
from quaternion_worker import QuaternionMath
from scipy.spatial.transform import Rotation as R
from copy import copy
from astropy import units as u
from poliastro.twobody import Orbit


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


class SatteliteWithDimension(SatteliteDummy):
    def __init__(self, label, radius):
        super().__init__(label)
        self.radius = radius
        self.satt_object = Sphere.get_planet(radius)

    def get_radius(self):
        return self.radius

    def at(self, t):
        if self.satellite_my is None:
            raise Exception("Satellite data not loaded")

        geocentric, exact_position = super().at(t)

        return geocentric, exact_position


class SatteliteObject(SatteliteWithDimension):
    def __init__(self,
                 label,
                 position_degradation_speed_km=0.2,
                 drift_speed_km_per_sec=0.01,
                 initial_uncertainty_km=1.0,
                 initial_velocity_uncertenaity_kms = 0.001,
                 radius = 0.05):
        super().__init__(label, radius)

        self.initial_velocity_uncertenaity_kms = initial_velocity_uncertenaity_kms
        self.initial_uncertainty_km = initial_uncertainty_km


        self.drift_speed_km_per_sec = drift_speed_km_per_sec
        self.position_degradation_speed_km = position_degradation_speed_km

    @staticmethod
    def sample_from_uncertainity(parameter):
        return np.random.uniform(-1, 1, size=3) * parameter

    def load_sattelite(self, tle, ts):
        super().load_sattelite(tle, ts)
        ts_now = ts.now()
        sattelite_my_now = self.satellite_my.at(ts_now)

        position_km, velocity_kmps = sattelite_my_now.position.km, sattelite_my_now.velocity.km_per_s
        position_error = self.sample_from_uncertainity(self.initial_uncertainty_km)
        velocity_error = self.sample_from_uncertainity(self.initial_velocity_uncertenaity_kms)

        print(f"position = {position_error}, velocity = {velocity_error}")
        #self.satellite_my = EarthSatellite(*tle, self.label, ts)
        #self.load_tle(tle)

    def get_tle_epoch(self):
        return self.satellite_my.epoch

    def dt_time(self, t):
        return (t.tt - self.get_tle_epoch().tt)

    '''
    def calculate_uncertainity(self, t):
        total_uncertainty_km = self.dt_time(t) * self.position_degradation_speed_km
        return max(0, total_uncertainty_km)
    '''


    def at(self, t):
        if self.satellite_my is None:
            raise Exception("Satellite data not loaded")

        tle_epoch = self.get_tle_epoch()  # Julian Date of TLE epoch

        geocentric, exact_position = super().at(t)

        #uncertainty = uncertainty_km * np.random.uniform(-1, 1, size=3)  # 3D uncertainty
        #uncertain_position = exact_position + uncertainty

        return exact_position
        return {
            'exact_position': exact_position,
            'uncertain_position': uncertain_position,
            'uncertainty_radius_km': uncertainty_km
        }


class SatteliteActive(SatteliteDummy):
    def __init__(self, label, orientation_vector = np.array((0.0,0.0,0.0, 1.0))):
        super().__init__(label, orientation_vector)

        self.sattelite_intruments = {}

    def add_intruments(self, intrument_label, instrument):
        self.sattelite_intruments[intrument_label] = instrument

    def orient_instrument_on_satellite(self, intrument_label, target_point_vector):
        target_vector = target_point_vector - self.get_current_position()
        target_vector = Utils.get_unit_vector(target_vector)  # Normalize the vector

        new_z_axis = target_vector


        new_y_axis = np.array([0, 0, 1]).astype(np.float64) # Start with the global z-axis
        if np.allclose(np.cross(new_z_axis, new_y_axis), [0, 0, 0]):
            new_y_axis = np.array([0, 1, 0])

        new_x_axis = np.cross(new_y_axis, new_z_axis)
        new_x_axis /= np.linalg.norm(new_x_axis)

        new_y_axis = np.cross(new_z_axis, new_x_axis)
        new_y_axis /= np.linalg.norm(new_y_axis)

        self.x_axis = new_x_axis
        self.y_axis = new_y_axis
        self.z_axis = new_z_axis

        #measured_intrument = self.sattelite_intruments[intrument_label]
        #intrument_unic_vec = Utils.get_unit_vector(measured_intrument.relative_orientation_to_sattelite_vec)

        #rotation_axis = np.cross(target_vector, intrument_unic_vec)
        #rotation_axis = Utils.get_unit_vector(rotation_axis)
        #rotation_angle = np.arccos(np.dot(intrument_unic_vec, target_vector))

        #rotation_quaternion = QuaternionMath.create_quaternion(rotation_axis, rotation_angle)
        #new_rotation = QuaternionMath.rotate_vector_by_quaternion(self.orientation_vector, rotation_quaternion)

        #self.orientation_quaternion = rotation_quaternion
        #self.update_axis_by_quaternion(rotation_quaternion)


    def at(self, t):
        if self.satellite_my is None:
            raise Exception("Satellite data not loaded")

        [geocentric, exact_position] = super().at(t)

        return exact_position

    def perform_measurements(self, data_from_objects):
        measured_data = {}
        for label, instrument in self.sattelite_intruments.items():
            measured_data[instrument.intrument_label] = instrument.measure(data_from_objects)

        return measured_data
