import numpy as np
import nibabel as nib
import glob


#load img
img_dir = "C:/Users/simon/OneDrive/Skrivebord/UNI/MASTER_THESIS/recon/subj04/mri"
img = nib.load(img_dir + "brainmask.mgz")
img = np.asarray(img.dataobj)
img = img.astype(float)


