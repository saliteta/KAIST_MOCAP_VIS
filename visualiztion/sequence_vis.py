
import open3d as o3d
import numpy as np

def joints_to_skeleton(joints:np.ndarray, edge_relationship: list, edge_color: np.ndarray):
    '''
        Given the Skeleton Joints positions, we will draw the skeleton
        return the lineset that contains a skeleton
    '''

    lineset = o3d.geometry.LineSet()
    lineset.points = o3d.utility.Vector3dVector(joints)
    lineset.lines = o3d.utility.Vector2iVector(edge_relationship)
    colors = np.tile(edge_color, (len(edge_relationship), 1))
    lineset.colors = o3d.utility.Vector3dVector(colors)
    return lineset

def marker_to_open3d_points(markers:np.ndarray):
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(markers)
    return point_cloud


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
            z= j * grid_spacing - grid_size / 2
            vertices.append([x, 0, z])
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

def adjust_camera_to_point_cloud(point_cloud, vis):
    """
    Adjusts the camera view to point to the center of the point cloud.

    Args:
        point_cloud (open3d.geometry.PointCloud): The point cloud.
        vis (open3d.visualization.Visualizer): The visualizer.

    Returns:
        None.
    """

    # Get the center of the point cloud.
    center = point_cloud.get_center()

    # Create a view control object.
    view_control = vis.get_view_control()

    # Set the camera position to the center of the point cloud.
    view_control.set_lookat(np.array([center[0], center[1], center[2]], dtype=np.float64), )

def skeleton_sequence_show(joints_position:np.ndarray, edge_relationship: list, edge_color: np.ndarray = np.array([1,0,0]), ground_plane_size = 400, plane_color_difference_distance = 2) -> None:
    vis = o3d.visualization.Visualizer()

    vis.create_window()
    
    ground_plane = create_ground_plane(ground_plane_size, plane_color_difference_distance)
    vis.add_geometry(ground_plane)
    vis.poll_events()
    
    for current_joints in joints_position:
    
        try:
            vis.remove_geometry(current_skeleton, False)
        except:
            print("no skeleton in there yet")
    
        
        # Add the transformed point cloud to the visualization
        current_skeleton = joints_to_skeleton(current_joints, edge_relationship, edge_color)
        vis.add_geometry(current_skeleton)
        vis.poll_events()
        # Update the visualization
        vis.update_renderer()
        
        # Set a delay between each visualization (in seconds)

    vis.destroy_window()
    return

def show_spheres_at_points(point_cloud, vis, sphere_color=(1, 0, 0)):
    """
    Show spheres at each point in a point cloud with custom color.

    Args:
        point_cloud (open3d.geometry.PointCloud): The point cloud.
        vis (open3d.visualization.Visualizer): The visualizer object.
        sphere_color (tuple or list): RGB values for the sphere color (between 0 and 1).

    Returns:
        None.
    """
    color = np.array(sphere_color)
    for point in point_cloud.points:
        sphere = o3d.geometry.TriangleMesh.create_sphere(radius=10)
        sphere.translate(point)
        sphere.paint_uniform_color(color)
        vis.add_geometry(sphere)

    vis.poll_events()
    vis.update_renderer()
    vis.clear_geometries()





def marker_sequence_show(marker_position:np.ndarray) -> None:
    vis = o3d.visualization.Visualizer()

    vis.create_window()
    
    #ground_plane = create_ground_plane(ground_plane_size, plane_color_difference_distance)
    #vis.add_geometry(ground_plane)
    vis.poll_events()
    print(marker_position.shape)
    for current_markers in marker_position:
        # Add the transformed point cloud to the visualization
        print("how long is the rendering")
        point_cloud = marker_to_open3d_points(current_markers)
        show_spheres_at_points(point_cloud, vis)

    vis.destroy_window()
    