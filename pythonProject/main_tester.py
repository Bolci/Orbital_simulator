import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.transform import Rotation as R

# Define an arbitrary point [x, y, z] (origin of the new coordinate system)
point = np.array([1, 1, 1]).astype(np.float64)

# Define an arbitrary vector in the new coordinate system (for example, [1, 0, 0])
arbitrary_vector = np.array([1, 0, 0]).astype(np.float64)  # Initially along the local x-axis

# Define the target point that you want the arbitrary vector to face
target_point = np.array([2, 2, 2]).astype(np.float64)

# Calculate the target vector (from the point to the target point)
target_vector = target_point - point
target_vector /= np.linalg.norm(target_vector)  # Normalize the vector

# Normalize the arbitrary vector (ensure it's a unit vector)
arbitrary_vector /= np.linalg.norm(arbitrary_vector)

# Find the rotation axis using the cross product of the arbitrary vector and the target vector
rotation_axis = np.cross(arbitrary_vector, target_vector)
rotation_axis /= np.linalg.norm(rotation_axis)  # Normalize the rotation axis

# Calculate the rotation angle using the dot product of the arbitrary vector and target vector
rotation_angle = np.arccos(np.dot(arbitrary_vector, target_vector))

# Create the rotation using axis-angle representation
rotation = R.from_rotvec(rotation_angle * rotation_axis)

# Define local coordinate system (initially aligned with global system)
local_x_axis = np.array([1, 0, 0])
local_y_axis = np.array([0, 1, 0])
local_z_axis = np.array([0, 0, 1])

# Apply the rotation to the local coordinate system
rotated_x_axis = rotation.apply(local_x_axis)
rotated_y_axis = rotation.apply(local_y_axis)
rotated_z_axis = rotation.apply(local_z_axis)

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot global coordinate system at the origin
ax.quiver(0, 0, 0, 1, 0, 0, color='r', label='Global X', length=1, normalize=True)
ax.quiver(0, 0, 0, 0, 1, 0, color='g', label='Global Y', length=1, normalize=True)
ax.quiver(0, 0, 0, 0, 0, 1, color='b', label='Global Z', length=1, normalize=True)

# Plot the rotated coordinate system at point [x, y, z]
ax.quiver(*point, *rotated_x_axis, color='magenta', label='Rotated X', length=1, normalize=True)
ax.quiver(*point, *rotated_y_axis, color='cyan', label='Rotated Y', length=1, normalize=True)
ax.quiver(*point, *rotated_z_axis, color='yellow', label='Rotated Z', length=1, normalize=True)

# Set plot limits and labels
ax.set_xlim([-5, 5])
ax.set_ylim([-5,5])
ax.set_zlim([-5, 5])

ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')

# Add a legend
ax.legend()

# Display the plot
plt.show()
