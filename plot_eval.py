import pandas as pd
import os
import glob
from plot_utility import correlation_plot, starbox_plot
import matplotlib.pyplot as plt
data_dir = "C:/Users/simon/Documents/GitHub/Msc_Thesis/HC_Analysis/Files_ig"
print("LOADING DATA")
df = pd.read_csv(data_dir + "/observer_merged_metric.csv")



#cor = correlation_plot(df, img_seq= "T1_MPR_", title = "Plot Title", x = "w_avg", y = "coent", fit_line = True,
#                            x_label= "Observer Scores", y_label="CoEnt")


#print(type(cor))
#plt.show()



#for img_type in df["img_type"].unique():
#   cor = correlation_plot(df, img_seq= img_type, title = "Plot Title", x = "w_avg", y = "aes", fit_line = True,
#                          x_label= "Observer Scores", y_label="CoEnt")



print("LOADING COX DF")
cox_dir = "C:/Users/simon/Documents/GitHub/Msc_Thesis/HC_Analysis/"

cox_df = pd.read_csv(cox_dir + "wilcox_results.csv")


print("done")


##bp = starbox_plot(df, "T1_MPR", "pers_id", "moco", "aes", "plot titel", nod = 0, wilcox_df= cox_df)


#plt.show()


for img_type in df["img_type"].unique():
    for metric in ["coent", "aes"]:
        for nods in [0,1]:
            starbox_plot(df, img_type, "pers_id", "moco", metric, "", nod = nods, wilcox_df= cox_df)
            plt.show()