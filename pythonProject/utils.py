import numpy as np
from scipy.spatial.transform import Rotation as R
from numpy.typing import NDArray


class Utils:
    @staticmethod
    def norm(vec: NDArray) -> NDArray:
        return np.sqrt(np.dot(vec, vec))

    @staticmethod
    def get_unit_vector(vector: NDArray) -> NDArray:
        return vector / np.linalg.norm(vector)

    @staticmethod
    def compute_rotation_matrix_in_3D(pitch: float, yaw: float, roll: float) -> NDArray:
        """Combines pitch, yaw, and roll into a single rotation matrix."""
        return R.from_euler('xyz', [pitch, yaw, roll], degrees=False).as_matrix()

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
        direction = Utils.get_unit_vector(p2 - p1)
        fixed_vector = Utils.get_unit_vector(fixed_vector)
        direction = np.dot(current_rotation.T, direction)

        rotation_axis = Utils.get_perpendicual_vector_to_vectors(fixed_vector, direction)

        # If the vectors are parallel, no rotation is needed
        if Utils.norm(rotation_axis) == 0:
            return R.from_matrix(np.eye(3))

        rotation_axis = Utils.get_unit_vector(rotation_axis)
        theta = Utils.get_rotation_angle(fixed_vector, direction)

        return R.from_rotvec(theta * rotation_axis)

    @staticmethod
    def compute_rot_between_vec(vec1: NDArray, vec2: NDArray) -> NDArray:
        vec1 = Utils.get_unit_vector(vec1)
        vec2 = Utils.get_unit_vector(vec2)

        rotation_axis = Utils.get_perpendicual_vector_to_vectors(vec1, vec2)

        if Utils.norm(rotation_axis) == 0:
            return np.eye(3)

        rotation_axis = Utils.get_unit_vector(rotation_axis)
        theta = Utils.get_rotation_angle(vec1, vec2)

        rotation = R.from_rotvec(theta * rotation_axis)
        rotation = rotation.as_matrix()
        rotation = Utils.get_unit_vector(rotation)

        return rotation

    @staticmethod
    def update_orientation(p1, p2, fixed_vector, current_rotation=None):
        if current_rotation is None:
            current_rotation = R.identity()  # Initialize with identity if no previous rotation

        rotation = Utils.compute_rotation_matrix(p1, p2, fixed_vector, current_rotation)
        rotation = rotation.as_matrix()
        current_rotation =  current_rotation @ rotation

        return current_rotation, rotation

    @staticmethod
    def yaw_pitch_roll_to_vector(yaw: float, pitch: float, roll: float, length: float) -> NDArray:
        """Generates a vector in 3D space given yaw, pitch, roll, and length."""
        return Utils.compute_rotation_matrix_in_3D(pitch, yaw, roll) @ np.array([length, 0, 0])

    @staticmethod
    def convert_quaternion_to_rotation_matrix(quaternion: NDArray) -> NDArray:
        return R.from_quat(quaternion).as_matrix()
