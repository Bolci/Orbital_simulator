from .dummy_instrument import DummyIntrument
import numpy as np
import cv2
import sys

sys.path.append("../")
from utils import Utils


class Camera(DummyIntrument):
    def __init__(self,
                 sensor_resolution,
                 fov_deg,
                 max_view_km=1000,
                 distortion_coeficients = np.zeros((4,1))):
        super().__init__(intrument_label="Camera")


        self.arcsec_to_rad = 4.84814e-6  # s
        self.resolution = np.asarray(sensor_resolution)
        self.fov_deg = np.asarray(fov_deg)
        self.fov_rad = np.deg2rad(self.fov_deg)

        self.arcsec_per_pixel = self.calculate_arcseconds_per_pixel(self.fov_deg, self.resolution)
        self.rad_per_pixel = self.arcsec_per_pixel * self.arcsec_to_rad
        self.max_view_km = max_view_km

        self.focal_length_xy = (self.resolution / 2) / np.tan(self.fov_deg / 2)

        self.camera_matrix = np.array([[self.focal_length_xy[1], 0, self.resolution[1]//2],
                                              [0, self.focal_length_xy[0], self.resolution[0]//2],
                                              [0, 0, 1]], dtype=np.float32)
        self.distortion_coeficients = distortion_coeficients

    @property
    def get_camera_matrix(self):
        return self.camera_matrix


    @staticmethod
    def calculate_arcseconds_per_pixel(fov_degrees, resolution_pixels):
        fov_arcseconds = fov_degrees * 3600
        arcsec_per_pixel = fov_arcseconds / resolution_pixels
        return arcsec_per_pixel

    @staticmethod
    def calculate_apparent_radius(fov_x_rad, fov_y_rad, resolution_x, resolution_y, distance, actual_radius):
        # Calculate the visible size at the given distance (using half of the FOV for calculation)
        visible_size_x = 2 * (distance * np.tan(fov_x_rad / 2))
        visible_size_y = 2 * (distance * np.tan(fov_y_rad / 2))

        # Calculate the apparent radius using geometric projection
        apparent_radius = actual_radius * distance / np.sqrt(distance ** 2 + actual_radius ** 2)

        # Calculate pixels per unit (for x-axis)
        pixels_per_unit_x = resolution_x / visible_size_x
        pixels_per_unit_y = resolution_y / visible_size_y

        # Calculate the apparent radius in pixels
        apparent_radius_in_pixels_x = apparent_radius * pixels_per_unit_x
        apparent_radius_in_pixels_y = apparent_radius * pixels_per_unit_y

        return apparent_radius_in_pixels_x, apparent_radius_in_pixels_y

    def get_image(self, measured_object):
        img = np.zeros(self.resolution, dtype=np.uint8)

        position_of_measured_object = measured_object.get_current_position()
        radius_of_measured_object = measured_object.get_radius()

        relative_position = position_of_measured_object - self.parent_sattelite.get_current_position()
        distance_to_sattelite = Utils.norm(relative_position)
        direction_to_sattelite = Utils.get_unit_vector(relative_position)

        relative_position = np.dot(self.parent_sattelite.rotation_matrix.T, direction_to_sattelite)
        relative_position = Utils.get_unit_vector(relative_position)
        #relative_position *= distance_to_sattelite

        rotation_vector = np.zeros((1,3), dtype=np.float32)
        #rotation_vector = Utils.rotation_matrix_to_vector(self.parent_sattelite.rotation_matrix).as_matrix().T

        image_points, _ = cv2.projectPoints(np.asarray([0.,0.,0.]), rotation_vector, relative_position, self.camera_matrix,
                                            self.distortion_coeficients)
        image_points = image_points.astype(np.int32)


        projected_radius = self.calculate_apparent_radius(self.fov_rad[1],
                                                          self.fov_rad[0],
                                                          self.resolution[1],
                                                          self.resolution[0],
                                                          distance=distance_to_sattelite,
                                                          actual_radius=radius_of_measured_object)
        projected_radius = projected_radius[0].astype(np.int32)
        points_to_projection = image_points[0][0]

        cv2.circle(img, (points_to_projection), projected_radius, (255, 255, 255), -1)

        return img

    def measure(self, measured_objects):
        image = np.zeros(self.resolution, dtype=np.uint8)

        for measured_object in measured_objects:
            relative_position = self.parent_sattelite.get_current_position() - measured_object.get_current_position()

            relative_distance = Utils.norm(relative_position)

            if relative_distance <= self.max_view_km:
                image = self.get_image(measured_object)

        return image
