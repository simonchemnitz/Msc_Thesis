import subprocess
import os
import glob


def bbregistration(sub, nifti_dir, output_dir):
    """
    Calculates the registration transform: using FreeSurfer functions 
    bbregister for T2 images

    Parameters
    ----------
    sub : str
        subject name as stated in the freesurfer SUBJECT_DIR
    nifti_dir : str
        Filepath for the nifti of the subject
    output_dir : str
        Filepath where output should be saved

    Returns
    -------
    None
    """
    #Filepath for the registration outputs
    registration_directory = output_dir + "Registration/"+sub+"/regs/"

    #Check if the registration_directory exists
    #Create folder if it does not exist
    if not os.path.exists(registration_directory):
            print('New registration directory created:')
            print(registration_directory)
            os.makedirs(registration_directory)
            
    #List of nifti files to register
    nifti_to_reg = glob.glob(nifti_dir+sub+"/*T2*")

    #For each file perform registration
    for i, nifti in enumerate(nifti_to_reg):
        #Image to move
        movImg = nifti

        #Name of the nifti files without .nii
        seq_name = os.path.basename(nifti)[:-4]
        #Output file name
        output_name = seq_name+".lta"
        #Output path
        regname = registration_directory+output_name

        #Perform bb registration
        subprocess.run('bbregister --s ' + sub + ' --mov '+  movImg + ' --reg ' + regname + ' --t2 --init-best-header', shell=True)
        
        #Print progress
        print()
        print(str(i+1)+"/"+str(len(nifti_to_reg)), " BBregs Done for " + sub)
        print()
    print("+------------------------------------------------------------------+")
    print("|                                                                  |")
    print("|                    bbreg for: "+sub+" Done                      |")
    print("|                                                                  |")
    print("+------------------------------------------------------------------+")


def apply_registration(sub, recon_dir, nifti_dir, output_dir):
    """
    Applies transforms (saved in output_dir/Registration/sub/regs) to the 
    brainmasks for T2 scans

    Parameters
    ----------
    sub : str
        subject name as stated in the freesurfer SUBJECT_DIR
    recon_dir : str
        Filepath for the freesurfer SUBJECT_DIR
    nifti_dir : str
        Filepath for the nifti of the subject
    output_dir : str
        Filepath where output should be saved

    Returns
    -------
    None
    """
    #Binarize brainmask
    #Path to brainmask
    brainmask = recon_dir+sub+"/mri/brainmask.mgz"
    #Output name for the binirized brainmask
    binary_brainmask_nii = output_dir+ "Registration/"+sub+"/bin_brainmask.nii"
    #Binirize mask
    subprocess.run('mri_binarize --i ' + brainmask + ' --o ' + binary_brainmask_nii + ' --match 0 --inv', shell=True)

    #T2 Nifti files to apply transformation to
    nifti_to_reg = glob.glob(nifti_dir+sub+"/*T2*")

    #Apply transformation
    for i, nifti in enumerate(nifti_to_reg):
        #sequence name eg: T2_TSE_TRA_512_TE115MS_0009
        seq_name = os.path.basename(nifti)[:-4]

        #Brain mask output name
        bm_mov = output_dir+ "Registration/" +sub+ "/bm_"+ seq_name + ".nii"

        #T2 image to register to
        T2_img = nifti

        #registration .lta file
        regname = output_dir + "Registration/"+sub+"/regs/"+seq_name+".lta"

        #Perform transformation
        subprocess.run('mri_vol2vol --mov ' + T2_img + ' --targ ' + binary_brainmask_nii + ' --o ' + bm_mov + ' --lta ' + regname + ' --inv --nearest', shell=True)
        
        #Print progress
        print()
        print(str(i+1)+"/"+str(len(nifti_to_reg)), " Transforms Done for " + sub)
        print()
    
    print("+------------------------------------------------------------------+")
    print("|                                                                  |")
    print("|              Transformation for: "+sub+" Done                   |")
    print("|                                                                  |")
    print("+------------------------------------------------------------------+")
    return None


base_dir = "/users/simon/desktop/mnt/mocodata1/Data_Analysis_Children/"
nifti_dir =  base_dir + "NIFTIS/"
output_dir = base_dir + "output_simon/"
recon_dir =  base_dir + "Data_Recon_ALL/"

subjects = ["MOCO_001","MOCO_002"]

for subject in subjects:
    bbregistration(subject, nifti_dir, output_dir)
    apply_registration(subject, recon_dir, nifti_dir, output_dir)