import numpy as np
import pandas as pd
from scipy.stats import wilcoxon
import os 
import glob

#Directory where data is located
data_dir = "HC_Analysis/Files_ig/Merge_Output/"

#Dataframe containing metric results
df = pd.read_csv(data_dir + "All_metric.csv")
df["img_type"] = df["img_type"].str[:-4]# because formatted wrong
#Remove redundent results
df = df.drop(["aes_lap", "aes_pst"], axis = 1)
#Remove duplicates if any
df = df.set_index(["pers_id", "moco", "nod", "RR", "shake", "still", "img_type"])
df = df[~df.index.duplicated(keep='first')]
df = df.reset_index()

#Different image sequences to calculate the wilcoxon rank for
img_sequences = df["img_type"].unique()
#Metrics to calculate for
metrics = ["tg", "coent", "aes"]
#different motions to calculate it for
motions = ["nod", "still"]
#nod shake and still are mutually disjoint, only one column 
#is nonzero at a time.


def calc_wilcox_rank(df, df_to_merge, metric, motion, sequence, re_ac):
    sub_df = df.copy()
    sub_df = sub_df.loc[sub_df["img_type"] == sequence]
    sub_df = sub_df.loc[sub_df[motion] == 1]
    sub_df = sub_df.loc[sub_df["RR"] == re_ac]
    if sub_df.shape[0]>0:
        sub_df = sub_df[["pers_id", "moco"] + [metric]].pivot(index = "pers_id", columns = "moco", values = metric)
        stat, pval = wilcoxon(x = sub_df[0], y = sub_df[1])
        pvaldata = {"metric": [metric], "img_type": [sequence], "RR": [re_ac], "motion": [motion], "pvalue": [pval]}
        pval_df = pd.DataFrame.from_dict(pvaldata)
        merged_df = pd.concat([df_to_merge, pval_df])
        return merged_df
    else: return df_to_merge

#dataframe to contain all wilcoxon pvalues
wilcox_df = pd.DataFrame()
for racq in [0,1]:
    for sequence in img_sequences:
        for metric in metrics:
            for motion in motions:
                wilcox_df = calc_wilcox_rank(df = df, df_to_merge = wilcox_df, metric = metric,
                                 motion = motion, sequence = sequence, re_ac = racq)

wilcox_df.to_csv("wilcox_values.csv", index = False)