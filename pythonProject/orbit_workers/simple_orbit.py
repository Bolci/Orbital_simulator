import numpy as np
from skyfield.timelib import Time
import sys

sys.path.append("../")

from time_buffer import TimeBuffer


class SimpleOrbit(TimeBuffer):
    def __init__(self):
        super().__init__()

    def get_orbit(self):
        return super().get_buffers()
