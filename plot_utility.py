import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
sns.set()


import glob
import os
from scipy import stats

from HC_Analysis import wilcox

dblue = (47, 122, 154)
lblue = (83, 201, 250)


def correlation_plot(df,img_seq, title,
                         x, y,
                         save_dir ="", file_name = "",
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
    save_dir : str
        Where to save the figure
    file_name : str
        What to call the file
    x : str
        column string for the x-axis data
    y : str
        column string for the y-axis data
    x_label : str
        x-axis label
    y_label : str
        y-axis label
    x_ticks : bool or array
        True/False uses default ticks values
        or turns off ticks.
        Array of type [locations, values] 
        to use custom ticks
    y_ticks : bool or array
        True/False uses default ticks values
        or turns off ticks.
        Array of type [locations, values] 
        to use custom ticks
    marker_color : tuple
        rgb color tuple, can be in [0,1] or [0,255]
    line_color : tuple
        rgb color tuple, can be in [0,1] or [0,255]
    alpha : float
        alpha opacity for plot markers
    fit_line : bool
        Whether or not to fit regression line.
    conf_int : bool
        Whether or not to add confidence interval to reg line.
    
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
    #Check ticks, and change acordingly
    #x-Ticks
    if isinstance(x_ticks,(list,np.ndarray)):
        plt.xticks(x_ticks[0], x_ticks[1])
    elif not x_ticks:
        plt.xticks([])
    #y-Ticks
    if isinstance(y_ticks,(list,np.ndarray)):
        plt.xticks(y_ticks[0], y_ticks[1])
    elif not y_ticks:
        plt.xticks([])
    
    
    #Spearman correlation
    spearmann_corr, pval = np.round(stats.spearmanr(x,y),4)
    #Add significance stars
    if pval <=0.05:
        spval = str(pval)+"*"
    elif pval <=0.001:
        spval = str(pval)+"**"
    else: spval = str(pval)
        

    #Annotate correlation
    x_max = np.max( fig.axes[0].get_xlim() )
    x_min = np.min( fig.axes[0].get_xlim() )
    y_max = np.max( fig.axes[0].get_ylim() )
    y_min = np.min( fig.axes[0].get_ylim() )
    fig.axes[0].annotate("Spearman Correlation: "+str(spearmann_corr)+"\n"+
                         "p-value:                          "+spval, xy = (0,0.9), xycoords = "axes fraction")
    #Change xlimits to avoid clipping of points
    plt.xlim(left = np.min(fig.axes[0].get_xlim())-0.1, right = x_max+0.1 )
    

    #Save the figure:
    if len(save_dir)>0:
        if not os.path.exists(save_dir):
            print("Folder did not exist")
            print("Creating folder")
            os.makedirs(save_dir)
        #Current date, eg oct_18
        dat = datetime.datetime.now()
        dat = dat.strftime("%b")+"_"+dat.strftime("%d")
        #Save figure to the savedir
        fig.savefig(save_dir + file_name+dat+".png")

    #Return the figure
    return fig





def starbox_plot(df, img_type, id_var, split_var, metric, plot_title, nod,
                 x_label, y_label, bp_kwargs = None, palette = None,
                 save_dir = "", file_name = "", wilcox_file = "", wilcox_df = "", RR = 0, shake = 0, 
                 id_color = "k", id_alpha = 0.7, linewidth = 3, box_cols = [dblue, lblue]):
    cols = []
    #Check colormaps
    for col in box_cols:
        #Change Maker color to floats
        if any(val>1 for val in col):
            #Change to float values
            col = tuple(val/255 for val in col)
            #Append to cols list
            cols.append(col)
    
    
    #Subset to relevant data
    rel_df = df.copy()
    rel_df = rel_df.loc[rel_df["nod"] == nod]
    rel_df = rel_df.loc[rel_df["img_type"] == img_type]
    rel_df = rel_df.loc[rel_df["shake"] == shake]
    rel_df = rel_df.loc[rel_df["RR"] == RR]

    #Drop redundant columns
    rel_df = rel_df[[id_var, split_var, metric]]
    
    #Subset to relevant wilcox data
    rel_cox = wilcox_df.loc[wilcox_df["metric"] == metric]
    rel_cox = rel_cox.loc[rel_cox["img_type"] == img_type]
    rel_cox = rel_cox.loc[rel_cox["nod"] == nod]
    
    #Check if the pvalue is significant
    if rel_cox.shape[0]>0:
    pval = list(rel_cox["pval"])[0]
    signf = False
    #Add significance stars
    if pval <=0.05:
        signf = True
        spval = str(pval)+"*"
    elif pval <=0.001:
        signf = True
        spval = str(pval)+"**"
    else: 


    #Create the boxplot:
    fig = plt.figure()
    ax = sns.boxplot(data = rel_df, x = split_var, y = metric, linewidth = linewidth)

    #Change colors of boxes
    for i in range(len(ax.get_xticks())):
        # Select which box you want to change    
        mybox = ax.artists[i]
        # Change the appearance of that box
        mybox.set_facecolor("none")
        mybox.set_edgecolor(cols[i%2])
    #Change whiskers color
    for i in range(5):
        ax.lines[i].set_color(cols[0])
        ax.lines[i+5].set_color(cols[1])
        
    return None