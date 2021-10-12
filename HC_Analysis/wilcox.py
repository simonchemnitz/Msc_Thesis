import numpy as np
import pandas as pd
import glob
import os

from scipy.stats import wilcoxon as cox



main_dir = "Files_ig/"

df = pd.read_csv(main_dir + "observer_merged_metric.csv")

def wilcox_test(df, nod, RR,shake, img_type, metric):


    #create a copy of the DataFrame
    cox_df = df.copy()
    #Subset for the relevant data
    cox_df = cox_df.loc[cox_df["nod"] == nod]
    cox_df = cox_df.loc[cox_df["RR"] == RR]
    cox_df = cox_df.loc[cox_df["shake"] == shake]
    cox_df = cox_df.loc[cox_df["img_type"] == img_type]

    #Drop redundant columns
    cox_df = cox_df.drop(["nod", "still", "RR", "shake", "img_type"], axis = 1)

    #Subset for only relevant columnds
    cox_df = cox_df[["pers_id", "moco", metric]]

    cox_df = cox_df.set_index(['pers_id', 'moco'])[metric].unstack().reset_index()

    #calculate the cox
    print( cox( x = cox_df[0] , y = cox_df[1] ) )




img_types = df["img_type"].unique()


print()
print()
print("                        Wilcoxon rank test:")
print()
print()


print("+------------------------------------------------------------------+")
print("|                                                                  |")
print("|                            CoEnt                                 |")
print("|                                                                  |")
print("+------------------------------------------------------------------+")
for img_type in img_types:
    print()
    print(img_type)
    print("   Nod")
    wilcox_test(df, nod = 1, RR = 0,shake = 0, img_type = img_type ,metric = "coent")
    print("   Still")
    wilcox_test(df, nod = 0, RR = 0,shake = 0, img_type = img_type ,metric = "coent")

print("+------------------------------------------------------------------+")
print("|                                                                  |")
print("|                             AES                                  |")
print("|                                                                  |")
print("+------------------------------------------------------------------+")
for img_type in img_types:
    print()
    print(img_type)
    print("   Nod")
    wilcox_test(df, nod = 1, RR = 0,shake = 0, img_type = img_type ,metric = "aes")
    print("   Still")
    wilcox_test(df, nod = 0, RR = 0,shake = 0, img_type = img_type ,metric = "aes")

