from abc import ABC, abstractmethod


class SatteliteAbstract(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def measure(self, data_from_objects):
        pass


class DummyIntrument(SatteliteAbstract):
    def __init__(self, intrument_label):
        self.intrument_label = intrument_label
        self.parent_sattelite = None

        self.relative_orientation_to_sattelite_vec = [0., 0., 0.]

    def assign_sattelite(self, sattelite_pointer):
        self.parent_sattelite = sattelite_pointer


    def measure(self, data_from_objects):
        pass

    def set_orientation_to_parent_sattelite_vec(self, orientation_vector):
        self.relative_orientation_to_sattelite_vec = orientation_vector

    def get_orientation_to_parent_sattelite_vec(self):
        return self.relative_orientation_to_sattelite_vec




