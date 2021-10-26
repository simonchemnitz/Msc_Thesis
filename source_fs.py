import subprocess


moco_subject_dir = "/mnt/Data_Analysis_Children/Data_Recon_ALL/"
priv_subject_dir = "/data1/Chemnitz_Thomsen_Simon/MRI_scans/fs_test_simon/"
freesurfer_dir = "/usr/local/nru/freesurfer/fs71"



subprocess.run("csh")
#Set Subject directory
subprocess.run("setenv SUBJECTS_DIR "+priv_subject_dir)
#Set Freesurfer home directory
subprocess.run("setenv FREESURFER_HOME " + freesurfer_dir)

#source freesurfer
subprocess.run("source $FREESURFER_HOME/SetUpFreesurfer.csh")