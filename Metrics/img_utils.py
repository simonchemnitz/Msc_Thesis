"""
Code for various image utility functions
"""
import numpy as np

def crop_img(img):
    '''
    Parameters
    ----------
    img : numpy array
        Image to be cropped.
    
    Returns
    -------
    crop_img : numpy array
        Cropped image such that all slices 
        contain at least one non-zero entry
    '''
    #Indices where the img is non-zero
    indices = np.array(np.where(img>0))
    
    #Max and Min x values where img is non-zero
    xmin = np.min(indices[0])
    xmax = np.max(indices[0])
    #Max and Min y values where img is non-zero
    ymin = np.min(indices[1])
    ymax = np.max(indices[1])
    #Max and Min z values where img is non-zero
    zmin = np.min(indices[2])
    zmax = np.max(indices[2])
    
    #Return cropped img
    return img[xmin:xmax, ymin:ymax , zmin:zmax]


def bin_img(img, n_levels):
    '''
    Parameters
    ----------
    img : numpy array
        Image to bin.
    n_levels : int
        Number of levels to bin the intensities in
    
    Returns
    -------
    binned_img : numpy array
        Binned image, which has n_levels different 
        intensity values
    '''
    
    #Intensity values to map to
    vals, bins = np.histogram(img, bins = n_levels)

    #Bin image
    binned_img = np.digitize(img, bins, right = True)
    
    return binned_img
