import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

import glob
import os
from scipy import stats


def correlation_plot(df,img_seq, title,
                         x,       y,
                         x_label = " ", y_label = " ",
                         x_ticks = True, y_ticks = True,
                         marker_color = (47, 122, 154),
                         line_color  = (83, 201, 250),
                         alpha = 0.7, fit_line = False, conf_int = True):
    '''
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing relevant data
        such as the values to plot and identifier 
        variables, eg image type or personal id
    img_seq : str
        Image sequence to plot x,y data from
        e.g. T1_MPR_
    title : str
        title of the plot
    x : str
        column string for the x-axis data
    y : str
        column string for the y-axis data
    x_label : str
        x-axis label
    y_label : str
        y-axis label
    x_ticks : bool
        True 
    y_ticks : 
    marker_color : 
    line_color : 
    alpha : 
    fit_line : 
    conf_int : 
    
    Returns
    -------
    fig : matplotlib.figure.Figure
        plot figure.
    '''
    
    #Check if the sequence is valid
    if not img_seq in df["img_type"].unique():
        print("ERROR")
        print("Invalid sequence")
        print("Valid sequences:")
        print(df["img_type"].unique())
        return None
    
    #Relevant pd.DataFrame
    rel_df = df.loc[df["img_type"] == img_seq]
    
    #Check colormaps
    #Change Maker color to floats
    if any(val>1 for val in marker_color):
        marker_color = tuple(val/255 for val in marker_color)
    #Change Line color to floats
    if any(val>1 for val in line_color):
        line_color = tuple(val/255 for val in line_color)
    
    #Assign x-y values
    try:
        x = rel_df[x]
        y = rel_df[y]
    except:
        print("ERROR")
        print("KeyError")
        print("Possibles keys:")
        print(list(df))
        return None
    
    #Create figure
    fig = plt.figure()
    
    #Scatter plot (x,y)
    sns.regplot(x,y, fit_reg = fit_line, ci = conf_int, 
                scatter_kws={'alpha':alpha, "color" : marker_color},
                line_kws={"color": line_color})
    
    #Add title and labels
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(x_ticks)
    
    #Spearman correlation
    
    spearmann_corr, pval = np.round(stats.spearmanr(x,y),4)
    #Add significance stars
    if pval <=0.05:
        spval = str(pval)+"*"
    elif pval <=0.01:
        spval = str(pval)+"**"
    else: spval = str(pval)
        
        
    #Annotate correlation
    x_max = np.max( fig.axes[0].get_xlim() )
    y_max = np.max( fig.axes[0].get_ylim() )
    fig.axes[0].annotate("Spearman Correlation: "+str(spearmann_corr)+"\n"+
                     "p-value:                         "+spval, xy = (x_max, y_max))
    
    
    #Return the figure
    return fig