import sys

from numpy.lib.function_base import extract

sys.path.append("../")

from sattelites.sattelite_active import SatteliteActive
from sattelites.sattelite_object import SatteliteObject
from skyfield.timelib import Time


class SimulationCore:
    def __init__(self, data_buffer):

        self.sattelite_active = None
        self.dummy_sattelites = None

        self.data_buffer = data_buffer

    def set_sattelites(self, active_sattelite: SatteliteActive, dummy_dattelites: list[SatteliteObject]):
        self.sattelite_active = active_sattelite
        self.dummy_sattelites = dummy_dattelites

    def do_one_time_loop(self, t: Time):
        self.sattelite_active.at(t)
        _ = [single_dummy.at(t) for single_dummy in self.dummy_sattelites]

        measured_data = self.sattelite_active.perform_measurements(self.dummy_sattelites)
        self.data_buffer.add_point(measured_data)

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

        return self.data_buffer
