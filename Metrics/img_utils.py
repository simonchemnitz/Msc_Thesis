"""
Code for various image utility functions
"""
import numpy as np
import subprocess
import os
import glob

def crop_img(img):
    '''
    Parameters
    ----------
    img : numpy array
        Image to be cropped.
    
    Returns
    -------
    crop_img : numpy array
        Cropped image such that all slices 
        contain at least one non-zero entry
    '''
    #Indices where the img is non-zero
    indices = np.array(np.where(img>0))
    
    #Max and Min x values where img is non-zero
    xmin = np.min(indices[0])
    xmax = np.max(indices[0])
    #Max and Min y values where img is non-zero
    ymin = np.min(indices[1])
    ymax = np.max(indices[1])
    #Max and Min z values where img is non-zero
    zmin = np.min(indices[2])
    zmax = np.max(indices[2])
    
    #Return cropped img
    return img[xmin:xmax, ymin:ymax , zmin:zmax]


def bin_img(img, n_levels):
    '''
    Parameters
    ----------
    img : numpy array
        Image to bin.
    n_levels : int
        Number of levels to bin the intensities in
    
    Returns
    -------
    binned_img : numpy array
        Binned image, which has n_levels different 
        intensity values
    '''
    
    #Intensity values to map to
    vals, bins = np.histogram(img, bins = n_levels)

    #Bin image
    binned_img = bins[np.digitize(img, bins, right = True)]
    
    #Return binned image
    return binned_img


def is_dicom(filepath):
    """
    Given a file check if it is of dicom format
    
    Parameters
    ----------
    filepath : str
        filepath for the file that should be checked
    
    Returns
    -------
        True if it is a dicom False if not
    """
    #Split the filepath
    lst = filepath.split(".")
    #If the file ends with IMA r DCM return True
    if lst[-1].lower() == "ima" or lst[-1].lower() == "dcm":
        return True
    else: return False

def dicom2nifti(patient_id, dicom_directory, nifti_directory):
    '''
    Converts dicom image to nifti using
    FreeSurfers mri_convert
    
    
    Parameters
    ----------
    dicom_folder : str
        Filepath for the folder containing the .IMA or .dcm files.
    dicom_directory : str
        Filepath for the folder containing all dicom folders
    nifti_directory : str
        Filepath for the nifti directory
        
    Returns
    -------
    in_volume : str
        Filepath to the first dicom file
    out_volume : str
        Filepath to the nifti file
    '''
    
    #List of all dicom folders for the patient
    for dicom_fold in glob.glob(patient_id+"*/"):
        #First file in the dicom folder
        in_volume = glob.glob(dicom_fold+"*")[0]
        #Check if the file is dicom format
        if is_dicom(in_volume):
            #Output volume
            out_volume = nifti_directory+patient_id[len(dicom_directory):]+ dicom_fold[len(patient):-1]+".nii"
            
            print(in_volume)
            print(out_volume)
            print("----------")
            print()
            #Convert to nifti with mri_convert
            subprocess.run('mri_convert ' + in_volume + ' ' + out_volume+' --no-dwi', shell=True)
            

            
def convert_all(dicom_directory, nifti_directory):
    for patient in glob.glob(dicom_directory+"*/"):
        dicom2nifti(patient, dicom_directory, nifti_directory)