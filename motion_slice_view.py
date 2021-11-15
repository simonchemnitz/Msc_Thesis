import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
from skimage.feature import canny
from scipy.ndimage import convolve
#Directories
nifti_dir = "/users/simon/desktop/data1/Chemnitz-Thomsen_Simon/MRI_scans/nifti/MOCO_001/"
bm_dir = "/users/simon/desktop/data1/Chemnitz-Thomsen_Simon/MRI_scans/Registration/MOCO_001/"
recon_dir = "/users/simon/desktop/data1/Chemnitz-Thomsen_Simon/MRI_scans/fs_test_simon/MOCO_001/mri/"

#Centered Gradient kernel in the x-direction
y_kern = np.array([[-1,-1,-1],
                   [0,0,0],
                   [1,1,1]])
#Centered Gradient kernel in the y-direction
x_kern = y_kern.T
#Load images
nod_img = nib.load(nifti_dir + "TCLMOCO_OFF_NOD_T2_TSE_TRA_512_TE115MS_0009.nii")
nod_img = np.asarray(nod_img.dataobj)

stilimg = nib.load(nifti_dir + "TCLMOCO_ON_STILL_T2_TSE_TRA_512_TE115MS_0008.nii")
stilimg = np.asarray(stilimg.dataobj)

nod_bm = nib.load(bm_dir+"bm_TCLMOCO_OFF_NOD_T2_TSE_TRA_512_TE115MS_0009.nii")
nod_bm = np.asarray(nod_bm.dataobj)

stilbm = nib.load(bm_dir+"bm_TCLMOCO_ON_STILL_T2_TSE_TRA_512_TE115MS_0008.nii")
stilbm = np.asarray(stilbm.dataobj)

nod_img = nod_img*nod_bm
stilimg = stilimg*stilbm

imslice = 13
nim = nod_img[:,:,imslice].astype(np.float)
sim = stilimg[:,:,imslice].astype(np.float)

#Create figure
c = 3
figsize = (16,16)
fontsize = 24
#Orig and Canny
fig, ax = plt.subplots(2,2, figsize = figsize)


ax[0,0].imshow(nim , cmap = "gray")
ax[0,0].axis("off")
ax[0,0].set_title("Nodding", fontsize = fontsize)

ax[0,1].imshow(canny(nim, sigma = np.sqrt(2)) , cmap = "gray")
ax[0,1].axis("off")
ax[0,1].set_title("Canny edge detected", fontsize = fontsize)

ax[1,0].imshow(sim , cmap = "gray")
ax[1,0].axis("off")
ax[1,0].set_title("Still", fontsize = fontsize)

ax[1,1].imshow(canny(sim, sigma = np.sqrt(2)) , cmap = "gray")
ax[1,1].axis("off")
ax[1,1].set_title("Canny edge detected", fontsize = fontsize)


fig.savefig("t2_aes_slice_canny.png",  bbox_inches = 'tight')

#convolved
fig, ax = plt.subplots(2,2, figsize = figsize)


ax[0,0].imshow(convolve(nim, x_kern), cmap = "gray")
ax[0,0].axis("off")
ax[0,0].set_title("Nodding convolved x", fontsize = fontsize)

ax[0,1].imshow(convolve(nim, y_kern), cmap = "gray")
ax[0,1].axis("off")
ax[0,1].set_title("Nodding convolved y", fontsize = fontsize)

ax[1,0].imshow(convolve(sim, x_kern), cmap = "gray")
ax[1,0].axis("off")
ax[1,0].set_title("Still convolved x", fontsize = fontsize)

ax[1,1].imshow(convolve(sim, y_kern), cmap = "gray")
ax[1,1].axis("off")
ax[1,1].set_title("Still convolved y", fontsize = fontsize)


plt.savefig("t2_aes_slice_convolve.png", bbox_inches = "tight")