from .dummy_instrument import DummyIntrument
import numpy as np
from utils.utils_vector import Utils


class LaserAltimeter(DummyIntrument):
    def __init__(self,
                 beam_divergence,
                 wavelenght = 1330.0,
                 speed_of_light = 3e8):
        super().__init__(intrument_label="Laser_altimeter")
        self.beam_divergence = beam_divergence
        self.wavelemght = wavelenght
        self.speed_of_light = speed_of_light
        self._pulse_length = 0

    @property
    def pulse_length(self):
        return self._pulse_length

    @pulse_length.setter
    def pulse_length(self, pl):
        self._pulse_length = pl

    def calculate_distance_resolution(self, pulse_length):
        return (self.speed_of_light * pulse_length) / 2

    def calculate_time_of_flight(self, target_distance):
        return (2 * target_distance) / self.speed_of_light

    def get_noise(self):
        noise_level = self._pulse_length # get noise level from the pulse lenght #TODO formula
        return np.random.normal(0, noise_level)

    def set_measurement_parameters(self, pulse_length):
        self.pulse_length = pulse_length

    def measure(self, measured_objects, *args):

        return_distances = []
        for measured_object in measured_objects:
            return_signal = 0

            relative_position = self.parent_sattelite.get_current_position - measured_object.get_current_position
            relative_distance = Utils.norm(relative_position)
            target_distance = relative_distance * 1000 #distance in meters

            noise = self.get_noise()
            time_of_flight = self.calculate_time_of_flight(target_distance)

            #distance_resolution = self.calculate_distance_resolution(self._pulse_length)

            #if time_of_flight <= distance_resolution:
            #    return_signal = time_of_flight + noise

            return_signal = time_of_flight + noise
            return_distances.append(return_signal)

        return return_distances