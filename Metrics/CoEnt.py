#Code is based on the article:
#Quantitative framework for prospective motion correction evaluation
#Nicolas Pannetier, Theano Stavrinos, Peter Ng, Michael Herbst, 
#Maxim Zaitsev, Karl Young, Gerald Matson, and Norbert Schuff
import numpy as np
#from skimage.feature.texture import greycomatrix   # this function is a Deprecated function
from skimage.feature import greycomatrix
from img_utils import bin_img, crop_img

def coent3d(img, brainmask = None, n_levels = 128, bin = True, crop = True, supress_zero = True):
    '''
    Parameters
    ----------
    img : numpy array
        Image for which the metrics should be calculated.
    n_levels : int
        Levels of intensities to bin image by
    bin : bool
        Whether or not to bin the image
    crop : bool 
        Whether or not to crop image/ delete empty slices 
    Returns
    -------
    CoEnt : float
        Co-Occurrence Entropy measure of the input image.
    '''
    #Apply brainmask if given one
    if brainmask is not None: #alternative type(brainmask) != type(None)
        img = img*brainmask
    #Crop image if crop is True
    if crop:
        img = crop_img(img)
    #Bin image if bin is True
    if bin:
        img = bin_img(img, n_levels=n_levels)
    #Scale imgage to have intensity values in [0,255]
    img = 255*(img/np.max(img))
    #Convert image to uint8
    #   as greycomatrix prefers uint8 as input
    img = img.astype(np.uint8)

    #Shape of the image/volume
    vol_shape = np.shape(img)

    #Empty matrix that will be the co-entropy matrix
    co_ent_matrix = np.zeros((256,256))

    #Generate 2d co-ent matrix for each slice
    for i in range(vol_shape[0]):
        #Temporary co-ent matrix
        tmp_comat = greycomatrix(img[i,:,:],
                                 distances = [1],
                                 angles = [0*(np.pi/2),
                                           1*(np.pi/2),
                                           2*(np.pi/2),
                                           3*(np.pi/2)])
        #greycomatrix will generate 4d array
        #The value P[i,j,d,theta] is the number of times 
        #that grey-level j occurs at a distance d and 
        #at an angle theta from grey-level i
        #as we only have one distance we just use 
        #tmp_comat[:,:,0,:]
        #As we want the total occurence not split on angles
        #we sum over axis 2.
        tmp_comat = np.sum(tmp_comat[:,:,0,:], axis = 2)
        #add the occurrences to the co-entropy matrix
        co_ent_matrix = co_ent_matrix + tmp_comat
    
    #Generate 2d co-ent matrix for each slice 
    #   to capture co-occurrence in the direction we sliced before
    for j in range(vol_shape[1]):
        #temporary co-ent matrix
        #note only pi,-pi as angles
        tmp_comat = greycomatrix(img[:,j,:],
                                 distances = [1], 
                                 angles = [1*(np.pi/2), 
                                           3*(np.pi/2)])
        #greycomatrix will generate 4d array
        #The value P[i,j,d,theta] is the number of times
        #that grey-level j occurs at a distance d and
        #at an angle theta from grey-level i
        #as we only have one distance we just use
        #tmp_comat[:,:,0,:]
        #As we want the total occurence not split on angles
        #we sum over axis 2.
        tmp_comat = np.sum(tmp_comat[:,:,0,:], axis = 2)
        #add the occurrences to the co-entropy matrix
        co_ent_matrix = co_ent_matrix + tmp_comat
    #Divide by 6 to get average occurance
    co_ent_matrix = (1/6)*co_ent_matrix
    if supress_zero:
        co_ent_matrix[0,0] = 0
    #Normalise
    co_ent_matrix = co_ent_matrix/np.sum(co_ent_matrix)
    #Take log2 to get entropy
    log_matrix = np.log2(co_ent_matrix)
    #Return the entropy
    return -np.nansum(co_ent_matrix*log_matrix)






def coent2d(img, brainmask = None, n_levels = 128, bin = True, crop = True, supress_zero = True):
    '''
    Parameters
    ----------
    img : numpy array
        Image for which the metrics should be calculated.
    n_levels : int
        Levels of intensities to bin image by
    bin : bool
        Whether or not to bin the image
    crop : bool 
        Whether or not to crop image/ delete empty slices 
    Returns
    -------
    CoEnt : float
        Co-Occurrence Entropy measure of the input image.
    '''
    #Apply brainmask if given one
    if brainmask is not None: #alternative type(brainmask) != type(None)
        img = img*brainmask
    #Crop image if crop is True
    if crop:
        img = crop_img(img)
    #Bin image if bin is True
    if bin:
        img = bin_img(img, n_levels=n_levels)
    #Scale imgage to have intensity values in [0,255]
    img = 255*(img/np.max(img))
    #Convert image to uint8
    #   as greycomatrix prefers uint8 as input
    img = img.astype(np.uint8)

    #Shape of the image/volume
    vol_shape = np.shape(img)

    comat = np.zeros((256,256))


    #Assuming volume is of the format
    # V(i,j,k) where k denotes the slice number
    for slice in range(vol_shape[2]):
        #Temporary co-occurrence matrix
        tmp_comat = greycomatrix(img[:,:,slice],
                                 distances = [1],
                                 angles = [0*(np.pi/2),
                                           1*(np.pi/2),
                                           2*(np.pi/2),
                                           3*(np.pi/2)])
        tmp_comat = np.sum(tmp_comat[:,:,0,:], axis = 2)
        comat = comat + tmp_comat
    
    #normallise comat
    comat =  comat/np.sum(comat)

    if supress_zero:
        comat[0,0] = 0

    #Take log2 to get entropy
    log_matrix = np.log2(comat)
    #Return the entropy
    return -np.nansum(comat*log_matrix)        


def coent(img, brainmask = None, n_levels = 128, bin = True, crop = True, supress_zero = True):
    '''
    Parameters
    ----------
    img : numpy array
        Image for which the metrics should be calculated.
    n_levels : int
        Levels of intensities to bin image by
    bin : bool
        Whether or not to bin the image
    crop : bool 
        Whether or not to crop image/ delete empty slices 
    Returns
    -------
    CoEnt : float
        Co-Occurrence Entropy measure of the input image.
    '''

    #check which function to use:
    img_vol = np.shape(img)

    if img_vol[2]<100:
        return coent2d(img, brainmask, n_levels, bin, crop, supress_zero)
    else: return coent3d(img, brainmask, n_levels, bin, crop, supress_zero)