import numpy as np
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt

def normalize(v):
    return v / np.linalg.norm(v)


P1_all = [np.array([1., 2., 3.]), np.array([1.,2.,3.]), np.array([1.,2.,3.]) ] # Example point 1 (local origin)
P2_all = [np.array([4., 5., 6.]), np.array([3.,3.,3.]), np.array([8.,7.,9.])]  # Example point 2 (target)
fixed_vector = np.array([0., 0., 1.])
fixed_vector_global = fixed_vector

local_coorrdinates_x = np.array([1.,0.,0.])
local_coorrdinates_y = np.array([0.,1.,0.])
local_coorrdinates_z = np.array([0.,0.,1.])

current_rotation = np.column_stack((local_coorrdinates_x,
                                   local_coorrdinates_y,
                                   local_coorrdinates_z))
fixed_vector_global = np.dot(current_rotation, fixed_vector)
fixed_vector_global = normalize(fixed_vector_global)

def compute_rotation_matrix(P1, P2, fixed_vector):
    direction = P2 - P1
    direction = normalize(direction)
    fixed_vector = normalize(fixed_vector)

    direction = np.dot(current_rotation.T, direction)
    direction = normalize(direction)

    rotation_axis = np.cross(fixed_vector, direction)

    if np.linalg.norm(rotation_axis) == 0:
        # If the vectors are parallel, no rotation is needed
        return R.from_matrix(np.eye(3))  # No rotation, return identity rotation

    rotation_axis = normalize(rotation_axis)

    theta = np.dot(fixed_vector, direction)

    #if np.isclose(theta, 0, atol=1e-8):  # Set atol to desired toleranc
    #    theta = 0

    theta = np.arccos(np.clip(theta, -1.0, 1.0))  # Clip to avoid numerical errors

    # Step 4: Use scipy to create the rotation object
    rotation = R.from_rotvec(theta * rotation_axis)  # Axis-angle to rotation vector

    return rotation


def update_orientation(P1, P2, fixed_vector, current_rotation=None):
    # Compute the new rotation to align local system to P2
    rotation = compute_rotation_matrix(P1, P2, fixed_vector)

    # Step 5: Cumulative rotation - Combine with the previous rotation
    if current_rotation is None:
        current_rotation = R.identity()  # Initialize with identity if no previous rotation

    rotation = rotation.as_matrix()

    current_rotation = current_rotation @ rotation

    return current_rotation, rotation

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
ax.plot([0],[0],[0],'*', label="GCC")

for step in range(2):  # Simulating over 10 time steps
    P1 = P1_all[step]
    P2 = P2_all[step]

    current_rotation, rotation = update_orientation(P1, P2, fixed_vector, current_rotation)
    #rot_matrix = current_rotation.as_matrix()
    rot_matrix = current_rotation
    print(F"current rotation {rot_matrix}")
    local_coorrdinates_x = np.dot(current_rotation, np.array([1,0,0]))
    local_coorrdinates_y = np.dot(current_rotation,  np.array([0,1,0]))
    local_coorrdinates_z = np.dot(current_rotation,  np.array([0,0,1]))

    fixed_vector_global = np.dot(current_rotation, fixed_vector)
    fixed_vector_global = normalize(fixed_vector_global)
    print(F" fixed vector global = {fixed_vector_global}")

    ax.plot(*P1,'*', label="LCC")
    ax.plot(*P2,'*', label="Direction")
    ax.plot([P1[0],P2[0]],[P1[1], P2[1]],[P1[2], P2[2]], '-*',color="magenta")

    ax.quiver(*P1, *fixed_vector_global, length=1000,color='yellow', label ='label_rot vec_global', normalize=True)
    ax.quiver(*P1, *fixed_vector, color='magenta', label='label_rot vec')
    ax.quiver(*P1,*local_coorrdinates_x,color='r',normalize=True)
    ax.quiver(*P1, *local_coorrdinates_y, color='g', normalize=True)
    ax.quiver(*P1, *local_coorrdinates_z, color='b', normalize=True)

plt.legend()
plt.show()