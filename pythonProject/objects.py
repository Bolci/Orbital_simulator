import numpy as np
from skyfield.api import load


class Sphere:

    @staticmethod
    def get_planet(planet_radius):
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)

        x_planet = planet_radius * np.outer(np.cos(u), np.sin(v))
        y_planet = planet_radius * np.outer(np.sin(u), np.sin(v))
        z_planet = planet_radius * np.outer(np.ones(np.size(u)), np.cos(v))

        return x_planet, y_planet, z_planet

    @staticmethod
    def get_sphere_with_in_diff_coordinates(planet_radius, x, y, z):
        x_p, y_p, z_p = Sphere.get_planet(planet_radius)
        x_p += x
        y_p += y
        z_p += z

        return x_p, y_p, z_p


class Sun:
    def __init__(self):
        self.sun = load('de421.bsp')['sun']

    def get_sun_position(self, t):
        return self.sun.at(t).position.km

    def get_relative_position_to_sun(self, t, sattelite_position):
        sun_position = self.get_sun_position(t)
        return sun_position - sattelite_position