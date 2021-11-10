#Code is based on the article:
#Quantitative framework for prospective motion correction evaluation
#Nicolas Pannetier, Theano Stavrinos, Peter Ng, Michael Herbst, 
#Maxim Zaitsev, Karl Young, Gerald Matson, and Norbert Schuff
import numpy as np
from skimage.feature import canny
from scipy.ndimage import convolve
from img_utils import crop_img, bin_img
import cv2
from skimage.morphology import thin
import math
import matplotlib.pyplot as plt
def aes(img, brainmask = None, sigma=np.sqrt(2), n_levels = 128, bin = False, crop = True, weigt_avg = False):
    '''
    Parameters
    ----------
    img : numpy array
        Image for which the metrics should be calculated.
    sigma : float
        Standard deviation of the Gaussian filter used 
        during canny edge detection.
    n_levels : int
        Levels of intensities to bin image by
    bin : bool
        Whether or not to bin the image
    crop : bool 
        Whether or not to crop image/ delete empty slices 
        
    Returns
    -------
    AES : float
        Average Edge Strength measure of the input image.
    '''
    #Apply brainmask if given one
    if brainmask is not None: #alternative type(brainmask) != type(None)
        img = img*brainmask
    #Crop image if crop is True
    if crop:
        img = crop_img(img)
    #Bin image if bin is True
    if bin:
        img = bin_img(img, n_levels = n_levels)
    #Centered Gradient kernel in the x-direction
    x_kern = np.array([[-1,-1,-1],
                       [0,0,0],
                       [1,1,1]])
    #Centered Gradient kernel in the y-direction
    y_kern = x_kern.T

    #Shape of volume/img
    vol_shape = np.shape(img)

    #Empty array to contain edge strenghts
    #Function returns the mean of this list
    es = []

    #weights for each slice
    #proportion of non zero pixels
    weights = []

    #Convert to float image
    img = img.astype(np.float)

    #For each slice calcule the edge strength
    for slice in range(vol_shape[2]):
        #Slice to do operations on
        im_slice = img[:,:,slice]

        #Weight, proportion of non zero pixels
        weights.append(np.mean(im_slice>0))

        #Convolve slice
        x_conv = convolve(im_slice, x_kern)
        y_conv = convolve(im_slice, y_kern)
        #Canny edge detector
        canny_img = canny(im_slice, sigma = sigma)
        #Numerator and denominator, to be divided
        #defining the edge strength of the slice
        numerator = np.sum(canny_img*( x_conv**2 + y_conv**2 ))
        denominator = np.sum(canny_img)

        #Calculate edge strength
        frac = np.sqrt(numerator)/denominator

        #Append the edge strength
        es.append(frac)
    es = np.array(es)
    #Remove nans
    es  = es[~np.isnan(es)]
    #Return the average edge strength
    if weigt_avg:
        return np.average(es, weights = weights)
    else: return np.mean(es)

def aes_lap(img, brainmask = None, sigma=np.sqrt(2), n_levels = 128, bin = False, crop = True, weigt_avg = False):
    '''
    Parameters
    ----------
    img : numpy array
        Image for which the metrics should be calculated.
    sigma : float
        Standard deviation of the Gaussian filter used 
        during canny edge detection.
    n_levels : int
        Levels of intensities to bin image by
    bin : bool
        Whether or not to bin the image
    crop : bool 
        Whether or not to crop image/ delete empty slices 
        
    Returns
    -------
    AES : float
        Average Edge Strength measure of the input image.
    '''
    #Apply brainmask if given one
    if brainmask is not None: #alternative type(brainmask) != type(None)
        img = img*brainmask
    #Crop image if crop is True
    if crop:
        img = crop_img(img)
    #Bin image if bin is True
    if bin:
        img = bin_img(img, n_levels = n_levels)
    #Centered Gradient kernel in the x-direction
    x_kern = np.array([[-1,-1,-1],
                       [0,0,0],
                       [1,1,1]])
    #Centered Gradient kernel in the y-direction
    y_kern = x_kern.T
    #Shape of volume/img
    vol_shape = np.shape(img)

    #Empty array to contain edge strenghts
    #Function returns the mean of this list
    es = []

    #weights for each slice
    #proportion of non zero pixels
    weights = []

    #Convert to float image
    img = img.astype(np.float)

    #For each slice calcule the edge strength
    for slice in range(vol_shape[2]):
        #Slice to do operations on
        im_slice = img[:,:,slice]

        #Weight, proportion of non zero pixels
        weights.append(np.mean(im_slice>0))

        #Convolve slice
        x_conv = convolve(im_slice, x_kern)
        y_conv = convolve(im_slice, y_kern)
        #Laplacian edge detection
        laplacian_img = cv2.Laplacian(im_slice,cv2.CV_64F, ksize = 15)
        binary_edge_image = thin(laplacian_img>0,2)
        #Numerator and denominator, to be divided
        #defining the edge strength of the slice
        numerator = np.sum(binary_edge_image*( x_conv**2 + y_conv**2 ))
        denominator = np.sum(binary_edge_image)

        #Calculate edge strength
        frac = np.sqrt(numerator)/denominator

        #Append the edge strength
        es.append(frac)
    es = np.array(es)
    #Remove nans
    es  = es[~np.isnan(es)]
    #Return the average edge strength
    if weigt_avg:
        return np.average(es, weights = weights)
    else: return np.mean(es)


