import numpy as np
import math


class QuaternionMath:
    def __init__(self):
        pass

    @staticmethod
    def create_quaternion(axis, angle_rad):
        """Creates a quaternion from an axis and an angle in degrees."""
        angle_radians = angle_rad / 2
        sin_angle = math.sin(angle_radians)
        cos_angle = math.cos(angle_radians)
        axis_normalized = axis / np.linalg.norm(axis)  # Normalize the axis vector
        return np.array(
            [cos_angle, axis_normalized[0] * sin_angle, axis_normalized[1] * sin_angle, axis_normalized[2] * sin_angle])

    @staticmethod
    def quaternion_multiply(q1, q2):
        """Multiplies two quaternions."""

        w1, x1, y1, z1 = q1
        w2, x2, y2, z2 = q2
        w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
        x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
        y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
        z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
        return np.array([w, x, y, z])

    @staticmethod
    def quaternion_conjugate(q):
        """Returns the conjugate of a quaternion (w, -x, -y, -z)."""
        w, x, y, z = q
        return np.array([w, -x, -y, -z])

    @staticmethod
    def rotate_vector_by_quaternion(vector, quaternion):
        """Rotates a vector in 3D space using a quaternion."""
        # Convert the vector to a quaternion (0, vx, vy, vz)
        vector_quaternion = np.array([0] + list(vector))

        # Apply the rotation: v' = q * v * q^-1
        q_conjugate = QuaternionMath.quaternion_conjugate(quaternion)
        rotated_vector_quaternion = QuaternionMath.quaternion_multiply(QuaternionMath.quaternion_multiply(quaternion, vector_quaternion), q_conjugate)

        # Return only the vector part of the resulting quaternion (vx', vy', vz')
        return rotated_vector_quaternion[1:]