#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import glob
import os

# Dir to folder containing all excel files
response_dir = "responses/"
files = glob.glob(response_dir+"*")

def weighted_scoring(df):
     '''
    Change scoring acording to scoring key
    ----------
    df : pandas.DataFrame
        Dataframe to change from answers index to score.
    Returns
    -------
    tmp_df : pandas.DataFrame
        pandas dataframe same as df but where entries of Qi 
        contains score of question i.
    '''
    #Create copy of the dataframe   
    tmp_df = pd.DataFrame.copy(df)
    #Two ways of scoring
    w0 = [0,1,2,3]
    w1 = [0,3,2,1]
    weights = [w0,w1]
    #Which weight to use
    #on which question.
    weight_val = [0,1,0,1,1,0,1,0,1,0,1,0,0,0,1,1,0,1,1,0]
    #Dictionairy containing weights, keys are the difference answers
    #Q1,...,Q20 and values are 0 or 1 based on wheter to used w0 or w1.
    weight_dict = {"Q"+str(i+1) : weights[weight_val[i]] for i in range(20)}
    

    #Column names, Q1,Q2,...,Q20
    answers = ["Q"+str(i) for i in range(1,21)]
    
    #For each column (question)
    #update entry to contain score
    for col in answers:
        #Weight to use
        w = weight_dict[col]
        #Update weight
        tmp_df[col] = np.array(w)[tmp_df[col]]

    #Return updated dataframe
    return tmp_df


def STAI_score(file_name, csv_file, weighted = False):
    '''
    Calculate the STAI score and append results to csv file
    containing all scores. If file does not exists it will create it
    Parameters
    ----------
    file_name : str
        file name of the excel file of survey results.
    csv_file : str
        file name of the csv file which keeps track of all relevant resulst.
    Returns
    -------
    new_state_csv : pandas dataframe
        pandas dataframe same as csv_file but appended the results from file_name.
        
        In addition it saves the pandas dataframe to the file csv_file.csv
    '''
    #    Column names for dataframes
    #Column names for State quiestionnaire
    #of the form Q1,Q2,Q3,...,Q20  
    answers = ["Q"+str(i) for i in range(1,21)]
    
    #Column names for Trait quiestionnaire
    #of the form Q1[1],Q1[2],Q1[3],...,Q1[20] 
    answers_trait = ["Q1[" +str(i) + "]" for i in range(1,21) ]
    
    #Column names to keep in the final csv file
    column_names = ["pers_id","comment", "date", "score", "time_to_complete(sec)"] +answers 
    
    # Check if state_csv_file exists otherwise create it
    if not os.path.isfile(csv_file):
        print("csv file does not exist")
        print("Creating file: " + csv_file)
        base_state_csv = pd.DataFrame(columns = column_names)
        base_state_csv.to_csv(csv_file, index = False)
    
    # Load dataframe containing all state scores
    csv = pd.read_csv(csv_file)
    
    # Load excel file file_name
    df =  pd.read_excel(file_name)
    
    surv_dict = {"434315" : "Trait",
            "443767" : "Home_State",
            "238699" : "After_Real_MR",
            "318579" : "Before_Real_MR",
            "411894" : "After_Mock_MR",
            "727961" : "Before_Mock_MR"}
    com = "Trait"
    for key in surv_dict:
        if key in file_name:
            com = surv_dict[key]
    
    # Correction of trait columns
    # originally they are named Q1[1],Q1[2],Q1[3],...,Q1[20]
    # renamed to Q1,Q2,Q3,...,Q20    
    if com == "Trait":
        df.columns = list(df.columns.drop(answers_trait))+answers
    
    if weighted and com != "Trait":
        print("Updated entries")
        df = weighted_scoring(df)

    # Check if state or trait results
    #if com != "Trait":
    # Calculate score
    df["score"] = df[answers].sum(axis = 1)
    # Add the time it took to complete
    df["time_to_complete(sec)"] = (pd.to_datetime(df["submitdate"])-pd.to_datetime(df["startdate"][0])).dt.seconds
    # Add the date it was completed
    df["date"] = pd.to_datetime(df["submitdate"]).dt.strftime("%Y-%m-%d %H:%M:%S")
    # Rename token to personal id
    df = df.rename({"token" : "pers_id"}, axis='columns')
    # Add if it is mock/real and before/after:
    df["comment"] = com

    # Subset to only contain certain columns
    df = df[["pers_id","comment", "date", "score", "time_to_complete(sec)"]+ answers]

    # Merge files
    new_state_csv = pd.concat([csv, df])

    # Remove Duplicates
    new_state_csv = new_state_csv.drop_duplicates()

    # Save file
    new_state_csv.to_csv(csv_file, index = False)
    
    # Save a compact file as well
    #Note: add  <header = [0,1] , index_col=[0]> 
    #when reading compact file: pd.read_csv(compact_file, <...>)
    comp_df = new_state_csv[["pers_id" , "comment", "score"]]
    comp_df = comp_df.pivot(index = "pers_id", columns = "comment")
    comp_df.to_csv(csv_file[:-4] + "_compact.csv")


for file in files:
    STAI_score(file_name = file, csv_file = "STAI_scores.csv")



print()
print()
print()
print("PRINTING SCORES")
print("---------------------------------------------------------------------------------------------------------")

df = pd.read_csv("STAI_scores.csv")
print(df)

df = pd.read_csv("STAI_scores_compact.csv" , header = [0,1] , index_col=[0])
print(df)