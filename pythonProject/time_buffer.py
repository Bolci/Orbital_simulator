from skyfield.timelib import Time


class TimeBuffer:
    def __init__(self):
        self._x_vals_buffer = []
        self._y_vals_buffer = []
        self._z_vals_buffer = []
        self._time_history_buffer = []

    def get_no_samples(self):
        return len(self._x_vals_buffer)

    def add_point(self, x_val: float, y_val: float, z_val: float, time: Time):
        self._x_vals_buffer.append(x_val)
        self._y_vals_buffer.append(y_val)
        self._z_vals_buffer.append(z_val)
        self._time_history_buffer.append(time)

    def get_buffers(self):
        return self._x_vals_buffer, self._y_vals_buffer, self._z_vals_buffer

    def get_sample_by_id(self, id_x):
        return self._x_vals_buffer[id_x], self._y_vals_buffer[id_x],  self._z_vals_buffer[id_x]

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