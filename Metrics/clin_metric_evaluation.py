import numpy as np
import pandas as pd
import os 
import glob
import nibabel as nib

#Metrics
from AES import aes
from CoEnt import coent
from Hannah_metrics import tgrad


def relevant_brain_mask(sub, nifti_file, brain_mask_dir):
    """
    Given a nifti file return the releant brain_mask.nii file

    Parameters
    ----------
    sub : str
        subject name as stated in the freesurfer SUBJECT_DIR
    nifti_file : str
        Filepath for the nifti file of the subject
    brain_mask_dir : str
        Filepath where brainmask files are stored
    """
    #Name of the relevant brainmask
    bm_file = "bm_" + os.path.basename(nifti_file)
    #Filepath for the brainmask file
    bm_path = brain_mask_dir + sub + "/" + bm_file

    #Check if file exists
    #and return it if it does
    if os.path.exists(bm_path):
        print("Mask found")
        print(bm_file)
        rel_bm = nib.load(bm_path)
        rel_bm = np.asarray(rel_bm.dataobj)
        return rel_bm
    #Else throw error
    else:
        print("Error:")
        print("Brainmask not found")
        print("File or directory" , bm_path, "Does not exist")
        return None

def evaluate_metrics(sub, nifti_file, brain_mask_dir, output_dir):
    """
    Given a nifti file return a dataframe 

    Parameters
    ----------
    sub : str
        subject name as stated in the freesurfer SUBJECT_DIR
    nifti_file : str
        Filepath for the nifti file of the subject
    brain_mask_dir : str
        Filepath where brainmask files are stored
    """
    #Load brainmask
    brainmask = relevant_brain_mask(sub, nifti_file, brain_mask_dir)
    if brainmask is None: return None


    img = nib.load(nifti_file)
    img = np.asarray(img.dataobj)
    print(np.shape(img))
    print(np.shape(brainmask))
    file_name = os.path.basename(nifti_file)
    seq = file_name[8:]

    metric_ditc = {"pers_id" : [sub],
                   "img_seq" : [seq],
                   "coent" : [coent(img, brainmask)],
                   "aes" : [aes(img, brainmask)],
                   "tgrad" : [tgrad(img, np.ndarray.flatten(brainmask))]
                   }

    df = pd.DataFrame.from_dict(metric_ditc)
    print(df)
    df.to_csv( output_dir + "Metrics/" + sub +"/"+ seq+".csv" , index = False)
    return df
 


base_dir = "/users/simon/desktop/mnt/mocodata1/Data_Analysis_Children/"
output_dir = base_dir + "output_simon/"
nifti_dir = base_dir + "NIFTIS/"
brain_mask_dir = output_dir + "Registration/"

subjects = ["MOCO_001","MOCO_002"]

sub = subjects[0]
nifti_files = glob.glob(nifti_dir+sub+"/*")
for file in nifti_files:
    print()
    evaluate_metrics(sub, file, brain_mask_dir, output_dir)
    print()


