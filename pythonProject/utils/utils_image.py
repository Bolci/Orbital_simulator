from numpy.typing import NDArray
import cv2
import numpy as np


class ImageUtils:
    @staticmethod
    def get_center_of_image(image: NDArray) -> tuple[int, int]:
        x_center, y_center = None, None

        if not np.sum(image) == 0:
            moments = cv2.moments(image, binaryImage=True)
            x_center = int(moments['m10'] / moments['m00'])
            y_center = int(moments['m01'] / moments['m00'])

        return x_center, y_center