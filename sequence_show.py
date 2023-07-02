from pre_processing.ncsoft_dataset_preprocessing import get_marker_pose
from visualiztion.sequence_vis import marker_sequence_show

if __name__ == "__main__":
    marker_sequence_data = get_marker_pose('NCSOFT\\npy_clean\M_KDH_2022-10-11_14-13-51.npy')
    marker_sequence_show(marker_position=marker_sequence_data)
    
