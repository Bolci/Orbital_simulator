import sys

import matplotlib.pyplot as plt
import numpy as np
from typing import Optional

sys.path.append('../')

from buffers.measurement_buffer import MeasurementBuffer
from numpy.typing import NDArray
from utils.utils_image import ImageUtils
from .core_abstract import CoreAbstract
from data_processors.lamber_solver import LambertSolver
from skyfield.timelib import Time
from exceptions.exceptions import SamplingException

class ProcessingCore(CoreAbstract):
    def __init__(self, ):
        super().__init__()

    @staticmethod
    def get_overlapped_image(image_data: list[NDArray]):
        overlapped_image = np.sum(image_data, axis=0)
        overlapped_image = np.clip(overlapped_image,0,255)
        return overlapped_image

    @staticmethod
    def process_images(image_data):
        for single_image in image_data:
            x_center,y_center = ImageUtils.get_center_of_image(single_image)

            plt.figure()
            plt.imshow(single_image)

            break

        return []

    def calculate_possition_from_image(self, data: dict[Optional], measurement_setup: dict[Optional]):
        pass


    def process_data(self,
                     measurement_buffer: MeasurementBuffer):

        time_sample = measurement_buffer._time_buffer[3]

        measurement_setup_report = self.sattelite_active.get_report_by_time(time_sample)
        data_in_time = measurement_buffer.get_sample_by_time(time_sample)

        if not (measurement_setup_report['Timestamp'] == data_in_time['Timestamp']):
            raise SamplingException('Timestamp for report and data are not the same')

        self.calculate_possition_from_image(data_in_time, measurement_setup_report)

        measured_data_all = measurement_buffer.get_reorganized_buffer()
        measured_data_all['Camera'] = measured_data_all['Camera']

        overlapped_image = self.get_overlapped_image(measured_data_all['Camera'])
        data = self.process_images(measured_data_all['Camera'])

        return {"Overlapped_image": overlapped_image}
