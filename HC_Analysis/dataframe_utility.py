import numpy as np
import pandas as pd

def format_dataframe_metric(file_path, metric_in, metric_out, file_reference, relevant_date):
    """
    Parameters
    ----------
    file_path : str
        Filepath containing metric evaluations 
        of a single subject
    metric_in : str
        Filepath for the metric files to load
    metric_out : str
        Output filepath where the dataframes should be stored
    file_reference : str
        Reference of how the file name is formatted,
        eg "Values_AES_CoEnt_10_06_"
    relevant_date : str
        Date of which the dataframes should be formatted around.
        For the lates data use the latest date, eg "10_06"
        
    Returns
    -------
    subject_DataFrame : pandas.DataFrame
        Data frame with columns such as
        ['aes', 'coent', 'moco', 'nod', 'RR', 
        'shake', 'still', 'pers_id', 'img_type']
    Saves the dataframe in csv format in metric-out-directory
    with subject id as filename
    """
    #Name of the subject
    subject_name = file_path[len(metric_in):][:5]
    #Name of the file
    #file_name = file_path[len(metric_in+subject_name)+1:]
    
    image_type = file_path[len(metric_in+subject_name+file_reference)+1:-4]
    
    #Check if the file is from the correct date
    correct_date = relevant_date in file_path
    #if wrong date stop
    if not correct_date: 
        #print("Wrong date")
        return None
    
    #Load the data
    file_df = pd.read_csv(file_path, sep = " ", names = ["type", "aes", "coent"],skiprows = [0],)
    
    #Format columns
    file_df["moco"] = 0
    file_df["nod"] = 0
    file_df["RR"] = 0
    file_df["shake"] = 0
    file_df["still"] = 0
    file_df["pers_id"] = subject_name
    
    
    #Replace with apropriate values
    #set moco to 1 if moco is on
    file_df.loc[ file_df["type"].str.lower().str.contains("moco_on") , "moco"] = 1
    #if shake set to 1
    file_df.loc[ file_df["type"].str.lower().str.contains("shake") , "shake"] = 1
    #set nod to 1 if nodding
    file_df.loc[ file_df["type"].str.lower().str.contains("nod") , "nod"] = 1
    #set nod to 1 if still
    file_df.loc[ file_df["type"].str.lower().str.contains("still") , "still"] = 1
    #set RR to 1 if reacquistition
    file_df.loc[ file_df["type"].str.lower().str.contains("rr") , "RR"] = 1

    
    #add image type
    file_df["img_type"] = image_type
    #Drop redundant column
    file_df = file_df.drop(["type"], axis = 1)
    
    subject_DataFrame = pd.read_csv(metric_out+subject_name+".csv")
    
    #merge the two dataframes
    subject_DataFrame = pd.concat([subject_DataFrame, file_df])
    
    #save the merged dataframe
    subject_DataFrame.to_csv(metric_out+subject_name+".csv", index = False)


def format_observer_dataframe(file, observer_in, observer_out):
    """
    Parameters
    ----------
    file_path : str
        Filepath containing observer scores 
        of a single subject
    observer_in : str
        Filepath for the observer scores file
    observer_out : str
        Filepath pointing to where
        the formatted dataframes should be saved to
    Returns
    -------
    file_df : pandas.DataFrame
        Data frame with columns such as
        ["w_avg", 'moco', 'nod', 'RR', 
        'shake', 'still', 'pers_id', 'img_type']
    Saves the dataframe in csv format in observer-out-directory
    with subject id as filename
    """
    #type of image
    image_type = file[len(observer_in):-9]
    
    #Laod file
    file_df = pd.read_csv(file, sep = " ", skiprows = [0], 
                          names = ["type", "Bianca", "Martin", "Nitesh"])
    
    #Add weighted average:
    file_df["w_avg"] = (file_df[["Bianca", "Martin", "Nitesh"]]*(np.array([1,1,2])*(1/4))).sum(axis =1)
    #Drop individual scores
    file_df = file_df.drop(["Bianca", "Martin", "Nitesh"], axis = 1)
    
    #Format columns
    file_df["nod"] = 0
    file_df["RR"]  = 0
    file_df["moco"]= 0
    file_df["pers_id"] = file_df['type'].str[3:8]
    file_df["shake"] = 0
    file_df["still"] = 0
    file_df["img_type"] = image_type
    
    #Replace with apropriate values
    #set moco to 1 if moco is on
    file_df.loc[ file_df["type"].str.lower().str.contains("moco_on") , "moco"] = 1
    #if shake set to 1
    file_df.loc[ file_df["type"].str.lower().str.contains("shake") , "shake"] = 1
    #set nod to 1 if nodding
    file_df.loc[ file_df["type"].str.lower().str.contains("nod") , "nod"] = 1
    #set nod to 1 if still
    file_df.loc[ file_df["type"].str.lower().str.contains("still") , "still"] = 1
    #set RR to 1 if reacquistition
    file_df.loc[ file_df["type"].str.lower().str.contains("rr") , "RR"] = 1
    
    #Drop type
    file_df = file_df.drop(["type"], axis = 1)
    

    #Save dataframe
    file_df.to_csv(observer_out+image_type+".csv", index = False)
    
