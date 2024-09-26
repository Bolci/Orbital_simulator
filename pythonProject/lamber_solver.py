import numpy as np
from Utils.utils_vector import Utils
from scipy.optimize import newton


class LambertSolver:
    def __init__(self, mu):
        """Lambert solver"""
        self.mu = mu

    def S(self, z):
        """Stumpff function S."""
        if z > 0:
            return (np.sqrt(z) - np.sin(np.sqrt(z))) / z**1.5
        elif z == 0:
            return 1 / 6
        else:
            return (np.sinh(np.sqrt(-z)) - np.sqrt(-z)) / (-z)**1.5

    def C(self, z):
        """Stumpff function C."""
        if z > 0:
            return (1 - np.cos(np.sqrt(z))) / z
        elif z == 0:
            return 0.5
        else:
            return (np.cosh(np.sqrt(-z)) - 1) / (-z)

    def y(self, z, r1_norm, r2_norm, A):
        """Calculates the y function used in Lambert's problem."""
        return r1_norm + r2_norm + A * (z * self.S(z) - 1) / np.sqrt(self.C(z))

    def F(self, z, r1_norm, r2_norm, A, dt):
        """Calculates the F function used in solving Lambert's problem."""
        return (self.y(z, r1_norm, r2_norm, A) / self.C(z))**1.5 * self.S(z) + A * np.sqrt(self.y(z, r1_norm, r2_norm, A)) - np.sqrt(self.mu) * dt

    def solve(self, r1, r2, dt):
        """Solves Lambert's problem for the given parameters.

        Parameters:
        r1 (array): Initial position vector (km)
        r2 (array): Final position vector (km)
        dt (float): Time of flight (seconds)

        Returns:
        v1 (array): Velocity at r1 (km/s)
        v2 (array): Velocity at r2 (km/s)
        """
        r1_norm = Utils.norm(r1)
        r2_norm = Utils.norm(r2)
        dtheta = np.arccos(np.dot(r1, r2) / (r1_norm * r2_norm))  # Angle between r1 and r2

        # Solving using universal variable formulation
        A = np.sin(dtheta) * np.sqrt(r1_norm * r2_norm / (1 - np.cos(dtheta)))

        # Use the Newton method to solve for z
        z_guess = 0.1  # Initial guess for z
        z_solution = newton(self.F, z_guess, args=(r1_norm, r2_norm, A, dt))

        # Calculate the velocity vectors at r1 and r2
        f = 1 - self.y(z_solution, r1_norm, r2_norm, A) / r1_norm
        g = A * np.sqrt(self.y(z_solution, r1_norm, r2_norm, A) / self.mu)

        v1 = (r2 - f * r1) / g
        g_dot = 1 - self.y(z_solution, r1_norm, r2_norm, A) / r2_norm
        v2 = (g_dot * r2 - r1) / g

        return v1, v2
