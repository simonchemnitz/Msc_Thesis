import pandas as pd
import os
import glob
from plot_utility import correlation_plot
import matplotlib.pyplot as plt

data_dir = "C:/Users/simon/Documents/GitHub/Msc_Thesis/HC_Analysis/Files_ig"

df = pd.read_csv(data_dir + "/observer_merged_metric.csv")



cor = correlation_plot(df, img_seq= "T1_MPR_", title = "Plot Title", x = "w_avg", y = "coent", fit_line = True,
                            x_label= "Observer Scores", y_label="CoEnt")


print(type(cor))
plt.show()



for img_type in df["img_type"].unique():
    cor = correlation_plot(df, img_seq= img_type, title = "Plot Title", x = "w_avg", y = "aes", fit_line = True,
                            x_label= "Observer Scores", y_label="CoEnt")