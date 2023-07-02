import open3d as o3d
import numpy as np
import time
import copy

from t_pose_vis import EDGE_COLOR, SKELETON_EDGES


def joints_to_skeleton(joints, edge_relationship: np.ndarray = SKELETON_EDGES, edge_color: np.ndarray = EDGE_COLOR):
    '''
        Given the Skeleton Joints positions, we will draw the skeleton
        return the lineset that contains a skeleton
    '''

    lineset = o3d.geometry.LineSet()
    lineset.points = o3d.utility.Vector3dVector(joints)
    lineset.lines = o3d.utility.Vector2iVector(edge_relationship)
    lineset.colors = o3d.utility.Vector3dVector(edge_color)
    return lineset

def create_ground_plane(grid_size=10.0, grid_spacing=0.1):
    '''
        This function will return a mesh that looks like a grid.
        This grid will help people to visualize the motion of point cloud
    '''
    num_cells = int(grid_size / grid_spacing)
    vertices = []
    triangles = []
    colors = []
    color1 = [0.8, 0.8, 0.8]
    color2 = [0.7, 0.7, 0.7]
    
    for i in range(num_cells + 1):
        x = i * grid_spacing - grid_size / 2
        for j in range(num_cells + 1):
            y = j * grid_spacing - grid_size / 2
            vertices.append([x, y, -1])
            colors.append(color1 if (i + j) % 2 == 0 else color2)

    for i in range(num_cells):
        for j in range(num_cells):
            v0 = i * (num_cells + 1) + j
            v1 = v0 + 1
            v2 = (i + 1) * (num_cells + 1) + j
            v3 = v2 + 1
            triangles.extend([[v0, v2, v1], [v1, v2, v3]])

    plane = o3d.geometry.TriangleMesh()
    plane.vertices = o3d.utility.Vector3dVector(vertices)
    plane.triangles = o3d.utility.Vector3iVector(triangles)
    plane.vertex_colors = o3d.utility.Vector3dVector(colors)
    return plane

if __name__ == "__main__":
    file = np.load("data/01_01_03_poses_0.npz")
    skeleton_rotation_sequence = file['J_R']
    skeleton_translation_sequence = file['J_t']
    skeleton_reference_joints = (file['J'])

    vis = o3d.visualization.Visualizer()

    current_skeleton_joint = o3d.geometry.PointCloud()
    vis.create_window()
    lineset = o3d.geometry.LineSet()
    
    ground_plane = create_ground_plane()
    vis.add_geometry(ground_plane)
    vis.poll_events()
    
    for i, (rotation_matrix, translation_vector) in enumerate(zip(skeleton_rotation_sequence, skeleton_translation_sequence)):
        try:
            vis.remove_geometry(current_skeleton, False)
        except:
            print("no skeleton in there yet")
    
        
        # Apply rotation and translation to the point cloud
        transformed_points = np.einsum('ijk,ik->ij', rotation_matrix, skeleton_reference_joints) + translation_vector
        current_skeleton_joint.points = o3d.utility.Vector3dVector(transformed_points)


        # Add the transformed point cloud to the visualization
        current_skeleton = joints_to_skeleton(np.asarray(current_skeleton_joint.points))
        vis.add_geometry(current_skeleton, False)
        vis.poll_events()
        # Update the visualization
        vis.update_renderer()
        
        # Set a delay between each visualization (in seconds)

    vis.destroy_window()
