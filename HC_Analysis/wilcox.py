import numpy as np
import pandas as pd
import glob
import os

from scipy.stats import wilcoxon as cox


#Directory with the apropriate files
main_dir = "Files_ig/"

#Load dataframe of results
df = pd.read_csv(main_dir +"Metric_csv/"+"merged_metric.csv")

#Exclude observations with the following sequences
excl = ["ADC", "TRACEW_B0", "TRACEW_B1000"]
df = df.loc[~df["img_type"].isin(excl) ]

#Image sequnces to split on
img_types = df["img_type"].unique()

def wilcox_test(df, nod, RR, shake, img_type, metric):
    """
    Parameters
    ----------
    df : pandas DataFrame
        DataFrame containing data from 
        different sequences with respective
        metric scores.
    nod : Bool
        0/1, whether or not to calculate
        the cox statistic for a nodding sequnce.
        1 if nodding, 0 if still.
    RR : Bool
        0/1, whether or not to calculate
        the cox statistic for a reacquisition sequnce.
        1 if with reacquisition, 0 if not.
    shake : Bool
        0/1, whether or not to calculate
        the cox statistic for a shaking sequnce.
        1 if shaking, 0 if not shaking.
    img_type : str
        Type of image sequence to look at
        when calculating the statistic.
        Example: T1_MPR_, T1_TIRM_, T2_TSE_
    metric : str
        Which metric to test significance for.
        Example: "coent", "aes"
    Returns: stat, pval
        The test statistic
        and the corresponding pvalue
    """

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

    cox_df = cox_df.drop_duplicates()
    cox_df = cox_df.set_index(['pers_id', 'moco'])[metric].unstack().reset_index()

    #calculate the cox
    stat, pval =  cox( x = cox_df[0] , y = cox_df[1] )
    print( cox( x = cox_df[0] , y = cox_df[1] ))

    return stat, pval


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

