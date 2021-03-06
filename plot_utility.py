import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches
import datetime
import seaborn as sns
sns.set()

import glob
import os
from scipy import stats
from scipy.stats import wilcoxon as cox


dblue = (47, 122, 154)
lblue = (83, 201, 250)


#Clinical plot
def plot_clin_data(clin_df, metric, i, ax, palette):
    #Scatter plot:
    sns.scatterplot(data = clin_df, x = "w_avg", y = metric, ax = ax[i],
                   hue = "pers_id", palette = palette, legend = None)
def plot_hc_data(hc_df, metric, i , ax, palette, linecol):
    #Scatterplot
    sns.scatterplot(data = hc_df, x = "w_avg", y = metric, ax = ax[i],
                   color = "gray", alpha = 0.6)
    #Line plot
    sns.regplot(data = hc_df, x = "w_avg", y = metric, ax = ax[i],
               fit_reg = True, ci = False,
               line_kws={"color": linecol},
               scatter_kws={'alpha':0.0})
    
    
def clinical_cor_plot(clin_df, hc_df, img_type, palette, linecolor, ylabels, titlelabels, title = None, main_title = None):
    #Check colormaps
    #Change Maker color to floats
    for i, col in enumerate(palette):
        if any(val>1 for val in col):
            palette[i] = tuple(val/255 for val in col)
    #if any(val>1 for val in markercolor):
        #markercolor = tuple(val/255 for val in markercolor)
    #Change Line color to floats
    if any(val>1 for val in linecolor):
        linecolor = tuple(val/255 for val in linecolor)
    #Subset Data
    rclin_df = clin_df.loc[clin_df["img_type"] == img_type].copy()
    rhc_df = hc_df.loc[hc_df["img_type"] == img_type].copy()
    
    fig, ax = plt.subplots(1, 3 ,figsize = (16,4))
    
    for i, metric in enumerate(["coent", "aes", "tg"]):
        plot_hc_data(rhc_df, metric, i, ax, palette, linecolor)
        plot_clin_data(rclin_df, metric, i, ax, palette)
        ax[i].set_xlabel("Observer Score (arb'U)")
        ax[i].set_ylabel(ylabels[metric])
        ax[i].set_title(titlelabels[metric])
    #Legend Settings
    legend_elements = [ Line2D([0], [0], color=linecolor, lw=4, label='Fitted Line'),
                        Line2D([0], [0], marker='o', color='gray', label='Healthy Control Data',lw=0),
                        Line2D([0], [0], marker='o', color=palette[0], label='MoCo_001',lw=0),
                        Line2D([0], [0], marker='o', color=palette[1], label='MoCo_002',lw=0),
                        Line2D([0], [0], marker='o', color=palette[2], label='MoCo_003',lw=0),]
    #Add Legend
    ax[1].legend(handles = legend_elements,
                 loc='upper center', bbox_to_anchor=(0.5, -0.3),
                 fancybox=True, shadow=True, ncol=len(legend_elements))

    #Super title
    if title is None:
        plt.suptitle("Clinical Metric Evaluation for " + img_type, y = 1.1, fontsize = 15)
    else: plt.suptitle(title, y = 1.1, fontsize = 15)
    return fig

#HC CORR PLOT
def string_pval(pval):
    """
    Given a pvalue format a
    string with relavent info
    """
    if pval <=0.001:
        spval = str(pval)+"**"
    elif pval <=0.05:
        spval = str(pval)+"*"
    elif np.round(pval,4) == 0.0:
        return "<0.0006"
    else: spval = str(pval)
    if np.round(pval,4) == 0.0:
        return "<0.0006"
    return spval

