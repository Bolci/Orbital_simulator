from .dummy_instrument import DummyIntrument


class LaserAltimeter(DummyIntrument):
    def __init__(self):
        super().__init__(intrument_label="Laser_altimeter")

    def measure(self, data_from_objects):
        pass
