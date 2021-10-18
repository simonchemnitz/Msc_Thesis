import pandas as pd
import os
import glob
from plot_utility import correlation_plot


data_dir = "/users/simon/documents/GitHub/Msc_Thesis/HC_Analysis/Files_ig"

df = pd.read_csv(data_dir + "/observer_merged_metric.csv")