def correlation_subplot(df, metrics, img_seq,
                        nrow = 1, ncol = 3, figure_size = (16,4),
                        title_names = None, ylabel_names = None,
                        linecolor = (83, 201, 250), 
                        markerpalette = [], 
                        alpha = 0.8, 
                        fitreg = True, confint = False,
                        title = None, title_size = 15, subtitle_size=10, 
                        main_title = None):
    """
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing relevant data
        such as the values to plot and identifier 
        variables, eg image type or personal id
    metrics : iterable
        list or array type containing strings of the 
        metrics to plot
    img_seq : str
        Image sequence to plot x,y data from
        e.g. T1_MPR_
    nrow : int
        number of rows in the figure
    ncol : int 
        number of columns in the figure
    figure_size : tuple
        size of the figure
    title_names : dictionary
        dictionary with metrics as keys 
        and appropriate title as values
    ylabel_names : dictionary
        dictionary with metrics as keys 
        and appropriate ylabels as values
    linecolor : tuple
        rgb color tuple for fitted line
    markerpalette : list
        list of rgb color tuples for scatter markers
    alpha : float
        opacity alpha, range [0,1]
    fitreg : bool
        Whether or not to fit a linear line to data
    confint : bool
        Whether or not to add confidence interval 
        to fitted line
    title : str
        Super-title for the figure
    title_size : float
        Fontsize of the super-title
    subtitle_size : float
        size of the titles for the subplots
    Returns
    --------
    fig : <class 'matplotlib.figure.Figure'>
        Scatterplot Figure for each metric
    """
    #Create figure
    fig, ax = plt.subplots(nrow, ncol, figsize = figure_size, 
                           sharey = False, sharex = False)
    #Check colormaps
    #Change Maker color to floats
    for i, col in enumerate(markerpalette):
        if any(val>1 for val in col):
            markerpalette[i] = tuple(val/255 for val in col)
    #if any(val>1 for val in markercolor):
        #markercolor = tuple(val/255 for val in markercolor)
    #Change Line color to floats
    if any(val>1 for val in linecolor):
        linecolor = tuple(val/255 for val in linecolor)
    
    #Set Palette


    #Subset for relevant dataframe
    rel_df = df.loc[df["img_type"] == img_seq]
    rel_df["col"] = rel_df["nod"]+2*rel_df["shake"]
    
    #Legend Settings
    legend_elements = [ Line2D([0], [0], color=linecolor, lw=4, label='Fitted Line'),
                        Line2D([0], [0], marker='o', color='k', label='MoCo off',lw=0),
                        Line2D([0], [0], marker='s', color='k', label='MoCo on',lw=0),
                        Line2D([0], [0], marker='o', color=markerpalette[0], label='Still',lw=0),
                        Line2D([0], [0], marker='o', color=markerpalette[1], label='Nod',lw=0),
                        Line2D([0], [0], marker='o', color=markerpalette[2], label='Shake',lw=0),]
    #Remove a color and legend point
    #if the sequence is not MPRAGE
    if "mpr" not in img_seq.lower():
        legend_elements = legend_elements[:-1]
        markerpalette = markerpalette[:-1]
    #For each metric create a correlation plot
    for i, metric in enumerate(metrics):
        #Spearmann correlation
        spearmann_corr, pval = np.round(stats.spearmanr(rel_df["w_avg"],rel_df[metric]),4)
        #Add significance stars
        #to pvalue
        #spval = string_pval(pval)
        spval = is_signf(pval)
        if spval == "NS":
            spval = ""
        #annotate spearmann corr
        ax[i].annotate("Spearman Correlation: "+str(spearmann_corr)+spval, 
                       xy = (0.2,-0.3), xycoords = "axes fraction")
        #Scatterplot
        sns.scatterplot(data = rel_df, x = "w_avg", y = metric, ax = ax[i],
                    style = "moco",
                    markers = ["o", "s"],
                    style_order = [0,1],
                    hue = "col",
                    hue_order = [i for i in range(len(markerpalette))],
                    palette = markerpalette, 
                    alpha = alpha, legend = None)
        #Line plot
        sns.regplot(data = rel_df, x = "w_avg", y = metric, ax = ax[i], fit_reg = fitreg,
               line_kws={"color": linecolor}, ci = confint,
               scatter_kws={'alpha':0.0},)

        #Change title and labels
        ax[i].set_title(title_names[metric], fontsize = title_size)
        ax[i].set_ylabel(ylabel_names[metric]+" (arb'U)", fontsize = title_size)
        ax[i].set_xlabel("Observer Scores (arb'U)", fontsize = title_size)
    
    #Add Legend
    ax[1].legend(handles = legend_elements,
                 loc='upper center', bbox_to_anchor=(0.5, -0.3),
                 fancybox=True, shadow=True, ncol=len(legend_elements))

    #Super title
    if title is None:
        plt.suptitle("Metric Evaluation for " + img_seq[:-1], y = 1.1, fontsize = title_size)
    else: plt.suptitle(title, y = 1.1, fontsize = title_size)
    if main_title is not None:
        plt.suptitle("Clinical Metric Evaluation for " + main_title[img_seq[:-1]], y = 1.1, fontsize = 15)
    #Return the figure
    return fig

