import numpy as np
from utils import Utils
from .sattelite_dummy import SatteliteDummy


class SatteliteActive(SatteliteDummy):
    def __init__(self, label):
        super().__init__(label)

        self.sattelite_intruments = {}
        self.instrument_orientation_with_respect_to_global = {}


    def add_intruments(self, intrument_label, instrument):
        self.sattelite_intruments[intrument_label] = instrument

    def set_intrument_orientation_relative_to_sattelite(self, intrument_label, orientation_vector):
        self.sattelite_intruments[intrument_label].set_orientation_to_parent_sattelite_vec(orientation_vector)
        self.instrument_orientation_with_respect_to_global[intrument_label] = np.dot(self.rotation_matrix, orientation_vector)

    def orient_instrument_on_satellite(self, intrument_label, target_point_vector):
        sattelite_location = self.get_current_position()
        intrument_local_orienation = self.sattelite_intruments[intrument_label].relative_orientation_to_sattelite_vec

        current_rotation, d_rotation = Utils.update_orientation(sattelite_location,
                                                                target_point_vector,
                                                                intrument_local_orienation,
                                                                self.rotation_matrix)

        self.rotation_matrix = current_rotation

        self.instrument_orientation_with_respect_to_global[intrument_label] = \
            np.dot(d_rotation, self.instrument_orientation_with_respect_to_global[intrument_label])

        self.update_rotation_by_r_matric(d_rotation)




        '''
        new_z_axis = target_vector

        new_y_axis = np.array([0, 0, 1]).astype(np.float64) # Start with the global z-axis
        if np.allclose(np.cross(new_z_axis, new_y_axis), [0, 0, 0]):
            new_y_axis = np.array([0, 1, 0])

        new_x_axis = np.cross(new_y_axis, new_z_axis)
        new_x_axis /= np.linalg.norm(new_x_axis)

        new_y_axis = np.cross(new_z_axis, new_x_axis)
        new_y_axis /= np.linalg.norm(new_y_axis)
        '''

        #self.x_axis = new_x_axis
        #self.y_axis = new_y_axis
        #self.z_axis = new_z_axis

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
