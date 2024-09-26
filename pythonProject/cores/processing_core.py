import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.append('../')

from buffers.measurement_buffer import MeasurementBuffer
from numpy.typing import NDArray
from utils.utils_image import ImageUtils


class ProcessingCore:
    def __init__(self, ):
        pass

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

    def process_data(self, measurement_buffer: MeasurementBuffer):
        measured_data_all = measurement_buffer.get_reorganized_buffer()
        measured_data_all['Camera'] = measured_data_all['Camera'][2:]

        overlapped_image = self.get_overlapped_image(measured_data_all['Camera'])
        data = self.process_images(measured_data_all['Camera'])

        return {"Overlapped_image": overlapped_image}
