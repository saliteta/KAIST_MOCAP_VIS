
        
        
from pre_processing.ncsoft_dataset_preprocessing import get_marker_pose, MESH_REALTIONSHIP
from visualiztion.frame_vis import marker_mesh_show, marker_frame_show
import numpy as np
'''
    we need to get the edge relationship for skeleton
    
'''


if __name__ == "__main__":

    marker_position = np.load('data\\result.npy')[0][0]
    marker_frame_show(marker_position)
