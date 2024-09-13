import numpy as np
from utils import Utils


class DummyIntrument():
    def __init__(self):
        self.parent_sattelite = None

    def assign_sattelite(self, sattelite_pointer):
        self.parent_sattelite = sattelite_pointer

    def measure(self, data_from_objects):
        pass


class Camera(DummyIntrument):
    def __init__(self,
                 sensor_resolution,
                 fov_deg,
                 relative_initial_orienetation_to_sattelite=[0.3279051159057125, 55.24257187138766, 45.0],
                 max_view_km=1000):
        super().__init__()

        self.arcsec_to_rad = 4.84814e-6  # s
        self.resolution = np.asarray(sensor_resolution)
        self.fov_deg = np.asarray(fov_deg)

        self.arcsec_per_pixel = self.calculate_arcseconds_per_pixel(self.fov_deg, self.resolution)
        self.rad_per_pixel = self.arcsec_per_pixel * self.arcsec_to_rad
        self.max_view_km = max_view_km

        self.focal_length_xy = (self.resolution / 2) / np.tan(self.fov_deg / 2)

        self.relative_orientation_to_sattelite = np.deg2rad(relative_initial_orienetation_to_sattelite)

    def set_rotation(self, rotation):
        self.relative_orientation_to_sattelite = np.deg2rad(rotation)

    @staticmethod
    def calculate_arcseconds_per_pixel(fov_degrees, resolution_pixels):
        fov_arcseconds = fov_degrees * 3600
        arcsec_per_pixel = fov_arcseconds / resolution_pixels
        return arcsec_per_pixel

    def project(self, point):
        """
        Project a 3D point onto a 2D image plane using a pinhole camera model with rotation.
        """
        translated_point = point - self.parent_sattelite.get_current_position()
        rotated_point = Utils.compute_rotation_matrix_in_3D(*self.relative_orientation_to_sattelite) @ translated_point

        # if rotated_point[2] <= 0:
        #    return None # Ignore points behind the camera

        x_2d = self.focal_length_xy[0] * (rotated_point[0] / rotated_point[2])
        y_2d = self.focal_length_xy[1] * (rotated_point[1] / rotated_point[2])

        # Convert to pixel coordinates
        pixel_x = int((x_2d + self.resolution[0] / 2))
        pixel_y = int((self.resolution[1] / 2 - y_2d))

        return pixel_x, pixel_y, rotated_point[2]

    def get_image(self, relative_distance_m, measured_object):
        img = np.zeros(self.resolution, dtype=np.uint8)

        return img

    def measure(self, measured_objects):
        for measured_object in measured_objects:
            relative_position = self.parent_sattelite.get_current_position() - measured_object.get_current_position()
            relative_distance = Utils.norm(relative_position)
            relative_distance_m = relative_distance * 1000

            if relative_distance <= self.max_view_km:
                image = self.get_image(relative_distance_m, measured_object)


class LaserAltimeter(DummyIntrument):
    def __init__(self):
        super().__init__()

    def measure(self, data_from_objects):
        pass