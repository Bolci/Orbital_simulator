import numpy as np
from datetime import datetime, timedelta
from skyfield.api import load
from astropy import units as u
from poliastro.twobody import Orbit
from poliastro.bodies import Earth


class TLEWorker:
  def __init__(self, mu_earth = 398600.4418,
               r_earth = 6378.1363):
    self.mu_earth = mu_earth
    self.r_earth = r_earth

  @staticmethod
  def orbital_period(semi_major_axis, mu):
    return 2 * np.pi * np.sqrt(semi_major_axis ** 3 / mu)

  @staticmethod
  def mean_motion(orbital_period):
    return 86400 / orbital_period

  @staticmethod
  def get_epoch(fraction_of_day = 0.0):
    now = datetime.utcnow()

    #move in time
    seconds_to_subtract = fraction_of_day * 86400
    new_time = now - timedelta(seconds=seconds_to_subtract)

    year = now.year % 100
    start_of_year = datetime(now.year, 1, 1)
    day_of_year = (now - start_of_year).days + 1
    epoch = f"{year:02d}{day_of_year:03d}.{int((now.hour * 3600 + now.minute * 60 + now.second) / 86400 * 1000000):06d}"
    return epoch

  @staticmethod
  def get_sattelite_from_cataloque(stations_url = 'http://celestrak.com/NORAD/elements/stations.txt', sattelite_key = 'ISS (ZARYA)'):
    satellites = load.tle_file(stations_url)
    satellite_iss = {sat.name: sat for sat in satellites}[sattelite_key]

    return satellite_iss


  def generate_tle_from_orbit_object(self, orbit):
    # Extract the classical orbital elements


    altitude = orbit.a.to_value(u.km) - self.r_earth
    print(altitude)
    eccentricity = orbit.ecc
    inclination = orbit.inc.to_value(u.deg)
    raan = orbit.raan.to_value(u.deg)
    argp = orbit.argp.to_value(u.deg)
    #true_anomaly = orbit.nu.to_value(u.deg)

    [line1, line2] = self.generate_tle(altitude=altitude,
                                       inclination=inclination,
                                       raan=raan,
                                       eccentricity=eccentricity)
    return [line1, line2]

  def generate_tle(self,
                   altitude,
                   inclination,
                   raan,
                   eccentricity = 0,
                   mean_motion_derivative = 0.0,
                   mean_motion_sec_derivative = 0.0,
                   bstar = 0.0,
                   omega = 0.0,
                   nu = 0.0,
                   satellite_number = 99999,
                   element_set_number = 999,
                   classification = 'U',
                   international_designator = '2022-999A'):

    semi_major_axis = self.r_earth + altitude

    T = self.orbital_period(semi_major_axis, self.mu_earth) # Orbital period
    mean_motion = self.mean_motion(T) # Mean motion (revs per day)
    epoch = self.get_epoch() # Epoch (current time)

    line1 = f"1 {satellite_number:05d}{classification} {international_designator} {epoch} {mean_motion_derivative:.8f} {mean_motion_sec_derivative:.8f} {bstar:.8f} 0 {element_set_number:04d}"
    line2 = f"2 {satellite_number:05d} {np.degrees(inclination):8.4f} {np.degrees(raan):8.4f} {eccentricity:07.0f} {omega:8.4f} {nu:8.4f} {mean_motion:11.8f} 00001"

    return [line1, line2]