#HC BOXPLOT
def pivot_df(df,nod):
    rel_df = df.copy()
    rel_df = rel_df.loc[rel_df["nod"] == nod]
    rel_df = rel_df.drop(["nod","moco"], axis = 1)
    rel_df = rel_df.pivot("pers_id", "x")
    return rel_df

def add_lines(df, ax):
    #For nodding:
    rel_df = pivot_df(df, nod= 1)
    npdf = np.array(rel_df.reset_index(drop = True))
    for row in npdf:
        sns.lineplot(x = [2,3], y = row, ax = ax, color = "k",alpha = 0.3)
        
    #For still:
    rel_df = pivot_df(df, nod= 0)
    npdf = np.array(rel_df.reset_index(drop = True))
    for row in npdf:
        sns.lineplot(x = [0,1], y = row, ax = ax, color = "k",alpha = 0.3)

def change_box_colors(ax, cols):
    for axis in ax:
    #whisker color
        for i in range(6):
            axis.lines[i].set_color(cols[0])
            axis.lines[i+5].set_color(cols[1])
            
            axis.lines[i+11].set_color(cols[0])
            axis.lines[i+17].set_color(cols[1])
    #Box color
        for i in range(len(axis.get_xticks())):
        # Select which box you want to change    
            mybox = axis.artists[i]
            # Change the appearance of that box
            mybox.set_facecolor("none")
            mybox.set_edgecolor(cols[i%2])
            
            mybox = axis.artists[i+2]
            # Change the appearance of that box
            mybox.set_facecolor("none")
            mybox.set_edgecolor(cols[i%2])

def wilcox(metric_df):
    #pvalue for still
    npdf = np.array(pivot_df(metric_df, 0).reset_index(drop = True))
    npdf[:,0]
    stat, stillpval = cox(npdf[:,0], npdf[:,1], alternative = "two-sided")
    
    #pvalue for nodding
    npdf = np.array(pivot_df(metric_df, 1).reset_index(drop = True))
    npdf[:,0]
    stat, nodpval = cox(npdf[:,0], npdf[:,1], alternative = "two-sided")
    
    return stillpval, nodpval

def is_signf(pval):
    if pval <=0.001:
        return "**"
    elif pval<=0.05:
        return "*"
    else: return "NS"

def subset_wilcox_df(df, img_seq, metric):
    rel_df = df.copy()
    rel_df = rel_df.loc[rel_df["img_type"] == img_seq]
    rel_df = rel_df.loc[rel_df["metric"] == metric]
    rel_df = rel_df.loc[rel_df["RR"] == 0]
    print(rel_df)
    nod_pvalue = rel_df.loc[rel_df["motion"] == "nod", "pvalue_cor"].reset_index(drop = True)[0]
    still_pvalue = rel_df.loc[rel_df["motion"] == "still", "pvalue_cor"].reset_index(drop = True)[0]
    print(nod_pvalue, still_pvalue)
    return still_pvalue , nod_pvalue

