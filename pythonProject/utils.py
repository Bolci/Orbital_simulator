import numpy as np
from scipy.spatial.transform import Rotation as R
from numpy.typing import NDArray


class Utils:
    @staticmethod
    def norm(vec: NDArray) -> NDArray:
        return np.sqrt(np.dot(vec, vec))

    @staticmethod
    def compute_rotation_matrix_in_3D(pitch: float, yaw: float, roll: float) -> NDArray:
        # Rotation matrix around X-axis (pitch)
        Rx = np.array([
            [1, 0, 0],
            [0, np.cos(pitch), -np.sin(pitch)],
            [0, np.sin(pitch), np.cos(pitch)]
        ])

        # Rotation matrix around Y-axis (yaw)
        Ry = np.array([
            [np.cos(yaw), 0, np.sin(yaw)],
            [0, 1, 0],
            [-np.sin(yaw), 0, np.cos(yaw)]
        ])

        # Rotation matrix around Z-axis (roll)
        Rz = np.array([
            [np.cos(roll), -np.sin(roll), 0],
            [np.sin(roll), np.cos(roll), 0],
            [0, 0, 1]
        ])

        # Combined rotation matrix
        return Rz @ Ry @ Rx

    @staticmethod
    def get_rotation_object(angle_times_axis: NDArray) -> R:
        return R.from_rotvec(angle_times_axis)

    @staticmethod
    def rotation_matrix_to_vector(rotation_matrix: NDArray) -> R:
        return R.from_matrix(rotation_matrix)

    @staticmethod
    def get_perpendicual_vector_to_vectors(vec1: NDArray, vec2: NDArray) -> NDArray:
        return np.cross(vec1, vec2)

    @staticmethod
    def get_rotation_angle(vec_1: NDArray, vec_2: NDArray) -> float:
        theta = np.dot(vec_1, vec_2)

        if np.isclose(theta, 0, atol=1e-8):  # Set atol to desired toleranc
            theta = 0
        theta = np.arccos(np.clip(theta, -1.0, 1.0))

        return theta

    @staticmethod
    def compute_rotation_matrix(p1: NDArray,
                                p2: NDArray,
                                fixed_vector: NDArray,
                                current_rotation: R):
        direction = p2 - p1
        direction = Utils.get_unit_vector(direction)
        fixed_vector = Utils.get_unit_vector(fixed_vector)

        direction = np.dot(current_rotation.T, direction)

        rotation_axis = Utils.get_perpendicual_vector_to_vectors(fixed_vector, direction)

        # If the vectors are parallel, no rotation is needed
        if Utils.norm(rotation_axis) == 0:
            return R.from_matrix(np.eye(3))

        rotation_axis = Utils.get_unit_vector(rotation_axis)
        theta = Utils.get_rotation_angle(fixed_vector, direction)

        rotation = R.from_rotvec(theta * rotation_axis)

        return rotation

    @staticmethod
    def update_orientation(P1, P2, fixed_vector, current_rotation=None):
        if current_rotation is None:
            current_rotation = R.identity()  # Initialize with identity if no previous rotation

        rotation = Utils.compute_rotation_matrix(P1, P2, fixed_vector, current_rotation)
        rotation = rotation.as_matrix()
        current_rotation =  current_rotation @ rotation

        return current_rotation, rotation

    @staticmethod
    def yaw_pitch_roll_to_vector(yaw: float,
                                 pitch: float,
                                 roll: float,
                                 length: float) -> NDArray:
        # Convert angles from degrees to radians
        yaw = np.radians(yaw)
        pitch = np.radians(pitch)
        roll = np.radians(roll)  # Roll is not typically used in a single vector case

        # Compute the direction cosines based on yaw, pitch (ignoring roll for simplicity)
        x = length * np.cos(pitch) * np.cos(yaw)
        y = length * np.cos(pitch) * np.sin(yaw)
        z = length * np.sin(pitch)

        return np.array([x, y, z])

    @staticmethod
    def convert_quaternion_to_rotation_matrix(quaternion):
        w, x, y, z = quaternion
        R = np.array([[1 - 2 * y ** 2 - 2 * z ** 2, 2 * x * y - 2 * z * w, 2 * x * z + 2 * y * w],
                      [2 * x * y + 2 * z * w, 1 - 2 * x ** 2 - 2 * z ** 2, 2 * y * z - 2 * x * w],
                      [2 * x * z - 2 * y * w, 2 * y * z + 2 * x * w, 1 - 2 * x ** 2 - 2 * y ** 2]])

        return R

    @staticmethod
    def get_unit_vector(vector: NDArray) -> NDArray:
        return vector / np.linalg.norm(vector)
