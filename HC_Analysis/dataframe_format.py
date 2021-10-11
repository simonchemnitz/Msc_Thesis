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

"""
'//////////////////////////////////////////////////////'
'//                                                  //'
'//               Metrics scores                     //'
'//                                                  //'
'//////////////////////////////////////////////////////'
"""

#Create empty metric dataframes for each subject


#DataFrame template
base_csv = pd.DataFrame(columns = ['aes', 'coent', 'moco', 'nod', 'RR', 
                                   'shake', 'still', 'pers_id', 'img_type'])

#Create base dataframes
subjects = glob.glob(metric_in+"*")

#for each subject create a dataframe
for sub in subjects:
    subject = sub[len(metric_in):]
    base_csv.to_csv(metric_out+subject+".csv", index = False)


#Format subject metric-DataFrames
#Folders for each subject
subjects = glob.glob(metric_in+"*")
#Format all metric files
for subject in subjects:
    for file in glob.glob(subject+"/*"):
        format_dataframe_metric(file)


#Merge all metric scores
#DataFrame template
merged_df = pd.DataFrame(columns = ['aes', 'coent', 'moco', 'nod', 'RR', 
                                   'shake', 'still', 'pers_id', 'img_type'])

#For each subject-csv file merge
for file in glob.glob(metric_out+"*"):
    if "merged" not in file:
        #load file 
        file_df = pd.read_csv(file)
        merged_df = pd.concat([merged_df, file_df])
#save the merged dataframe
merged_df.to_csv(metric_out+"merged_metric.csv", index = False)



"""
'//////////////////////////////////////////////////////'
'//                                                  //'
'//                Observer scores                   //'
'//                                                  //'
'//////////////////////////////////////////////////////'
"""


#Format all ovserver files
for file in glob.glob(observer_in+"*"):
    format_observer_dataframe(file)


#Merge all observer scores
#DataFrame template
merged_df = pd.DataFrame(columns = ["w_avg","nod","RR","moco",
                                    "pers_id","shake","still","img_type"])

for file in glob.glob(observer_out+"*"):
    #Load file
    file_df = pd.read_csv(file)
    #Merge dataframe
    merged_df = pd.concat([merged_df, file_df])
merged_df.to_csv(observer_out+"merged_observer.csv", index = False)




"""
'//////////////////////////////////////////////////////'
'//                                                  //'
'//      Merge Metrics and Observer scores           //'
'//                                                  //'
'//////////////////////////////////////////////////////'
"""
#Load dataframes
metric_dataframe = pd.read_csv(metric_out+"merged_metric.csv")
observer_dataframe = pd.read_csv(observer_out+"merged_observer.csv")
#List of image types that were scored
#by observers
im_types = observer_dataframe["img_type"].unique()

#Subset metrics to only contain data on image types
#that were scored by observers
metric_dataframe = metric_dataframe.loc[metric_dataframe["img_type"].isin(im_types)]

#Set joint index
metric_dataframe = metric_dataframe.set_index(["pers_id", "img_type", "moco", "still", "nod", "shake", "RR"])
observer_dataframe = observer_dataframe.set_index(["pers_id", "img_type", "moco", "still", "nod", "shake", "RR"])

#Merge the two dataframes
merged_dataframe =  metric_dataframe.join(observer_dataframe).reset_index()
merged_dataframe = merged_dataframe.dropna()


merged_dataframe =  metric_dataframe.join(observer_dataframe).reset_index()
merged_dataframe = merged_dataframe.dropna()



merged_dataframe.to_csv(main_dir+"observer_merged_metric.csv", index = False)