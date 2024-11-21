import numpy as np
from numpy.typing import NDArray
from utils.utils_vector import Utils


class UtilsCamera:

    @staticmethod
    def pixel_to_los(pixel_coords,
                     camera_intrinsics):
        #expected that camera is pointing towards zaxis derection

        fx, fy, cx, cy = camera_intrinsics
        x,y = pixel_coords

        if x == None:
            x = 0
            y = 0

        norm_x = (x - cx) / fx
        norm_y = (y - cy) / fy
        los_camera_frame = np.asarray([norm_x, norm_y, 1])
        los_camera_frame = Utils.get_unit_vector(los_camera_frame)

        return los_camera_frame

    @staticmethod
    def transform_to_inertial(los_camera, rotation_matrix = np.eye(3)):
        """
        Transform LOS vector from the camera frame to the inertial frame.
        :param los_camera: Line-of-sight vector in the camera frame
        :param rotation_matrix: 3x3 rotation matrix from camera to inertial frame
        :return: Line-of-sight vector in the inertial frame
        """
        los_inertial = rotation_matrix @ los_camera
        return los_inertial / np.linalg.norm(los_inertial)

    @staticmethod
    def calculate_ra_dec(los_vector):
        x, y, z = los_vector
        dec = np.arcsin(z) * (180.0 / np.pi)
        ra = np.arctan2(y, x) * (180.0 / np.pi)
        if ra < 0:
            ra += 360.0  # Ensure RA is in [0, 360)
        return ra, dec

    @staticmethod
    def calculate_arcseconds_per_pixel(fov_degrees: NDArray[np.float32],
                                       resolution_pixels: NDArray[np.float32]) -> NDArray[np.float32]:
        fov_arcseconds = fov_degrees * 3600
        arcsec_per_pixel = fov_arcseconds / resolution_pixels
        return arcsec_per_pixel

    @staticmethod
    def calculate_apparent_radius(fov_rad: NDArray,
                                  resolution_x: NDArray,
                                  distance: float,
                                  actual_radius: float) -> int:
        visible_size = 2 * (distance * np.tan(
            fov_rad / 2))  # Calculate the visible size at the given distance (using half of the FOV for calculation)
        apparent_radius = actual_radius * distance / np.sqrt(
            distance ** 2 + actual_radius ** 2)  # Calculate the apparent radius using geometric projection
        pixels_per_unit = resolution_x / visible_size  # Calculate pixels per unit (for x-axis)
        apparent_radius_in_pixels = apparent_radius * pixels_per_unit  # Calculate the apparent radius in pixels

        return apparent_radius_in_pixels
