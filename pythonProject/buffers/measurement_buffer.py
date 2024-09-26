from .abstract_buffer import AbstractBuffer


class MeasurementBuffer(AbstractBuffer):
    def __init__(self):
        super().__init__()
        self.measurement_buffer = []

    def get_no_samples(self):
        pass

    def get_sample_by_id(self, id_x: int):
        pass

    def get_buffers(self):
        pass

    def add_point(self, *args, **kwargs):
        pass

    def get_last_point(self):
        pass
