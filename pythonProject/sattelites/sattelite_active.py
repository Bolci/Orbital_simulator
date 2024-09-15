from skyfield.sgp4lib import EarthSatellite
import numpy as np
from utils import Utils
from .sattelite_dummy import SatteliteDummy


class SatteliteActive(SatteliteDummy):
    def __init__(self, label, orientation_vector = np.array((0.0,0.0,0.0, 1.0))):
        super().__init__(label, orientation_vector)

        self.sattelite_intruments = {}
        self.sattelite_instruments_orientation = {}

    def add_intruments(self, intrument_label, instrument):
        self.sattelite_intruments[intrument_label] = instrument

    def set_intrument_orientation_relative_to_sattelite(self, intrument_label, orientation_vector):
        self.sattelite_instruments_orientation[intrument_label] = orientation_vector

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
