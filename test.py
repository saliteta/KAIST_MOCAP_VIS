import numpy as np

# Example input matrices
points = np.random.rand(24, 3)
rotation_matrices = np.random.rand(24, 3, 3)

# Perform rotation for each point individually using np.einsum
rotated_points = np.einsum('ijk,ik->ij', rotation_matrices, points)

print(rotated_points.shape)
