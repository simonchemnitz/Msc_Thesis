import numpy as np
import nibabel as nib
import glob
from skimage.feature import canny

#load img
img_dir = "C:/Users/simon/OneDrive/Skrivebord/UNI/MASTER_THESIS/recon/subj04/mri"
img = nib.load(img_dir + "brainmask.mgz")
img = np.asarray(img.dataobj)
img = img.astype(float)



x_kern = np.array([[-1,-1,-1],
                   [0,0,0],
                   [1,1,1]])

y_kern = x_kern.T

print(x_kern)
print(y_kern)