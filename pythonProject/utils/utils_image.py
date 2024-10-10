import matplotlib.pyplot as plt
from numpy.typing import NDArray
import cv2
import numpy as np
from scipy.ndimage import center_of_mass


class ImageUtils:
    @staticmethod
    def get_center_of_image(image: NDArray) -> tuple[int, int]:
        x_center, y_center = None, None

        if not np.sum(image) == 0:
            y_center, x_center = center_of_mass(image)

        return x_center, y_center
