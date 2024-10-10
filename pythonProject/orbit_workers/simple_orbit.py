import sys

sys.path.append("../")

from buffers.time_buffer import TimeBuffer


class SimpleOrbit(TimeBuffer):
    def __init__(self):
        super().__init__()

    def get_orbit(self):
        return super().get_buffers()

    def get_first_point(self):
        return self.get_sample_by_id(0)
