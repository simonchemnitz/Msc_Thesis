#Code is based on the article:
#Quantitative framework for prospective motion correction evaluation
#Nicolas Pannetier, Theano Stavrinos, Peter Ng, Michael Herbst, 
#Maxim Zaitsev, Karl Young, Gerald Matson, and Norbert Schuff
import numpy as np
from skimage.feature.texture import greycomatrix


def coent(img, levels = 256):
    '''
    Parameters
    ----------
    img : numpy array
        Image for which the metrics should be calculated.
    levels : int
        Levels of intensities to bin by
    
    Returns
    -------
    CoEnt : float
        Co-Occurrence Entropy measure of the input image.
    '''

    #Convert image to int
    #as greycomatrix only takes int input
    img = img.astype(int)

    #Shape of the image/volume
    vol_shape = np.shape(img)

    #Empty matrix that will be the co-entropy matrix
    co_ent_matrix = np.zeros((levels,levels))

    #Generate 2d co-ent matrix for each slice
    for i in range(vol_shape[0]):
        #temporary co-ent matrix
        tmp_comat = greycomatrix(img[i,:,:],
                                 levels = levels,
                                 distances = [1],
                                 angles = [np.pi,-np.pi, 
                                           np.pi/2,-np.pi/2])
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
        co_ent_matrix = co_ent_matrix+tmp_comat
    
    #generate 2d co-ent matrix for each slice 
    #to capture co-occurrence in the direction we sliced before
    for j in range(vol_shape[1]):
        #temporary co-ent matrix
        #note only pi,-pi as angles
        tmp_comat = greycomatrix(img[:,j,:],
                                 levels = levels, 
                                 distances = [1], 
                                 angles = [np.pi, -np.pi])
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
    #Normalise
    co_ent_matrix = co_ent_matrix/np.sum(co_ent_matrix)
    #Take log2 to get entropy
    log_matrix = np.log2(co_ent_matrix)
    #Return the entropy
    return -np.nansum(co_ent_matrix*log_matrix)