def box_subplot(df, wilcox_df, metrics, img_seq, linewidth = 3, box_cols = [], main_title = None):

    #Colors to use
    cols = []
    #Check colormaps
    for col in box_cols:
        #Change Maker color to floats
        if any(val>1 for val in col):
            #Change to float values
            col = tuple(val/255 for val in col)
            #Append to cols list
            cols.append(col)

    fig, ax = plt.subplots(3,1, figsize = (8,16))

    #Subset dataframe
    #Without shake and without Reacquisition
    rel_df = df.copy()
    rel_df = rel_df.loc[rel_df["img_type"] == img_seq]
    rel_df = rel_df.loc[rel_df["RR"] == 0]
    rel_df = rel_df.loc[rel_df["shake"] == 0]

    print("MAKING PLOT")
    print("---------------------------------------------------")
    print("---------------------------------------------------")
    print("---------------------------------------------------")
    print("---------------------------------------------------")
    for i, metric in enumerate(metrics):
        #make boxplot for each metric
        metric_df = rel_df[["pers_id", "moco", "nod"]+[metric]].copy()

        metric_df["x"] = metric_df["moco"]+2*metric_df["nod"]

        #create boxplot
        sns.boxplot(data = metric_df, x = "x", y = metric, ax = ax[i], linewidth = linewidth)
        #Print Adding lines
        add_lines(metric_df, ax[i])
        print()
        print("---------------------------------------------------")
        print(i)
        print(metric)
        #Retrieve wilcoxon rank pavlues
        still_pvalue, nod_pvalue = subset_wilcox_df(wilcox_df, img_seq, metric)
        print(still_pvalue, nod_pvalue)
        #Convert to string format
        still_pvalue, nod_pvalue = is_signf(still_pvalue), is_signf(nod_pvalue)
        print(still_pvalue, nod_pvalue)
        print("---------------------------------------------------")
        print()
        #Add stars and significance level
        #still
        y, h, col = metric_df[metric].max() + 0.1, 0.05*(metric_df[metric].max()-metric_df[metric].min()), 'k'
        x1,x2 = 0,1
        ax[i].plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, c=col)
        ax[i].text((x1+x2)*.5, y+h, still_pvalue, ha='center', va='bottom', color=col, fontsize = 15)
        #nodding
        y, h, col = metric_df[metric].max() + 0.1, 0.05*(metric_df[metric].max()-metric_df[metric].min()), 'k'
        x1,x2 = 0+2,1+2
        ax[i].plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, c=col)
        ax[i].text((x1+x2)*.5, y+h, nod_pvalue, ha='center', va='bottom', color=col, fontsize = 15)
        
        

    #Set xticks
    for i in range(3):
        ax[i].set_xticks([0.5, 2.5])
        ax[i].set_xticklabels(["Still", "Nod"],fontsize=16)
        ax[i].set_xlabel("")

    #Titles
    ax[0].set_title("Co-occurence Entropy", fontsize = 16)
    ax[1].set_title("Average Edge Strength", fontsize = 16)
    ax[2].set_title("TennenGrad", fontsize = 16)
    #Labels
    ax[0].set_ylabel("CoEnt(arb'U)", fontsize = 16)
    ax[1].set_ylabel("AES(arb'U)", fontsize = 16)
    ax[2].set_ylabel("TG(arb'U)", fontsize = 16)

    #Change colors of the boxes
    change_box_colors(ax, cols)


    #Legend Settings
    legend_elements = [Line2D([0], [0], marker='s', color=cols[0], label='MoCo off',lw=0),
                    Line2D([0], [0], marker='s', color=cols[1], label='MoCo on' ,lw=0),]
    #Add legend
    ax[2].legend(handles = legend_elements,
                    loc='upper center',bbox_to_anchor=(0.5, -0.1),
                    fancybox=True, shadow=True, ncol=len(legend_elements))
    #Add super title
    plt.suptitle("Metric boxplot " + img_seq[:-1], fontsize = 24, y = 0.95)

    if main_title is not None:
        try:
            plt.suptitle("Metric boxplot " + main_title[img_seq[:-1]], fontsize = 24, y = 0.95)
        except:
            print("OK hello")
    return fig


