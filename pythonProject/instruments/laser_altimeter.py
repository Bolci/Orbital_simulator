from tester_laser import pulse_length
from .dummy_instrument import DummyIntrument
import numpy as np
from utils import Utils


class LaserAltimeter(DummyIntrument):
    def __init__(self,
                 beam_divergence,
                 wavelenght = 1330.0,
                 speed_of_light = 3e8,
                 noise_level = 0.05 ):
        super().__init__(intrument_label="Laser_altimeter")
        self.beam_divergence = beam_divergence
        self.wavelemght = wavelenght
        self.speed_of_light = speed_of_light
        self.noise_level = noise_level

        self.pulse_length = 0

    @staticmethod
    def return_signal_streng(position, beam_radius):
        return  np.exp(-2 * (position ** 2) / (beam_radius ** 2))

    def calculate_distance_resolution(self, pulse_length):
        return (self.speed_of_light * pulse_length) / 2

    def calculate_time_of_flight(self, target_distance):
        return (2 * target_distance) / self.speed_of_light

    @staticmethod
    def get_noise(noise_level):
        return np.random.normal(0, noise_level)

    def set_measurement_parameters(self, pulse_length):
        self.pulse_length = pulse_length

    def measure(self, measured_objects):

        return_signals = []
        for measured_object in measured_objects:

            return_signal = [0, None]

            relative_position = self.parent_sattelite.get_current_position - measured_object.get_current_position
            relative_distance = Utils.norm(relative_position)
            target_distance = relative_distance * 1000 #distance in meters
            beam_radius = target_distance*self.beam_divergence

            distance_from_beam_center = 0.0


            noise = self.get_noise(self.noise_level)
            time_of_flight = self.calculate_time_of_flight(target_distance)
            signal_strength = self.return_signal_streng(distance_from_beam_center, beam_radius)
            distance_resolution = self.calculate_distance_resolution(self.pulse_length)

            if time_of_flight <= distance_resolution:
                return_signal = [signal_strength + noise, time_of_flight]

            return_signals.append(return_signal)

        return return_signals