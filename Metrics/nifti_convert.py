"""
+------------------------------------------------------------------+
|                                                                  |
|                  Remember to run with python3,                   |
|                  ie: python3 nifti_convert.py                    |
|                                                                  |
+------------------------------------------------------------------+
"""
from img_utils import convert_all

#Dicom and Nifti dir
#read as (in and out dir)
dicomdir = "/data1/Chemnitz-Thomsen_Simon/MRI_scans/2021_09_01_Simon/MOCO_TRACOLINE_TEST_20210901_135204_354000"
niftidir = "/data1/Chemnitz-Thomsen_Simon/MRI_scans/2021_09_01_Simon/nifti"



print("+------------------------------------------------------------------+")
print("|                                                                  |")
print("|                    Converting Dicom to Nifti                     |")
print("|                                                                  |")
print("+------------------------------------------------------------------+")


convert_all(dicomdir, niftidir)


print("+------------------------------------------------------------------+")
print("|                                                                  |")
print("|                       Nifti Conversion Done                      |")
print("|                                                                  |")
print("+------------------------------------------------------------------+")