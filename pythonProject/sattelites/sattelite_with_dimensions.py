from .sattelite_dummy import SatteliteDummy
import sys

sys.path.append("../")
from objects import Sphere


class SatteliteWithDimension(SatteliteDummy):
    def __init__(self, label, radius):
        super().__init__(label)
        self.radius = radius
        self.satt_object = Sphere.get_planet(radius)

    @property
    def get_radius(self):
        return self.radius

    def at(self, t):
        if self.satellite_my is None:
            raise Exception("Satellite data not loaded")

        geocentric, exact_position = super().at(t)

        return geocentric, exact_position