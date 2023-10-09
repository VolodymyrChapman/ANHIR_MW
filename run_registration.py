import os
import numpy as np
import matplotlib.pyplot as plt

import anhir_method as am
import utils
from skimage.io import imsave


def main():
    source_path =  'CD10_40x/479379.png' # Source path
    target_path = 'HE_40x/474049.png'  # Target path

    # source_landmarks_path = None # Source landmarks path
    # target_landmarks_path = None # Target landmarks path

    # source_landmarks = utils.load_landmarks(source_landmarks_path)
    # target_landmarks = utils.load_landmarks(target_landmarks_path)

    source = utils.load_image(source_path)
    target = utils.load_image(target_path)

    p_source, p_target, ia_source, ng_source, nr_source, i_u_x, i_u_y, u_x_nr, u_y_nr, warp_resampled_landmarks, warp_original_landmarks, return_dict = am.anhir_method(target, source)

    # transformed_source_landmarks = warp_original_landmarks(source_landmarks)

    # resampled_source_landmarks, transformed_resampled_source_landmarks, resampled_target_landmarks = warp_resampled_landmarks(source_landmarks, target_landmarks)
    
    imsave('474379_nr.png')

if __name__ == '__main__':
    main()