from abc import ABC, abstractmethod


class AbstractBuffer(ABC):
    def __init__(self):
        self._time_buffer = []

    @abstractmethod
    def get_no_samples(self):
        pass

    @abstractmethod
    def get_sample_by_id(self, id_x: int):
        pass

    @abstractmethod
    def get_buffers(self):
        pass

    @abstractmethod
    def add_point(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_last_point(self):
        pass
