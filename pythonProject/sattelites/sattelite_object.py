from .sattelite_with_dimensions import SatteliteWithDimension
import numpy as np
import sys
from skyfield.timelib import Time
from numpy.typing import NDArray
sys.path.append('../')

from tle_worker import TLEWorker

class SatteliteObject(SatteliteWithDimension):
    def __init__(self,
                 label: str,
                 position_degradation_speed_km:float = 0.2,
                 drift_speed_km_per_sec:float = 0.01,
                 initial_uncertainty_km:float = 1.0,
                 initial_velocity_uncertenaity_kms:float = 0.001,
                 radius:float = 0.05) -> None:
        super().__init__(label, radius)

        self.initial_velocity_uncertenaity_kms = initial_velocity_uncertenaity_kms
        self.initial_uncertainty_km = initial_uncertainty_km

        self.drift_speed_km_per_sec = drift_speed_km_per_sec
        self.position_degradation_speed_km = position_degradation_speed_km

        self.tle_true = None
        self.satellite_my_true = None

    @staticmethod
    def sample_from_uncertainity(parameter) -> NDArray:
        return np.random.uniform(-1, 1, size=3) * parameter

    def load_sattelite(self, tle: list[str, str], ts: Time) -> None:
        super().load_sattelite(tle, ts)
        #ts_now = ts.now()
        #sattelite_my_now = self.satellite_my.at(ts_now)
        #position_km, velocity_kmps = sattelite_my_now.position.km, sattelite_my_now.velocity.km_per_s
        #position_error = self.sample_from_uncertainity(self.initial_uncertainty_km)
        #velocity_error = self.sample_from_uncertainity(self.initial_velocity_uncertenaity_kms)
        #initial_error_position = position_error + position_km
        #initial_error_vector = velocity_error + velocity_kmps
        #mu_earth = 398600.4418
        #r_earth = 6378.1363
        #mean_motion_rev_per_day = self.satellite_my.model.nm
        #mean_motion_rad_per_sec = mean_motion_rev_per_day * (2 * np.pi) / (24 * 3600)
        # Calculate the semi-major axis using the mean motion
        #semi_major_axis = (mu_earth / (mean_motion_rad_per_sec ** 2)) ** (1 / 3)
        #current_speed = np.sqrt(mu_earth * (2 / initial_error_position - 1 / semi_major_axis))
        #print(current_speed)
        #r = initial_error_position * u.km
        #v = velocity_kmps * u.km / u.s
        # Create an orbit object using the true position and velocity relative to Earth
        #orbit = Orbit.from_vectors(Earth, r, v)
        #print(f"Position: {r}, Velocity: {v}")
        #r = np.array([r[0].to_value(u.km), r[1].to_value(u.km), r[2].to_value(u.km)])
        #v = np.array([v[0].to_value(u.km / u.s), v[1].to_value(u.km / u.s), v[2].to_value(u.km / u.s)])
        #orbital_energy = (Utils.norm(v) ** 2 / 2) - (mu_earth / Utils.norm(r))
        #print(F"orbital energy {orbital_energy}")
        #print(orbit.a, orbit.ecc, orbit.inc)
        #tle_creator = TLEWorker()
        #generated_tle = tle_creator.generate_tle_from_orbit_object(orbit)
        #print(generated_tle)
        #self.tle_true = generated_tle
        #self.satellite_my_true = EarthSatellite(*generated_tle, "_true", ts)

    @property
    def get_tle_epoch(self):
        return self.satellite_my.epoch

    def dt_time(self, t: Time):
        return (t.tt - self.get_tle_epoch().tt)


    def at(self, t: Time) -> NDArray:
        if self.satellite_my is None:
            raise Exception("Satellite data not loaded")

        #if self.satellite_my_true is None:
        #    raise Exception("True sattelite data are not generated")
        #new_t = copy(t)
        _, expected_position = super().at(t)
        #exact_position = self.satellite_my_true.at(new_t).position.km

        #geocentric = self.satellite_my_true.at(new_t)
        #exact_position = geocentric.position.km
        return expected_position
