import numpy as np
import open3d as o3d
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from sequence_vis import joints_to_skeleton


def marker_frame_show(markers: np.ndarray) -> None:    

    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(markers)


    o3d.visualization.draw_geometries([point_cloud])


def skeleton_frame_show(skeleton:np.ndarray, edge_relationship:np.ndarray, edge_color) -> None:
    lineset = joints_to_skeleton(skeleton, edge_relationship, edge_color)
    o3d.visualization.draw_geometries([lineset])
    
    
def marker_mesh_show(markers: np.ndarray, mesh_relationship:np.ndarray) -> None:    

    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(markers)
    mesh.triangles = o3d.utility.Vector3iVector(mesh_relationship)
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(mesh)
    vis.run()
    vis.destroy_window()
