from .dummy_instrument import DummyIntrument
import numpy as np
from numpy.typing import NDArray
from typing import Tuple, Optional
import cv2
import sys

sys.path.append("../")
from utils.utils_vector import Utils
from utils.utils_camera import UtilsCamera


class Camera(DummyIntrument):
    def __init__(self,
                 sensor_resolution: tuple,
                 fov_deg: tuple,
                 max_view_km: float =1000.0,
                 distortion_coeficients: tuple = (0.0,0.0,0.0,0.0),
                 camera_uncertanity_in_km: int = 0.1) -> None:
        super().__init__(intrument_label="Camera")

        self.arcsec_to_rad = 4.84814e-6  # s
        self.resolution = np.asarray(sensor_resolution)
        self.fov_deg = np.asarray(fov_deg)
        self.fov_rad = np.deg2rad(self.fov_deg)
        self.camera_uncertanity_in_km = camera_uncertanity_in_km

        self.arcsec_per_pixel = UtilsCamera.calculate_arcseconds_per_pixel(self.fov_deg, self.resolution)
        self.rad_per_pixel = self.arcsec_per_pixel * self.arcsec_to_rad
        self.max_view_km = max_view_km

        self.focal_length_xy = (self.resolution / 2) / np.tan(self.fov_deg / 2)

        self.camera_matrix = np.array([[self.focal_length_xy[1], 0, self.resolution[1]//2],
                                              [0, self.focal_length_xy[0], self.resolution[0]//2],
                                              [0, 0, 1]], dtype=np.float32)
        self.distortion_coeficients = np.asarray(distortion_coeficients)

        self.flag = 0

    @property
    def get_camera_matrix(self) -> NDArray[np.float64]:
        return self.camera_matrix

    def sample_uncertanity(self):
        return np.random.normal(self.camera_uncertanity_in_km, 3)

    def get_camera_report(self):
        return {'camera_intrinsics': {'fx': self.focal_length_xy[1],
                                      'fy': self.focal_length_xy[0],
                                      'cx': self.resolution[1]//2,
                                      'cy': self.resolution[0]//2}}

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

        #add errors to image
        #relative_position += self.sample_uncertanity()

        rotation_vector = np.zeros((1, 3), dtype=np.float32)
        image_points, _ = cv2.projectPoints(np.asarray([0., 0., 0.]), rotation_vector, relative_position,
                                            self.camera_matrix,
                                            self.distortion_coeficients)
        image_points = image_points.astype(np.int32)

        projected_radius = UtilsCamera.calculate_apparent_radius(self.fov_rad[::-1],
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

        distance_to_sattelite = utils.norm(relative_position)
        direction_to_sattelite = utils.get_unit_vector(relative_position)

        relative_position = np.dot(self.parent_sattelite.rotation_matrix.T, direction_to_sattelite)
        relative_position = utils.get_unit_vector(relative_position)

        rotation_matrix_to_instrument = utils.compute_rot_between_vec(np.array([0.,0.,1.]),
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