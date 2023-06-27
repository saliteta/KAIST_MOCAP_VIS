import numpy as np 
import open3d as o3d


'''
    we need to get the edge relationship for skeleton
    
'''

SKELETON_EDGES = np.array([ [0,1], [0,2], [0,3], [1,4], [4,7], [7,10], 
                            [2,5], [5,8], [8,11], [3,6], [6,9], [9,14],
                            [9,13], [14,17], [17,19], [19,21], [21,23], [13,16],
                            [16,18], [18,20], [20,22], [14,12], [13,12], [12,15],
                            ])

EDGE_COLOR = np.array(
                  [[1, 0, 0] for i in range(len(SKELETON_EDGES))
                   ]) # Yellow


if __name__ == "__main__":
    
    file = np.load("data/01_01_03_poses_0.npz")
    skeleton = file['J']
    lineset = o3d.geometry.LineSet()
    lineset.points = o3d.utility.Vector3dVector(skeleton)
    lineset.lines = o3d.utility.Vector2iVector(SKELETON_EDGES)
    lineset.colors = o3d.utility.Vector3dVector(EDGE_COLOR)
    
    o3d.visualization.draw_geometries([lineset])

    
    
    
    
    
    