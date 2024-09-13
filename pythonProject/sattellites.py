from skyfield.sgp4lib import EarthSatellite
import numpy as np
from objects import Sphere


class SatteliteDummy:
    def __init__(self, label):
        self.label = label

        self.tle_elem = None
        self.satellite_my = None

        self.position_vector = None

    def set_current_position(self, position_vector):
        self.position_vector = position_vector

    def get_current_position(self):
        return self.position_vector

    def load_sattelite(self, tle, ts):
        self.satellite_my = EarthSatellite(*tle, self.label, ts)
        self.load_tle(tle)

    def load_tle(self, tle):
        self.tle_elem = tle

    def at(self, t):
        if self.satellite_my is None:
            raise Exception("Satellite data not loaded")

        geocentric = self.satellite_my.at(t)
        exact_position = geocentric.position.km

        self.position_vector = exact_position

        return geocentric, exact_position

    def __call__(self):
        return self.satellite_my


class SatteliteWithDimension(SatteliteDummy):
    def __init__(self, label, radius):
        super().__init__(label)
        self.radius = radius
        self.satt_object = Sphere.get_planet(radius)

    def get_radius(self):
        return self.radius

    def at(self, t):
        if self.satellite_my is None:
            raise Exception("Satellite data not loaded")

        geocentric, exact_position = super().at(t)

        return exact_position


class SatteliteObject(SatteliteDummy):
    def __init__(self,
                 label,
                 position_degradation_speed_km=0.2,
                 drift_speed_km_per_sec=0.01,
                 initial_uncertainty_km=1.0):
        super().__init__(label)

        self.position_degradation_speed_km = position_degradation_speed_km

        self.drift_speed_km_per_sec = drift_speed_km_per_sec
        self.initial_uncertainty_km = initial_uncertainty_km
        self.drift_velocity = np.random.uniform(-1, 1, size=3) * self.drift_speed_km_per_sec

        self.initialized = False
        self.initial_position_error = None

    def get_tle_epoch(self):
        return self.satellite_my.epoch

    def dt_time(self, t):
        return (t.tt - self.get_tle_epoch().tt)

    def calculate_uncertainity(self, t):
        total_uncertainty_km = self.dt_time(t) * self.position_degradation_speed_km
        return max(0, total_uncertainty_km)

    def sample_initial_position_error(self):
        u = np.random.uniform(0, 1)
        v = np.random.uniform(0, 1)
        theta = 2 * np.pi * u
        phi = np.arccos(2 * v - 1)
        r = self.initial_uncertainty_km * (np.random.uniform(0, 1) ** (1 / 3))  # Uniform distribution in a sphere

        x = r * np.sin(phi) * np.cos(theta)
        y = r * np.sin(phi) * np.sin(theta)
        z = r * np.cos(phi)
        return np.array([x, y, z])

    def at(self, t):
        if self.satellite_my is None:
            raise Exception("Satellite data not loaded")

        uncertainty_km = self.calculate_uncertainity(t)
        tle_epoch = self.get_tle_epoch()  # Julian Date of TLE epoch

        [geocentric, exact_position] = super().at(t)

        uncertainty = uncertainty_km * np.random.uniform(-1, 1, size=3)  # 3D uncertainty
        uncertain_position = exact_position + uncertainty

        return {
            'exact_position': exact_position,
            'uncertain_position': uncertain_position,
            'uncertainty_radius_km': uncertainty_km
        }


class SatteliteActive(SatteliteDummy):
    def __init__(self, label):
        super().__init__(label)

        self.sattelite_intruments = []

    def add_intruments(self, instruments):
        self.sattelite_intruments.append(instruments)

    def at(self, t):
        if self.satellite_my is None:
            raise Exception("Satellite data not loaded")

        [geocentric, exact_position] = super().at(t)

        return exact_position

    def perform_measurements(self, data_from_objects):
        return [x.measure(data_from_objects)
                for x in self.sattelite_intruments]
