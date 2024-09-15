from .dummy_instrument import DummyIntrument
import numpy as np


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

    @staticmethod
    def return_signal_strengt(position, beam_radius):
        return  np.exp(-2 * (position ** 2) / (beam_radius ** 2))

    def calculate_object_resolution(self, pulse_length):
        return (self.speed_of_light * pulse_length) / 2

    def calculate_time_of_flight(self, target_distance):
        time_of_flight = (2 * target_distance) / self.speed_of_light

    def measure(self, measured_objects):
        for measured_object in measured_objects:
            pass

