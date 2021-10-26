import subprocess
import os
import glob


def mri_reg(sub, nifti_dir, output_dir):
    """
    Parameters
    ----------
    sub : str
        subject name
    """

    