def correlation_plot(df,img_seq, title,
                         x, y,
                         save_dir ="", file_name = "",
                         x_label = " ", y_label = " ",
                         x_ticks = True, y_ticks = True,
                         marker_color = (47, 122, 154),
                         line_color  = (83, 201, 250),
                         alpha = 0.7, fit_line = True, conf_int = True, legend_label = ["Fitted Line", "Data"], ax = None):
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
        plotted figure.
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
    
    if ax is not None:
        sns.regplot(x,y, fit_reg = fit_line, ci = conf_int, 
            scatter_kws={'alpha':alpha, "color" : marker_color},
            line_kws={"color": line_color}, ax = ax)
    else:
        #Scatter plot (x,y)
        sns.regplot(x,y, fit_reg = fit_line, ci = conf_int, 
                    scatter_kws={'alpha':alpha, "color" : marker_color},
                    line_kws={"color": line_color})
    
    #Add title and labels
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend(loc = "upper right", labels = legend_label)


    #Check ticks, and change acordingly
    #If ticks values are provided they are used
    #otherwise default ticks are used

    #x-ticks
    #Check if list or array is passed
    if isinstance(x_ticks,(list,np.ndarray)):
        #Replace x-ticks with the provided ticks
        plt.xticks(x_ticks[0], x_ticks[1])
    #If bool "false" is given to ticks remove ticks
    elif not x_ticks:
        plt.xticks([])
    #y-ticks
    #Check if list or array is passed
    if isinstance(y_ticks,(list,np.ndarray)):
        #Replace y-ticks with the provided ticks
        plt.xticks(y_ticks[0], y_ticks[1])
    #If bool "false" is given to ticks remove ticks
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
    #Fraction to put the annotation
    #if both zero it is a bottom left,
    #if both 1 top right
    #Values in range [0,1]
    x_frac = 0
    y_frac = 0.9
    fig.axes[0].annotate("Spearman Correlation: "+str(spearmann_corr)+"\n"+
                         "p-value:                          "+spval, xy = (x_frac,y_frac), xycoords = "axes fraction")
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



