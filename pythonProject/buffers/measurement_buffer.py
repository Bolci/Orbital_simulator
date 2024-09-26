from .abstract_buffer import AbstractBuffer
import sys

sys.path.append("../")

from utils.utils_general import UtilsGeneral

class MeasurementBuffer(AbstractBuffer):
    def __init__(self):
        super().__init__()
        self.measurement_buffer = []

    def get_no_samples(self):
        return len(self.measurement_buffer)

    def get_sample_by_id(self, id_x: int):
        return self.measurement_buffer[id_x]

    def get_buffers(self):
        return self.measurement_buffer

    def add_point(self, measurement_values):
        self.measurement_buffer.append(measurement_values)

    def get_last_point(self):
        return_val = self.measurement_buffer[-1] if self.measurement_buffer else [0]
        return return_val

    def get_reorganized_buffer(self):
        return UtilsGeneral.convert_list_of_dicts_to_dicts_of_list(self.measurement_buffer)
