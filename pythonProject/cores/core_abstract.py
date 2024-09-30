from sattelites.sattelite_active import SatteliteActive
from sattelites.sattelite_object import SatteliteObject


class CoreAbstract:
    def __init__(self):
        self.sattelite_active = None
        self.dummy_sattelites = None

    def set_sattelites(self, active_sattelite: SatteliteActive, dummy_dattelites: list[SatteliteObject]):
        self.sattelite_active = active_sattelite
        self.dummy_sattelites = dummy_dattelites