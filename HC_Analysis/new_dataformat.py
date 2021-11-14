import numpy as np
import pandas as pd
import glob
import os


def format_df_columns(df_orig):
    #Create a copy of the DataFrame
    df = df_orig.copy()
    #Format columns
    df["moco"] = 0
    df["nod"] = 0
    df["RR"] = 0
    df["shake"] = 0
    df["still"] = 0
    
    #Replace with apropriate values
    #Set moco to 1 if moco is on
    df.loc[ df["type"].str.lower().str.contains("moco_on") , "moco"] = 1
    #If shake set to 1
    df.loc[ df["type"].str.lower().str.contains("shake") , "shake"] = 1
    #Set nod to 1 if nodding
    df.loc[ df["type"].str.lower().str.contains("nod") , "nod"] = 1
    #Set nod to 1 if still
    df.loc[ df["type"].str.lower().str.contains("still") , "still"] = 1
    #Set RR to 1 if reacquistition
    df.loc[ df["type"].str.lower().str.contains("rr") , "RR"] = 1
    
    #Drop redundant columns
    df = df.drop(["type"], axis = 1)
    
    #Return the formatted dataframe
    return df


####               #####
#### Metric Format #####
####               #####
def format_single_metric_file(file, to_merge, pers_id, img_seq, save_file, save):
    #Load data
    df = pd.read_csv(file, skiprows = [0],sep = " ", names = ["type", "tg", "coent", "aes", "aes_lap", "aes_pst"])
    #Add id column
    df["pers_id"] = pers_id
    #Format columns
    df = format_df_columns(df)
    
    #Add image type
    df["img_type"] = img_seq
    
    if save:
        #Save dataframe
        df.to_csv(pers_id+save_file+".csv", index = False)
    
    #Merge dataframe with to_merge
    merged = pd.concat([to_merge, df])
    
    #Return merged dataframe
    return merged

def format_all_metric_files(file_dir, reference_date, reference_name, save_subfiles, out_dir, save_file):
    #Check if the out_dir exists otherwise create it
    if not os.path.exists(out_dir):
            print("Directory created:")
            print("  ", out_dir)
            os.makedirs(out_dir)
    
    #Base dataframe to merge with
    base_metric = pd.DataFrame()
    
    #Folders for all the healthy controls
    hc_folders = glob.glob(file_dir+"*")
    
    #Format metric dataframe
    #For each healthy control 
    #in the folder of healthy control's
    for HC in hc_folders:
        #Name of patient, eg HC_01
        patient_id = os.path.basename(HC)
        patient_folder = glob.glob(HC+"/*")
        for file in patient_folder:
            if reference_date in file:
                #Image sequence eg T2_Flair_
                img_sequence = os.path.basename(file)[len(reference_name+reference_date):]
                print(patient_id, img_sequence)
                #print(file)
                print()
                
                base_metric = format_single_metric_file(file, base_metric, patient_id, 
                                                        img_sequence, save_file, save_subfiles)
        
    #Save dataframe
    base_metric.to_csv(out_dir + "All_metric.csv", index = False)
    print("File saved to: ")
    print(out_dir)
    print("+------------------------------------------------------------------+")
    print("|                                                                  |")
    print("|                     Metric Scores Merged                         |")
    print("|                                                                  |")
    print("+------------------------------------------------------------------+")
    
    return base_metric
    

####                 #####
#### Observer Format #####
####                 #####
def format_sigle_observer_file(file, to_merge, img_seq, save, out_dir, save_file):
    #Load data
    df = pd.read_csv(file, sep = " ", skiprows = [0], 
                names = ["type", "Bianca", "Martin", "Nitesh"])
    
    #Add weighted average:
    df["w_avg"] = (df[["Bianca", "Martin", "Nitesh"]]*(np.array([1,1,2])*(1/4))).sum(axis =1)
    
    #Drop individual scores
    df = df.drop(["Bianca", "Martin", "Nitesh"], axis = 1)
    
    #Ad id columns
    df["pers_id"] = df['type'].str[3:8]
    
    #Add image type
    df["img_type"] = img_seq

    #Format columns
    df = format_df_columns(df)
    
    if save:
        #Save dataframe
        df.to_csv(out_dir+img_seq+save_file+".csv", index = False)
    
    #Merge dataframe with to_merge
    merged = pd.concat([to_merge, df])
    
    #Return merged dataframe
    return merged


def format_all_observer_files(file_dir, save_subfiles, out_dir, save_file):
    #Check if the out_dir exists otherwise create it
    if not os.path.exists(out_dir):
            print("Directory created:")
            print("  ", out_dir)
            os.makedirs(out_dir)
            
    #Base dataframe to merge with
    base_observer = pd.DataFrame()
    
    #Files
    obs_files = glob.glob(file_dir+"*")

    for file in obs_files:
        im_sequence = os.path.basename(file)[:-9]
        print(im_sequence)
        #print(file)
        print()
        #Format the data
        base_observer = format_sigle_observer_file(file, base_observer, 
                                                   im_sequence, save_subfiles, 
                                                   out_dir, save_file)
    
    #Save dataframe
    base_observer.to_csv(out_dir + "All_observer.csv", index = False)
    print("File saved to: ")
    print(out_dir)
    print("+------------------------------------------------------------------+")
    print("|                                                                  |")
    print("|                     Observer Scores Merged                       |")
    print("|                                                                  |")
    print("+------------------------------------------------------------------+")
    
    #Return dataframe
    return base_observer

####                                  #####
#### Merge metric and observer Format #####
####                                  #####
def merge_metric_and_observers(metric_file, observer_file, out_dir):
    #Check if the output directory exists otherwise create it
    if not os.path.exists(out_dir):
            print("Directory created:")
            print("  ", out_dir)
            os.makedirs(out_dir)

    #Load Data
    obs_df = pd.read_csv(observer_file)
    metric_df = pd.read_csv(metric_file)
    ##########
    ##########
    ##########
    metric_df["img_type"] = metric_df["img_type"].str[:-4]  #If the imgtype has bad extension
    ##########
    ##########
    ##########
    print(metric_df.head())
    #Subset to the appropriate image sequences
    sequences = obs_df["img_type"].unique()
    metric_df = metric_df.loc[metric_df["img_type"].isin(sequences)]
    print(metric_df.head())
    #Set joint index
    metric_df = metric_df.set_index(["pers_id", "img_type", "moco", "still", "nod", "shake", "RR"])
    obs_df = obs_df.set_index(["pers_id", "img_type", "moco", "still", "nod", "shake", "RR"])
    print(metric_df.head())
    #Join dataframes
    joined_df =  metric_df.join(obs_df).reset_index()
    #Remove nans
    joined_df = joined_df.dropna()
    #Save the Dataframe
    joined_df.to_csv(out_dir+"Metric_and_Observer.csv", index = False)
    print("File saved to: ")
    print(out_dir)
    print("+------------------------------------------------------------------+")
    print("|                                                                  |")
    print("|                 Observer and Metrics Merged                      |")
    print("|                                                                  |")
    print("+------------------------------------------------------------------+")

    #Return dataframe
    return joined_df
