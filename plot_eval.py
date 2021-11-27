import pandas as pd
import os
import glob
from plot_utility import correlation_plot, starbox_plot, correlation_subplot, box_subplot, clinical_cor_plot
import matplotlib.pyplot as plt
data_dir = "/Users/simon/Documents/GitHub/Msc_Thesis/HC_Analysis/Files_ig"
out_dir = "/Users/simon/Documents/GitHub/Msc_Thesis/Figures/"
wilcox_df = pd.read_csv("/Users/simon/Documents/GitHub/Msc_Thesis/wilcox_values.csv")

print("Sequences: ")
title_names = {"coent": "Co-Occurence Entropy",
             "aes": "Average Edge Stength",
             "tg": "TennenGrad"}
ylabel_names = {"coent": "CoEnt(arb'U)",
             "aes": "AES(arb'U)",
             "tg": "TG(arb'U)"}

marker_color = (47, 122, 154)
line_color  = (83, 201, 250)

dblue = (47,122,154)
lblue = (83, 201, 250)

dpink = (126,25,82)
lpink = (231,47,149)

palette = [dblue, dpink]
palette = [dblue, dpink, lpink]


box_df = pd.read_csv(data_dir + "/Merge_Output/"+"All_metric.csv")
box_df["img_type"] = box_df["img_type"].str[:-4]
box_df = box_df.set_index(["pers_id", "moco", "nod", "RR", "shake", "still", "img_type"])
box_df = box_df[~box_df.index.duplicated(keep='first')]
box_df = box_df.reset_index()

#Create boxplot
for im_seq in box_df["img_type"].unique():
    print(im_seq)
    fig = box_subplot(box_df,wilcox_df, metrics = ["coent", "aes", "tg"], img_seq = im_seq, box_cols=[dblue,lblue])
    fig.savefig(out_dir+"box"+im_seq+".png", bbox_inches = 'tight')
#Create correlation plot
cor_df = pd.read_csv(data_dir + "/Merge_Output/"+"Metric_and_Observer.csv")
for im_seq in cor_df["img_type"].unique():
    fig = correlation_subplot(df = cor_df,metrics =  ["coent", "aes", "tg"],
                              img_seq =  im_seq, title_names = title_names, 
                              ylabel_names = ylabel_names, markerpalette=palette ) 

    #savefigure
    fig.savefig(out_dir+"hc_cor_"+im_seq+".png", bbox_inches = 'tight')



#Create clinical plot
data_dir = "/Users/simon/Documents/GitHub/Msc_Thesis/HC_Analysis/Files_ig/Merge_Output/"
clinical_dir = "/Users/simon/Documents/GitHub/Msc_Thesis/Clinical_Metrics/"
out_dir = "/Users/simon/Documents/GitHub/Msc_Thesis/Figures/"

#Load Data
clin_res = pd.read_csv(clinical_dir + "Metric_and_Observer.csv")
hc_res = pd.read_csv(data_dir + "Metric_and_Observer.csv")
hc_res["img_type"] = hc_res["img_type"].str[:-1]
clin_res["tg"] = clin_res["tgrad"]

palette = [(47, 122, 154),(231,47,149),(126,25,82)]
linecol = (83, 201, 250)

for img_seq in clin_res["img_type"].unique():
    fig = clinical_cor_plot(clin_res, hc_res, img_seq, palette, linecol, ylabel_names, title_names)
    fig.savefig(out_dir+"clin_cor_"+img_seq+".png", bbox_inches = 'tight')