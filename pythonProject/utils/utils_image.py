from numpy.typing import NDArray
import cv2


class ImageUtils:
    @staticmethod
    def get_center_of_image(image: NDArray) -> tuple[int, int]:
        moments = cv2.moments(image, binaryImage=True)
        x_center = int(moments['m10'] / moments['m00'])
        y_center = int(moments['m01'] / moments['m00'])

        return x_center, y_center