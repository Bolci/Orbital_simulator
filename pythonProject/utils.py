import numpy as np

class Utils:
    @staticmethod
    def norm(vec):
        return np.sqrt(np.dot(vec, vec))

    @staticmethod
    def compute_rotation_matrix_in_3D(pitch, yaw, roll):
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
        return Ry @ Rx

    @staticmethod
    def yaw_pitch_roll_to_vector(yaw, pitch, roll, length):
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
    def get_unit_vector(vector):
        return vector / np.linalg.norm(vector)
