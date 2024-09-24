import numpy as np
from utils import Utils
from .sattelite_dummy import SatteliteDummy
from skyfield.timelib import Time
from typing import Optional
from numpy.typing import NDArray


class SatteliteActive(SatteliteDummy):
    def __init__(self, label: str) -> None:
        super().__init__(label)

        self.sattelite_intruments = {}
        self.instrument_orientation_with_respect_to_global = {}


    def add_intruments(self, intrument_label: str, instrument: Optional) -> None:
        self.sattelite_intruments[intrument_label] = instrument

    def set_intrument_orientation_relative_to_sattelite(self,
                                                        intrument_label: str,
                                                        orientation_vector: NDArray) -> None:
        self.sattelite_intruments[intrument_label].set_orientation_to_parent_sattelite_vec(orientation_vector)
        self.instrument_orientation_with_respect_to_global[intrument_label] = np.dot(self.rotation_matrix, orientation_vector)

    def orient_instrument_on_satellite(self, intrument_label: str,
                                       target_point_vector: NDArray) -> None:
        sattelite_location = self.get_current_position
        intrument_local_orienation = self.sattelite_intruments[intrument_label].relative_orientation_to_sattelite_vec

        current_rotation, d_rotation = Utils.update_orientation(sattelite_location,
                                                                target_point_vector,
                                                                intrument_local_orienation,
                                                                self.rotation_matrix)

        self.rotation_matrix = current_rotation

        self.instrument_orientation_with_respect_to_global[intrument_label] = \
            np.dot(d_rotation, self.instrument_orientation_with_respect_to_global[intrument_label])

        self.update_rotation_by_r_matric(d_rotation)


    def at(self, t: Time) -> NDArray:
        if self.satellite_my is None:
            raise Exception("Satellite data not loaded")

        [geocentric, exact_position] = super().at(t)

        return exact_position

    def perform_measurements(self, data_from_objects: list) -> dict[str, Optional]:
        measured_data = {}
        for label, instrument in self.sattelite_intruments.items():
            measured_data[instrument.intrument_label] = instrument.measure(data_from_objects)

        return measured_data