def starbox_plot(df, img_seq, id_var, split_var, metric, plot_title, nod,
                 x_label = "", y_label = "", x_ticks = [],
                 save_dir = None, file_name = None, wilcox_file = None, wilcox_df = None, RR = 0, shake = 0, 
                 id_color = "k", id_alpha = 0.7, linewidth = 3, box_cols = [dblue, lblue], legend = False):
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
    id_var : str
        Column name for identifying which the observations
        belong to
    split_var : str
        Variable to split by. The different values
        of split_var corresponds to each box in the boxplot.
        eg if split_var has 2 levels, 2 boxes are produced
    metric : str
        which metric to use/plot along y-axis, eg "coent" or "aes"
    plot_title : str
        title of the plot
    nod : bool
        0 is for still images, 1 is for nodding images
    x_label : str
        x-axis label
    y_label : str
        y-axis label
    x_ticks : bool or array
        True/False uses default ticks values
        or turns off ticks.
        Array of type [locations, values] 
        to use custom ticks
    save_dir : str
        Where to save the figure
    file_name : str
        What to call the file
    wilcox_file : str
        Filepath for a csv file containing wilcoxon rank
        test statistics and pvalues for each metric,
        nodding/still and for the metric used.
        wilcox_file or wilcox_df should be specified
    wilcox_df : pd.DataFrame
        DataFrame containing wilcoxon rank
        test statistics and pvalues for each metric,
        nodding/still and for the metric used.
        wilcox_file or wilcox_df should be specified
    RR : bool
        Reacquisition
    shake : bool
        Shaking
    id_color : str
        Color for the connecting lines between two boxplots
        Default is black
    id_alpha : float
        Alpha level opacity for the connecting lines
    linewidth : float
        Linewidth of the boxplot
    box_cols : list
        List containing rbg values to use to the plots.
        Two values should be given 
    line_color : tuple
        rgb color tuple, can be in [0,1] or [0,255]
    legend : bool
        If true adds a legend to the plot
    
    Returns
    -------
    fig : matplotlib.figure.Figure
        plotted figure.
    '''   

    #Input verification
    if wilcox_df is None and wilcox_file is None:
        print("Error, both wilcox file path and dataframe is None")
        print("Need a wilcox dataframe or file")
    if (save_dir is None) ^ (file_name is None):
        print("Error, save_dir and save_file should either both be None or specified")
    cols = []
    #Check colormaps
    for col in box_cols:
        #Change Maker color to floats
        if any(val>1 for val in col):
            #Change to float values
            col = tuple(val/255 for val in col)
            #Append to cols list
            cols.append(col)
    
    #Load data
    if wilcox_file is not None:
        wilcox_df = pd.read_csv(wilcox_file)
    
    #Subset to relevant data
    rel_df = df.copy()
    rel_df["img_type"] = rel_df["img_type"]#.str[:-1]
    rel_df = rel_df.loc[rel_df["nod"] == nod]
    rel_df = rel_df.loc[rel_df["img_type"] == img_seq]
    rel_df = rel_df.loc[rel_df["shake"] == shake]
    rel_df = rel_df.loc[rel_df["RR"] == RR]
    """
    #Drop redundant columns
    cox_df = rel_df.copy()
    cox_df = cox_df.drop(["nod", "still", "RR", "shake", "img_type"], axis = 1)

    #Subset for only relevant columnds
    cox_df = cox_df[["pers_id", "moco", metric]]

    cox_df = cox_df.drop_duplicates()
    cox_df = cox_df.set_index(['pers_id', 'moco'])[metric].unstack().reset_index()

    #Calculate the Wilcoxon test statistic and pvalue
    stat, pval =  cox( x = cox_df[0] , y = cox_df[1] )
    print( cox( x = cox_df[0] , y = cox_df[1] ))
    """

    #Drop redundant columns
    rel_df = rel_df[[id_var, split_var, metric]]
    
    #Subset to relevant wilcox data
    rel_cox = wilcox_df.loc[wilcox_df["metric"] == metric]
    rel_cox = rel_cox.loc[rel_cox["img_type"] == img_seq]
    rel_cox = rel_cox.loc[rel_cox["nod"] == nod]
    

    #Check if the pvalue is significant
    signf = False
    if rel_cox.shape[0]>0:
        pval = round(list(rel_cox["pval"])[0],5)
        #Add significance stars
        if pval <=0.001:
            signf = True
            str_pval = str(pval)+"**"
        elif pval <=0.05:
            signf = True
            str_pval = str(pval)+"*"
        else: str_pval = str(pval)


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
    for i in range(6):
        ax.lines[i].set_color(cols[0])
        ax.lines[i+5].set_color(cols[1])


    #if significant add stars and stripes
    if signf:
        #Add stars and significance level
        y, h, col = rel_df[metric].max() + 0.1, 0.1, 'k'
        x1,x2 = 0,1
        plt.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, c=col)
        plt.text((x1+x2)*.5, y+h, str_pval, ha='center', va='bottom', color=col)
    #Add idlines
    plot_array = np.asarray( rel_df.pivot(id_var, columns =split_var) )
    for val in plot_array:
        plt.plot(val, c = id_color, alpha = id_alpha)
    if nod == 1:
        nod_title = "nodding"
    else: nod_title = "still"
    #Set axis labels
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(plot_title +" "+img_seq+" "+metric+" "+nod_title )

    ax.set_xticklabels(x_ticks)

    moco_off = mpatches.Patch(color=cols[0], label="MoCo off")
    moco_on = mpatches.Patch(color=cols[1], label="MoCo on")
    if legend:
        plt.legend(handles=[moco_on,moco_off])


    #Save figure
    if save_dir is not None:
        if not os.path.exists(save_dir):
            print("Folder did not exist")
            print("Creating folder")
            os.makedirs(save_dir)
        #Current date, eg oct_18
        dat = datetime.datetime.now()
        dat = dat.strftime("%b")+"_"+dat.strftime("%d")
        #Save figure to the savedir
        fig.savefig(save_dir + file_name+dat+".png")
    return fig