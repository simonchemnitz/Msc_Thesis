import numpy as np
import nibabel 
import glob
from skimage.feature.texture import greycomatrix


def coent(img, levels = 256):
    vol_shape = np.shape(img)

    co_ent_matrix = np.zeros((levels,levels))

    for i in range(vol_shape[0]):
        tmp_comat = greycomatrix(img[i,:,:],
                                 levels = levels,
                                 distance = [1],
                                 angles = [np.pi,-np.pi, 
                                           np.pi/2,-np.pi/2])
        tmp_comat = np.sum(tmp_comat[:,:,0,:], axis = 2)
        
        co_ent_matrix = co_ent_matrix+tmp_comat
    for j in range(vol_shape[1]):
        tmp_comat = greycomatrix(img[:,j,:],
        levels = levels, distance = [1])