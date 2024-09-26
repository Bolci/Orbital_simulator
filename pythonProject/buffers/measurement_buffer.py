from .abstract_buffer import AbstractBuffer


class MeasurementBuffer(AbstractBuffer):
    def __init__(self):
        super().__init__()
        self.measurement_buffer = []

    def get_no_samples(self):
        return len(self.measurement_buffer)

    def get_sample_by_id(self, id_x: int):
        return self.measurement_buffer[id_x]

    def get_buffers(self):
        return self.measurement_buffer

    def add_point(self, measurement_values):
        self.measurement_buffer.append(measurement_values)

    def get_last_point(self):
        pass


