from .abstract_buffer import AbstractBuffer
from skyfield.timelib import Time
from typing import Optional
from copy import copy
import sys
sys.path.append('../')

from utils.utils_time import UtilsTime

class TimeBuffer(AbstractBuffer):
    def __init__(self):
        super().__init__()
        self._x_vals_buffer = []
        self._y_vals_buffer = []
        self._z_vals_buffer = []

    def get_no_samples(self) -> int:
        return len(self._x_vals_buffer)

    def add_point(self, x_val: Optional, y_val: Optional, z_val: Optional, time: Time) -> None:
        self._x_vals_buffer.append(x_val)
        self._y_vals_buffer.append(y_val)
        self._z_vals_buffer.append(z_val)
        self._time_buffer.append(time)

    def get_buffers(self) -> tuple[list, list, list]:
        return self._x_vals_buffer, self._y_vals_buffer, self._z_vals_buffer

    def get_sample_by_id(self, id_x: int):
        return self._x_vals_buffer[id_x], self._y_vals_buffer[id_x],  self._z_vals_buffer[id_x]

    def get_sample_by_id_with_time(self, id_x: int):
        return {'Timestamp': copy(self._time_buffer[id_x]), 'Data': {'x_val': self._x_vals_buffer[id_x],
                                                                     'y_val': self._y_vals_buffer[id_x],
                                                                     'z_val': self._z_vals_buffer[id_x],
                                                                     }}
    def get_last_point(self):
        x_point = 0
        y_point = 0
        z_point = 0

        if self._x_vals_buffer:
            x_point = self._x_vals_buffer[-1]

        if self._y_vals_buffer:
            y_point = self._y_vals_buffer[-1]

        if self._z_vals_buffer:
            z_point = self._z_vals_buffer[-1]

        return x_point, y_point, z_point

    def get_sample_by_time(self, t: Time):
        id_sample = UtilsTime.find_id_of_closest_time(self._time_buffer, t)
        return self.get_sample_by_id_with_time(id_sample)


    def clean(self):
        self._x_vals_buffer, self._y_vals_buffer, self._z_vals_buffer  = [], [], []
        self._time_buffer = []
