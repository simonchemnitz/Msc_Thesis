import subprocess
import os
import glob


def mri_reg(sub, nifti_dir, output_dir):
    """
    Parameters
    ----------
    sub : str
        subject name as stated in the freesurfer SUBJECT_DIR
    nifti_dir : str
        Filepath for the nifti of the subject
    output_dir : str
        Filepath where output should be saved
    """

    registration_directory = output_dir + "regs/"+sub
    if not os.path.exists(registration_directory):
            print('New registration directory created:')
            print(registration_directory)
            os.makedirs(registration_directory)
            

    nifti_to_convert = glob.glob(nifti_dir+sub+"/*")
    for nifti in nifti_to_convert:
        if "MPR" not in nifti and "LOCALIZER" not in nifti:
            #name of the nifti files without .nii
            seq_name = os.path.basename(nifti)[:-4]
            #output file name
            output_name = seq_name+".lta"
            print(output_name)
            print(nifti)
            print()





nifti_dir = "/users/simon/desktop/data1/MRI_scans/nifti/"
output_dir = "/users/simon/desktop/data1/MRI_SCANS/"

subject = "MOCO_001"


mri_reg(subject, nifti_dir, output_dir)
    
