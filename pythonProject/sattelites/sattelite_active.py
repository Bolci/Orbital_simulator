import numpy as np
from utils.utils_vector import Utils
from .sattelite_dummy import SatteliteDummy
from skyfield.timelib import Time
from typing import Optional
from numpy.typing import NDArray
from copy import copy
import sys
sys.path.append("../")
from buffers.time_buffer import TimeBuffer


class SatteliteActive(SatteliteDummy):
    def __init__(self, label: str) -> None:
        super().__init__(label)

        self.sattelite_intruments = {}
        self._orientation_buffer = TimeBuffer()

    def add_intruments(self, intrument_label: str, instrument: Optional) -> None:
        self.sattelite_intruments[intrument_label] = instrument

    @property
    def orientation_buffer(self):
        return self._orientation_buffer

    def set_intrument_orientation_relative_to_sattelite(self,
                                                        intrument_label: str,
                                                        orientation_vector: NDArray) -> None:
        self.sattelite_intruments[intrument_label].set_orientation_to_parent_sattelite_vec(orientation_vector)

    def orient_instrument_on_satellite(self, intrument_label: str,
                                       target_point_vector: NDArray) -> None:
        sattelite_location = self.get_current_position
        intrument_local_orienation = self.sattelite_intruments[intrument_label].relative_orientation_to_sattelite_vec

        current_rotation, d_rotation = Utils.update_orientation(sattelite_location,
                                                                target_point_vector,
                                                                intrument_local_orienation,
                                                                self.rotation_matrix)
        self.rotation_matrix = current_rotation
        self.update_rotation_by_r_matric(d_rotation)

    def get_report_by_time(self, time: Time):
        sample = super().get_report_by_time(time)
        
        orientation_sample = self._orientation_buffer.get_sample_by_time(time)
        sample['Satellite_orientation'] = orientation_sample
        instruments_orientation = {}

        for label, instrument in self.sattelite_intruments.items():
            instruments_orientation[label] = instrument.get_orientation_to_parent_sattelite_vec()

        sample['Instruments_orientation'] = instruments_orientation
        return sample



    def at(self, t: Time) -> NDArray:
        if self.satellite_my is None:
            raise Exception("Satellite data not loaded")

        [_, exact_position] = super().at(t)

        self._orientation_buffer.add_point(self.x_axis, self.y_axis, self.z_axis, copy(t))

        return exact_position

    def perform_measurements(self, data_from_objects: list) -> dict[str, Optional]:
        measured_data = {}
        for label, instrument in self.sattelite_intruments.items():
            measured_data[instrument.intrument_label] = instrument.measure(data_from_objects)
        return measured_data
