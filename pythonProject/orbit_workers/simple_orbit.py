import numpy as np


class SimpleOrbit:
    def __init__(self):
        self._x_vals_buffer = []
        self._y_vals_buffer = []
        self._z_vals_buffer = []


    def add_point(self, x_val: float, y_val: float, z_val: float):
        self._x_vals_buffer.append(x_val)
        self._y_vals_buffer.append(y_val)
        self._z_vals_buffer.append(z_val)

    def get_last_point(self):
        x_point = 0
        y_point = 0
        z_point = 0

        if not self._x_vals_buffer:
            x_point = self._x_vals_buffer[-1]

        if not self._y_vals_buffer:
            y_point = self._y_vals_buffer[-1]

        if not self._z_vals_buffer:
            z_point = self._z_vals_buffer[-1]

        return x_point, y_point, z_point
