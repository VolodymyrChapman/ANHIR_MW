import os
import numpy as np
import matplotlib.pyplot as plt

import anhir_method as am
import preprocessing
import utils
from skimage.io import imsave, imread
from skimage.transform import resize

from scipy import ndimage as nd

def resample_single(source,resample_ratio):
    s_y_size, s_x_size = source.shape
    source = utils.resample(source, int(s_x_size/resample_ratio), int(s_y_size/resample_ratio))
    return source

def main(target_path, moving_path, outdir = ''):

    source = utils.load_image(moving_path)
    target = utils.load_image(target_path)

    if source.shape[0] == 1:
        source = source[0,:,:]

    if target.shape[0] == 1:
        target = target[0,:,:]

    p_source, p_target, ia_source, ng_source, nr_source, i_u_x, i_u_y, u_x_nr, u_y_nr, warp_resampled_landmarks, warp_original_landmarks, return_dict, initial_resample_ratio = am.anhir_method(source, target)
    

    # Need to use x and y nr transformations on padded rgb channels
    # parse rgb image to transform
    rgb_warp = imread(moving_path)
    target_shape = imread(target_path).shape

    s_resampled = []
    for channel in range(3):
        s_resampled.append(resample_single(rgb_warp[:,:,channel], initial_resample_ratio))

    s_resampled = np.stack(s_resampled, axis = -1)

    # conduct preprocess to get padding
    source, target, t_source, t_target, (source_l_x, source_r_x, source_l_y, source_r_y), (target_l_x, target_r_x, target_l_y, target_r_y) = preprocessing.preprocess(s_resampled[:,:,0], p_target, False)

    rgb_warp_pad = []
    for channel in range(3):
        rgb_warp_pad.append(np.pad(s_resampled[:,:,channel], [(source_l_y, source_r_y), (source_l_x, source_r_x)], mode='constant'))

    rgb_warp_pad = np.stack(rgb_warp_pad, axis = -1)

    # size down to post-registration size

    # add padding to be same size as target

    # warp image in each channel
    for channel in range(3):
        rgb_warp_pad[:,:,channel] = utils.warp_image(rgb_warp_pad[:,:,channel], u_x_nr, u_y_nr)

    # resize to match input ihc
    registered_scaled = (resize(rgb_warp_pad, target_shape)* 255).astype(np.uint8)

    outfile = os.path.split(moving_path)[-1]

    # save resized
    imsave(os.path.join(outdir, 'registered_' + outfile),registered_scaled)
    
if __name__ == '__main__':
    # main(target_path = '/media/volodymyr/1TB_Store_B/Lymphoma_subgrouping/Projects/2023_10_HE_vs_CD10_follicles/data/HE_40x/474067.png', moving_path =  '/media/volodymyr/1TB_Store_B/Lymphoma_subgrouping/Projects/2023_10_HE_vs_CD10_follicles/data/CD10_40x/479210.png', outdir = 'output')
    # main(target_path = '/media/volodymyr/1TB_Store_B/Lymphoma_subgrouping/Projects/2023_10_HE_vs_CD10_follicles/data/HE_40x/474200.png', moving_path =  '/media/volodymyr/1TB_Store_B/Lymphoma_subgrouping/Projects/2023_10_HE_vs_CD10_follicles/data/CD10_40x/485672.png', outdir = 'output')
    # main(target_path = '/media/volodymyr/1TB_Store_B/Lymphoma_subgrouping/Projects/2023_10_HE_vs_CD10_follicles/data/HE_40x/474197.png', moving_path =  '/media/volodymyr/1TB_Store_B/Lymphoma_subgrouping/Projects/2023_10_HE_vs_CD10_follicles/data/CD10_40x/485758.png', outdir = 'output')
    # main(target_path = '/media/volodymyr/1TB_Store_B/Lymphoma_subgrouping/Projects/2023_10_HE_vs_CD10_follicles/data/HE_40x/474173.png', moving_path =  '/media/volodymyr/1TB_Store_B/Lymphoma_subgrouping/Projects/2023_10_HE_vs_CD10_follicles/data/CD10_40x/485985.png', outdir = 'output')
    # main(target_path = '/media/volodymyr/1TB_Store_B/Lymphoma_subgrouping/Projects/2023_10_HE_vs_CD10_follicles/data/HE_40x/474049.png', moving_path =  '/media/volodymyr/1TB_Store_B/Lymphoma_subgrouping/Projects/2023_10_HE_vs_CD10_follicles/data/CD10_40x/479379.png', outdir = 'output')