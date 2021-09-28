import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

from AES import aes
from CoEnt import coent
from img_utils import crop_img, bin_img


img_dir = "C:/Users/simon/OneDrive/Skrivebord/metric/mri/"

img = nib.load(img_dir + "brainmask.mgz")
img = np.asarray(img.dataobj)


img = crop_img(img)
img = bin_img(img, n_levels= 128)


print("Co-Ent" , coent(img))
print("AES" , aes(img))