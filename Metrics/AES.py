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

slice = 90



x_kern = np.array([[-1,-1,-1],
                   [0,0,0],
                   [1,1,1]])

y_kern = x_kern.T

#Convolve slice
x_conv = convolve(img[slice,:,:], x_kern)
y_conv = convolve(img[slice,:,:], y_kern)

