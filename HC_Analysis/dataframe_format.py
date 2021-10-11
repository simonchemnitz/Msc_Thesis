import numpy as np
import pandas as pd
import glob
import os

from dataframe_utility import format_dataframe_metric, format_observer_dataframe


#File directories
main_dir = "Files_ig/"

#Metric directories
metric_in = main_dir+"Metric_results/"
metric_out = main_dir+"Metric_csv/"

#Observer directories
observer_in = main_dir+"Observer_Results/"
observer_out = main_dir+"Observer_csv/"

#Date of the latets evalution
relevant_date = "10_06"
#Filename reference
file_reference = "Values_AES_CoEnt_10_06_"



#Create empty metric dataframes for each subject


#DataFrame template
base_csv = pd.DataFrame(columns = ['aes', 'coent', 'moco', 'nod', 'RR', 
                                   'shake', 'still', 'pers_id', 'img_type'])

#Create base dataframes
subjects = glob.glob(metric_in+"*")

#for each subject create a dataframe
for sub in subjects:
    subject = sub[len(metric_in):]
    base_csv.to_csv(hc_out+subject+".csv", index = False)
