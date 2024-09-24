from abc import ABC, abstractmethod
from typing import Optional

import numpy as np
from numpy.typing import NDArray
import sys

sys.path.append("../")
from sattelites.sattelite_active import SatteliteActive


class SatteliteAbstract(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def measure(self, data_from_objects: Optional) -> Optional:
        pass


class DummyIntrument(SatteliteAbstract):
    def __init__(self, intrument_label: str) -> None:
        self.intrument_label = intrument_label
        self.parent_sattelite = None

        self.relative_orientation_to_sattelite_vec = np.asarray([0., 0., 0.], dtype=np.float32)

    def assign_sattelite(self, sattelite_pointer: SatteliteActive) -> None:
        self.parent_sattelite = sattelite_pointer

    def measure(self, data_from_objects: Optional) -> Optional:
        pass

    def set_orientation_to_parent_sattelite_vec(self, orientation_vector: NDArray) -> None:
        self.relative_orientation_to_sattelite_vec = orientation_vector

    def get_orientation_to_parent_sattelite_vec(self) -> NDArray:
        return self.relative_orientation_to_sattelite_vec
