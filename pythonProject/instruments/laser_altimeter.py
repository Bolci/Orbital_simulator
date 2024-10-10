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
        self._measurement_uncertanity = 1
        self.measuremet_std_dev = 1

    def set_measurement_uncertanity(self, measurement_uncertanity):
        self._measurement_uncertanity = measurement_uncertanity
        self.measuremet_std_dev = np.sqrt(self._measurement_uncertanity)

    def calculate_distance_resolution(self, pulse_length):
        return (self.speed_of_light * pulse_length) / 2

    def calculate_time_of_flight(self, target_distance):
        return (2 * target_distance) / self.speed_of_light

    def get_noise(self):
        return np.random.normal(0, self.measuremet_std_dev, 1)

    def set_measurement_parameters(self, pulse_length):
        self.pulse_length = pulse_length

    def measure(self, measured_objects, *args):

        return_distances = []
        for measured_object in measured_objects:

            relative_position = self.parent_sattelite.get_current_position - measured_object.get_current_position
            relative_distance = Utils.norm(relative_position)
            target_distance = relative_distance  #distance in meters
            #return_signal = [target_distance]

            return_signal = target_distance + self.get_noise()

            return_distances.append(return_signal)

        return return_distances
