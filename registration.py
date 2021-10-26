import subprocess
import os
import glob


def bbregistration(sub, nifti_dir, output_dir):
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

    registration_directory = output_dir + "Registration/"+sub+"/regs/"
    print(registration_directory)
    #Check if the registration_directory exists
    #Create folder if it does not
    if not os.path.exists(registration_directory):
            print('New registration directory created:')
            print(registration_directory)
            os.makedirs(registration_directory)
            
    #List of nifti files to regi
    nifti_to_reg = glob.glob(nifti_dir+sub+"/*")
    #For each file perform registration
    for i, nifti in enumerate(nifti_to_reg):
        if "MPR" not in nifti and "LOCALIZER" not in nifti:
            #Image to move
            movImg = nifti

            #Name of the nifti files without .nii
            seq_name = os.path.basename(nifti)[:-4]
            #Output file name
            output_name = seq_name+".lta"
            regname = registration_directory+"/"+output_name

            #Perform bb registration
            #print('bbregister --s ' + sub + ' --mov '+  movImg + ' --reg ' + regname + ' --t2 --init-best-header')
            #subprocess.run('bbregister --s ' + sub + ' --mov '+  movImg + ' --reg ' + regname + ' --t2 --init-best-header', shell=True)

            #Print progress
            print()
            print(str(i)+"/"+str(len(nifti_to_reg)), "Done")
            print()
    print("+------------------------------------------------------------------+")
    print("|                                                                  |")
    print("|                    bbreg for: "+sub+" Done                      |")
    print("|                                                                  |")
    print("+------------------------------------------------------------------+")


def apply_registration(sub, recon_dir, nifti_dir, output_dir):
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
    #Binarize brainmask
    #Path to brainmask
    brainmask = recon_dir+sub+"/mri/brainmask.mgz"
    print(brainmask)
    #Output name
    binary_brainmask_nii = output_dir+sub+"/bin_brainmask.nii"
    print(binary_brainmask_nii)
    #subprocess.run('mri_binarize --i ' + brainmask + ' --o ' + binary_brainmask_nii + ' --match 0 --inv', shell=True)


    return None

nifti_dir = "/users/simon/desktop/data1/Chemnitz-Thomsen_Simon/MRI_scans/nifti/"
output_dir = "/users/simon/desktop/data1/Chemnitz-Thomsen_Simon/MRI_SCANS/"
recon_dir = "/users/simon/desktop/data1/Chemnitz-Thomsen_Simon/MRI_SCANS/fs_test_simon/"

subject = "MOCO_001"


bbregistration(subject, nifti_dir, output_dir)
    

apply_registration(subject, recon_dir, nifti_dir, output_dir)