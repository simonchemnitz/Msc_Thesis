import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
from img_utils import crop_img
from skimage.feature import canny
from scipy.ndimage import convolve
file = "/users/simon/desktop/metric/mri/"

img = nib.load(file+"brainmask.mgz")
img = np.asarray(img.dataobj)

img = crop_img(img)

float_img = img.astype(np.float)

#Centered Gradient kernel in the x-direction
x_kern = np.array([[-1,-1,-1],
                    [0,0,0],
                    [1,1,1]])
#Centered Gradient kernel in the y-direction
y_kern = x_kern.T


fig, ax = plt.subplots(2,2, figsize = (12,12))

slice = 50
ax[0,0].imshow(float_img[:,:,slice], cmap = "gray")
ax[0,1].imshow(canny(float_img[:,:,slice]), cmap = "gray")

#Convolutions
ax[1,0].imshow( convolve(img[:,:,slice], x_kern),  cmap = "gray" )
ax[1,1].imshow( convolve(img[:,:,slice], y_kern),  cmap = "gray" )

#Titles
ax[0,0].set_title("$\mathcal{I}^{(k)}$", size = 25)
ax[0,1].set_title("$E(\mathcal{I}^{(k)})$", size = 25)
ax[1,0].set_title("$G_x(\mathcal{I}^{(k)})$", size = 25)
ax[1,1].set_title("$G_y(\mathcal{I}^{(k)})$", size = 25)

plt.setp(plt.gcf().get_axes(), xticks=[], yticks=[])

plt.show()

fig.savefig("aes_example.pdf")