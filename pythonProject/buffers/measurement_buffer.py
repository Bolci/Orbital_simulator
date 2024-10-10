from skyfield.timelib import Time
from .abstract_buffer import AbstractBuffer
from copy import copy
import sys

sys.path.append("../")
from utils.utils_general import UtilsGeneral
from utils.utils_time import UtilsTime


class MeasurementBuffer(AbstractBuffer):
    def __init__(self):
        super().__init__()
        self._measurement_buffer = []

    def get_no_samples(self):
        return len(self._measurement_buffer)

    def get_sample_by_id(self, id_x: int):
        return self._measurement_buffer[id_x]

    def get_sample_by_id_with_time(self, id_x: int):
        return {'Timestamp': copy(self._time_buffer[id_x]), 'Data': self._measurement_buffer[id_x]}

    def get_buffers(self):
        return self._measurement_buffer, self._time_buffer

    def add_point(self, measurement_values, time_val: Time):
        self._measurement_buffer.append(measurement_values)
        self._time_buffer.append(time_val)

    def get_last_point(self):
        return self.get_sample_by_id(-1)

    def get_value_by_time(self, ):
        print(self._time_buffer)

    def get_reorganized_buffer(self):
        return UtilsGeneral.convert_list_of_dicts_to_dicts_of_list(self._measurement_buffer)

    def get_sample_by_time(self, t: Time):
        id_sample = UtilsTime.find_id_of_closest_time(self._time_buffer, t)
        return self.get_sample_by_id_with_time(id_sample)

    def clean(self):
        self._measurement_buffer = []
        self._time_buffer = []
