import sys

sys.path.append("../")

from .core_abstract import CoreAbstract
from skyfield.timelib import Time
from copy import copy
import sys

sys.path.append('../')

from utils.utils_time import UtilsTime


class SimulationCore(CoreAbstract):
    def __init__(self, data_buffer):
        super().__init__()
        self.data_buffer = data_buffer

    def do_one_time_loop(self, t: Time):
        self.sattelite_active.at(t)
        _ = [single_dummy.at(t) for single_dummy in self.dummy_sattelites]

        measured_data = self.sattelite_active.perform_measurements(self.dummy_sattelites)
        self.data_buffer.add_point(measured_data, copy(t))

        return measured_data

    def perform_simulation(self, time_range, counter_max = 300):
        counter = 0
        is_oriented_flag = 0

        for id_t, t in enumerate(time_range):

            if is_oriented_flag < 1:
                _, sattelite_dummy_possition = self.dummy_sattelites[0].at_raw(t)
                self.sattelite_active.orient_instrument_on_satellite('Camera', sattelite_dummy_possition)
            is_oriented_flag += 1

            _, point = self.do_one_time_loop(t)

            if counter >= counter_max:
                break
            counter += 1

        return self.data_buffer,
