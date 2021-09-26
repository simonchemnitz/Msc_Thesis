import numpy as np
import nibabel 
import glob
from skimage.feature.texture import greycomatrix


def coent(img, levels = 256):
    vol_shape = np.shape(img)

    co_ent_matrix = np.zeros((levels,levels))

    