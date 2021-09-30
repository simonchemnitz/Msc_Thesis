#Code is based on the article:
#Quantitative framework for prospective motion correction evaluation
#Nicolas Pannetier, Theano Stavrinos, Peter Ng, Michael Herbst, 
#Maxim Zaitsev, Karl Young, Gerald Matson, and Norbert Schuff
import numpy as np
from skimage.feature import canny
from scipy.ndimage import convolve





def aes(img, brainmask = None, sigma=1):
    '''
    Parameters
    ----------
    img : numpy array
        Image for which the metrics should be calculated.
    sigma : float
        Standard deviation of the Gaussian filter used 
        during canny edge detection.
    Returns
    -------
    AES : float
        Average Edge Strength measure of the input image.
    '''

    if brainmask != None:
        img = img*brainmask
    #Centered Gradient kernel in the x-direction
    x_kern = np.array([[-1,-1,-1],
                       [0,0,0],
                       [1,1,1]])
    #Centered Gradient kernel in the y-direction
    y_kern = x_kern.T

    #shape of volume/img
    vol_shape = np.shape(img)

    #Empty array to contain edge strenghts
    #Function returns the mean of this list
    es = []

    #for each slice calcule the edge strength
    for slice in range(vol_shape[0]):
        #Convolve slice
        x_conv = convolve(img[slice,:,:], x_kern)
        y_conv = convolve(img[slice,:,:], y_kern)
        #Canne edge detector
        canny_img = canny(img[slice,:,:], sigma = sigma)
        #Numerator and denominator, to be divided
        #defining the edge strength of the slice
        numerator = np.sum(canny_img*( x_conv**2 + y_conv**2 ))
        denominator = np.sum(canny_img)

        #note different result if we divide by zero then take nanmean
        #compared to replacing frac value by zero then nanmean
        #if we dont check we can remove if statement and just use 
        #np.nanmean
        if denominator>0:
            frac = np.sqrt(numerator)/denominator
        else: frac = 0
        #Append the edge strength
        es.append(frac)
    #Return the average edge strength
    return np.nanmean(es)

