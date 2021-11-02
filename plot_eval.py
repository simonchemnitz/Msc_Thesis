import pandas as pd
import os
import glob
from plot_utility import correlation_plot, starbox_plot, correlation_subplot
import matplotlib.pyplot as plt
data_dir = "/Users/simon/Documents/GitHub/Msc_Thesis/HC_Analysis/Files_ig"

df = pd.read_csv(data_dir + "/observer_merged_metric.csv")
print("Sequences: ")
print(df["img_type"].unique())

title_names = {"aes": "Average Edge Strength",
             "coent": "Co-Occurence Entropy",
             "tg": "TennenGrad"}
label_names = {"aes": "AES",
             "coent": "CoEnt",
             "tg": "TG"}

marker_color = (47, 122, 154)
line_color  = (83, 201, 250)

for im_seq in df["img_type"].unique():
    fig = correlation_subplot(df = df,metrics =  ["coent", "aes", "tg"],
                              img_seq =  im_seq, title_names = title_names, 
                              ylabel_names = label_names ) 
    fig.savefig("test"+im_seq+".png", bbox_inches = 'tight')



#for img_type in df["img_type"].unique():
#    for ax, metric in enumerate(["coent", "aes", "tg"]):
#        #fig, axes = plt.subplots(1, 3, sharex=True, figsize=(16,8))
#        cor = correlation_plot(df, img_seq= img_type, title = "Plot Title"+img_type, x = "w_avg", y = metric, fit_line = True,
#                          x_label= "Observer Scores", y_label=metric, ax = None)
#plt.show()



#cox_dir = "/Users/simon/Documents/GitHub/Msc_Thesis/HC_Analysis/"

#cox_df = pd.read_csv(cox_dir + "wilcox_results.csv")


#for img_type in df["img_type"].unique():
#    for metric in ["coent", "aes"]:
#        for nods in [0,1]:
#            starbox_plot(df, img_type, "pers_id", "moco", metric, "", nod = nods, wilcox_df= cox_df)
#            plt.show()


