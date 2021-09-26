import numpy as np
import nibabel as nib
import glob
from skimage.feature import canny
from scipy.ndimage import convolve
import matplotlib.pyplot as plt


#load img
img_dir = "C:/Users/simon/OneDrive/Skrivebord/UNI/MASTER_THESIS/recon/subj04/mri/"
img = nib.load(img_dir + "brainmask.mgz")
img = np.asarray(img.dataobj)
img = img.astype(float)


def aes(img):
    '''
    Parameters
    ----------
    img : numpy array
        image for which the metrics should be calculated.

    Returns
    -------
    AES : float
        Average Edge Strength measure of the input image.
    '''
    x_kern = np.array([[-1,-1,-1],
                   [0,0,0],
                   [1,1,1]])

    y_kern = x_kern.T

    #shape of volume/img
    vol_shape = np.shape(img)

    #Empty array to contain edge strenghts
    es = []

    #for each slice calcule the edge strength
    for slice in range(vol_shape[0]):


        #Convolve slice
        x_conv = convolve(img[slice,:,:], x_kern)
        y_conv = convolve(img[slice,:,:], y_kern)
        canny_img = canny(img[slice,:,:])

        numerator = np.sum(canny_img*( x_conv**2 + y_conv**2 ))
        denominator = np.sum(canny_img)

        #note different result if we divide by zero then take nanmean
        #compared to replacing frac value by zero then nanmean
        #if we dont check we can remove if statement and just use 
        #np.nanmean
        if denominator>0:
            frac = np.sqrt(numerator)/denominator
        else: frac = 0
        es.append(frac)

    return np.nanmean(es)

print(aes(img))
