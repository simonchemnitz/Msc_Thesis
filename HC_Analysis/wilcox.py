import numpy as np
import pandas as pd
import glob
import os

from scipy.stats import wilcoxon as cox



main_dir = "Files_ig/"

df = pd.read_csv(main_dir + "observer_merged_metric.csv")




def wilcox_test(df, nod, RR,shake, metric):

    #create a copy of the DataFrame
    cox_df = df.copy()
    #Subset for the relevant data
    cox_df = cox_df.loc[cox_df["nod"] == nod]
    cox_df = cox_df.loc[cox_df["RR"] == RR]
    cox_df = cox_df.loc[cox_df["shake"] == shake]

    #Drop redundant columns
    cox_df = cox_df.drop(["nod", "still", "RR", "shake"], axis = 1)

    #Subset for only relevant columnds
    cox_df = cox_df[["pers_id", "img_type", "moco", metric]]

    cox_df = cox_df.set_index(['pers_id', 'img_type', 'moco'])[metric].unstack().reset_index()
    #print(cox_df)

    print( cox( x = cox_df[0] , y = cox_df[1] ) )




wilcox_test(df, nod = 1, RR = 0,shake = 0, metric = "aes")