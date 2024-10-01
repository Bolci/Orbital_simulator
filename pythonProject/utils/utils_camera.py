import numpy as np
from numpy.typing import NDArray


class UtilsCamera:
    @staticmethod
    def pixel_to_los(pixel_coords, camera_intrinsics, camera_orientation):
        # This function will convert pixel coordinates into a 3D LoS vector based on camera intrinsic parameters
        # camera_intrinsics contains fx, fy, cx, cy (focal length and principal point)
        # camera_orientation contains rotation matrix to world coordinates

        fx, fy, cx, cy = camera_intrinsics
        x, y = pixel_coords

        # Normalize pixel coordinates (to camera frame)
        norm_x = (x - cx) / fx
        norm_y = (y - cy) / fy

        # Assume a focal length of 1 unit in the camera z-axis (camera frame)
        los_camera_frame = np.array([norm_x, norm_y, 1.0])

        # Rotate the LoS vector to the world (ECI) frame using the camera orientation
        los_world_frame = np.dot(camera_orientation, los_camera_frame)

        # Normalize the vector to get the direction (LoS)
        return los_world_frame / np.linalg.norm(los_world_frame)

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
