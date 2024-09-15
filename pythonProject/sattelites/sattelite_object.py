from .sattelite_with_dimensions import SatteliteWithDimension
import numpy as np
from astropy import units as u
from poliastro.twobody import Orbit
from poliastro.bodies import Earth


class SatteliteObject(SatteliteWithDimension):
    def __init__(self,
                 label,
                 position_degradation_speed_km=0.2,
                 drift_speed_km_per_sec=0.01,
                 initial_uncertainty_km=1.0,
                 initial_velocity_uncertenaity_kms = 0.001,
                 radius = 0.05):
        super().__init__(label, radius)

        self.initial_velocity_uncertenaity_kms = initial_velocity_uncertenaity_kms
        self.initial_uncertainty_km = initial_uncertainty_km


        self.drift_speed_km_per_sec = drift_speed_km_per_sec
        self.position_degradation_speed_km = position_degradation_speed_km

    @staticmethod
    def sample_from_uncertainity(parameter):
        return np.random.uniform(-1, 1, size=3) * parameter

    def load_sattelite(self, tle, ts):
        super().load_sattelite(tle, ts)
        ts_now = ts.now()
        sattelite_my_now = self.satellite_my.at(ts_now)

        position_km, velocity_kmps = sattelite_my_now.position.km, sattelite_my_now.velocity.km_per_s
        position_error = self.sample_from_uncertainity(self.initial_uncertainty_km)
        velocity_error = self.sample_from_uncertainity(self.initial_velocity_uncertenaity_kms)

        initial_error_position = position_error + position_km
        initial_error_vector = velocity_error + velocity_kmps

        r = initial_error_position * u.km
        v = initial_error_vector * u.km / u.s

        # Create an orbit object using the true position and velocity relative to Earth
        orbit = Orbit.from_vectors(Earth, r, v)

        #tle_creator = T
        #generated_tle =


    def get_tle_epoch(self):
        return self.satellite_my.epoch

    def dt_time(self, t):
        return (t.tt - self.get_tle_epoch().tt)

    '''
    def calculate_uncertainity(self, t):
        total_uncertainty_km = self.dt_time(t) * self.position_degradation_speed_km
        return max(0, total_uncertainty_km)
    '''


    def at(self, t):
        if self.satellite_my is None:
            raise Exception("Satellite data not loaded")

        tle_epoch = self.get_tle_epoch()  # Julian Date of TLE epoch

        geocentric, exact_position = super().at(t)

        #uncertainty = uncertainty_km * np.random.uniform(-1, 1, size=3)  # 3D uncertainty
        #uncertain_position = exact_position + uncertainty

        return exact_position
        return {
            'exact_position': exact_position,
            'uncertain_position': uncertain_position,
            'uncertainty_radius_km': uncertainty_km
        }
