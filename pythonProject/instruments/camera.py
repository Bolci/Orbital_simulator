from .dummy_instrument import DummyIntrument
import numpy as np
from numpy.typing import NDArray
from typing import Tuple, Optional
import cv2
import sys

sys.path.append("../")
from utils import Utils


class Camera(DummyIntrument):
    def __init__(self,
                 sensor_resolution: tuple,
                 fov_deg: tuple,
                 max_view_km: float =1000.0,
                 distortion_coeficients: tuple = (0.0,0.0,0.0,0.0)) -> None:
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
        self.distortion_coeficients = np.asarray(distortion_coeficients)

    @property
    def get_camera_matrix(self) -> NDArray[np.float64]:
        return self.camera_matrix


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
        visible_size = 2 * (distance * np.tan(fov_rad / 2)) # Calculate the visible size at the given distance (using half of the FOV for calculation)
        apparent_radius = actual_radius * distance / np.sqrt(distance ** 2 + actual_radius ** 2) # Calculate the apparent radius using geometric projection
        pixels_per_unit = resolution_x / visible_size # Calculate pixels per unit (for x-axis)
        apparent_radius_in_pixels = apparent_radius * pixels_per_unit # Calculate the apparent radius in pixels

        return apparent_radius_in_pixels

    def project_object(self, measured_object: Optional) -> Tuple[NDArray, int]:
        relative_position = measured_object.get_current_position - self.parent_sattelite.get_current_position

        distance_to_satellite = Utils.norm(relative_position)
        relative_position = Utils.get_unit_vector(relative_position)
        direction_to_sattelite = Utils.get_unit_vector(relative_position)

        relative_position = np.dot(self.parent_sattelite.rotation_matrix.T, direction_to_sattelite)
        relative_position = Utils.get_unit_vector(relative_position)

        rotation_matrix_to_instrument = Utils.compute_rot_between_vec(np.array([0., 0., 1.]),
                                                                      self.relative_orientation_to_sattelite_vec)
        relative_position = np.dot(rotation_matrix_to_instrument.T, relative_position)
        relative_position *= distance_to_satellite

        rotation_vector = np.zeros((1, 3), dtype=np.float32)
        image_points, _ = cv2.projectPoints(np.asarray([0., 0., 0.]), rotation_vector, relative_position,
                                            self.camera_matrix,
                                            self.distortion_coeficients)
        image_points = image_points.astype(np.int32)


        projected_radius = self.calculate_apparent_radius(self.fov_rad[::-1],
                                                          self.resolution[::-1],
                                                          distance=distance_to_satellite,
                                                          actual_radius=measured_object.get_radius)

        return image_points[0][0], projected_radius[0].astype(np.int32)


    def get_image(self, measured_object: Optional) -> NDArray:
        img = np.zeros(self.resolution, dtype=np.uint8)

        points_to_projection, projected_radius = self.project_object(measured_object)
        cv2.circle(img, points_to_projection, projected_radius, (255, 255, 255), -1)

        return img


    def measure(self, measured_objects: Optional) -> NDArray:
        image = np.zeros(self.resolution, dtype=np.uint8)

        for measured_object in measured_objects:
            relative_position = self.parent_sattelite.get_current_position - measured_object.get_current_position

            relative_distance = Utils.norm(relative_position)

            if relative_distance <= self.max_view_km:
                image = self.get_image(measured_object)

        return image

    """
    def get_image(self, measured_object: Optional) -> NDArray:
        img = np.zeros(self.resolution, dtype=np.uint8)

        position_of_measured_object = measured_object.get_current_position
        radius_of_measured_object = measured_object.get_radius
        relative_position = position_of_measured_object - self.parent_sattelite.get_current_position

        distance_to_sattelite = Utils.norm(relative_position)
        direction_to_sattelite = Utils.get_unit_vector(relative_position)

        relative_position = np.dot(self.parent_sattelite.rotation_matrix.T, direction_to_sattelite)
        relative_position = Utils.get_unit_vector(relative_position)

        rotation_matrix_to_instrument = Utils.compute_rot_between_vec(np.array([0.,0.,1.]),
                                                                      self.relative_orientation_to_sattelite_vec)
        relative_position = np.dot(rotation_matrix_to_instrument.T, relative_position)
        relative_position *= distance_to_sattelite

        rotation_vector = np.zeros((1,3), dtype=np.float32)
        image_points, _ = cv2.projectPoints(np.asarray([0.,0.,0.]), rotation_vector, relative_position, self.camera_matrix,
                                            self.distortion_coeficients)
        image_points = image_points.astype(np.int32)

        projected_radius = self.calculate_apparent_radius(self.fov_rad[::-1],
                                                          self.resolution[::-1],
                                                          distance=distance_to_sattelite,
                                                          actual_radius=radius_of_measured_object)
        projected_radius = projected_radius[0].astype(np.int32)
        points_to_projection = image_points[0][0]

        cv2.circle(img, (points_to_projection), projected_radius, (255, 255, 255), -1)

        return img
    """