#PST EDGE DETECTOR 
#@author: Madhuri Suthar, UCLA
#GitHub: JalaliLabUCLA
def cart2pol(x, y):
    theta = np.arctan2(y, x)
    rho = np.hypot(x, y)
    return (theta, rho)    
def PST(I,LPF,Phase_strength,Warp_strength):
    L=0.5
    x = np.linspace(-L, L, I.shape[0])
    y = np.linspace(-L, L, I.shape[1])
    [X1, Y1] =(np.meshgrid(x, y))
    X=X1.T
    Y=Y1.T
    [THETA,RHO] = cart2pol(X,Y)

    # Apply localization kernel to the original image to reduce noise
    Image_orig_f=((np.fft.fft2(I)))  
    expo = np.fft.fftshift(np.exp(-np.power((np.divide(RHO, math.sqrt((LPF**2)/np.log(2)))),2)))
    Image_orig_filtered=np.real(np.fft.ifft2((np.multiply(Image_orig_f,expo))))
    # Constructing the PST Kernel
    PST_Kernel_1=np.multiply(np.dot(RHO,Warp_strength), np.arctan(np.dot(RHO,Warp_strength)))-0.5*np.log(1+np.power(np.dot(RHO,Warp_strength),2))
    PST_Kernel=PST_Kernel_1/np.max(PST_Kernel_1)*Phase_strength
    # Apply the PST Kernel
    temp=np.multiply(np.fft.fftshift(np.exp(-1j*PST_Kernel)),np.fft.fft2(Image_orig_filtered))
    Image_orig_filtered_PST=np.fft.ifft2(temp)

    # Calculate phase of the transformed image
    PHI_features=np.angle(Image_orig_filtered_PST)
     

    out=PHI_features
    return (out, PST_Kernel)


def aes_pst(img, brainmask = None, sigma=np.sqrt(2), n_levels = 128, bin = False, crop = True, weigt_avg = False):
    '''
    Parameters
    ----------
    img : numpy array
        Image for which the metrics should be calculated.
    sigma : float
        Standard deviation of the Gaussian filter used 
        during canny edge detection.
    n_levels : int
        Levels of intensities to bin image by
    bin : bool
        Whether or not to bin the image
    crop : bool 
        Whether or not to crop image/ delete empty slices 
        
    Returns
    -------
    AES : float
        Average Edge Strength measure of the input image.
    '''
    #Apply brainmask if given one
    if brainmask is not None: #alternative type(brainmask) != type(None)
        img = img*brainmask
    #Crop image if crop is True
    if crop:
        img = crop_img(img)
    #Bin image if bin is True
    if bin:
        img = bin_img(img, n_levels = n_levels)
    #Centered Gradient kernel in the x-direction
    x_kern = np.array([[-1,-1,-1],
                       [0,0,0],
                       [1,1,1]])
    #Centered Gradient kernel in the y-direction
    y_kern = x_kern.T
    #Shape of volume/img
    vol_shape = np.shape(img)

    #Empty array to contain edge strenghts
    #Function returns the mean of this list
    es = []

    #weights for each slice
    #proportion of non zero pixels
    weights = []

    #Convert to float image
    img = img.astype(np.float)

    #For each slice calcule the edge strength
    for slice in range(vol_shape[2]):
        #Slice to do operations on
        im_slice = img[:,:,slice]

        #Weight, proportion of non zero pixels
        weights.append(np.mean(im_slice>0))

        #Convolve slice
        x_conv = convolve(im_slice, x_kern)
        y_conv = convolve(im_slice, y_kern)
        #Laplacian edge detection
        pst_img, pst = PST(1-im_slice,LPF=0.08,Phase_strength =0.0001,Warp_strength=0.001)
        binary_edge_image = thin(pst_img>0,1)
        #Numerator and denominator, to be divided
        #defining the edge strength of the slice
        numerator = np.sum(binary_edge_image*( x_conv**2 + y_conv**2 ))
        denominator = np.sum(binary_edge_image)

        #Calculate edge strength
        frac = np.sqrt(numerator)/denominator

        #Append the edge strength
        es.append(frac)
    es = np.array(es)
    #Remove nans
    es  = es[~np.isnan(es)]
    #Return the average edge strength
    if weigt_avg:
        return np.average(es, weights = weights)
    else: return np.mean(es)