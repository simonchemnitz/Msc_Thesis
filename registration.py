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
            regname = output_name

            #Perform bb registration
            print('bbregister --s ' + sub + ' --mov '+  movImg + ' --reg ' + regname + ' --t2 --init-best-header')
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




nifti_dir = "/users/simon/desktop/data1/MRI_scans/nifti/"
output_dir = "/users/simon/desktop/data1/MRI_SCANS/"

subject = "MOCO_001"


mri_reg(subject, nifti_dir, output_dir)
    
