#!/usr/bin/env python
# coding: utf-8
from email.parser import BytesParser
from posixpath import basename
import numpy as np
import pandas as pd
import glob
import email
from email.parser import BytesParser
from email import policy
import os


# Dir to folder containing all excel files
response_dir = "Files_ig/Responses/"
files = glob.glob(response_dir+"*")

def weighted_scoring(df):
    '''
    Change scoring acording to scoring key
    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe to change from answers index to score.

    Returns
    -------
    tmp_df : pandas.DataFrame
        pandas dataframe same as df but where entries of Qi 
        contains score of question i
        rather than the answer option for question i.
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

#Load token ids
def get_tokens(eml_file):
    #Load token ids
    with open(eml_file, "rb") as fp:
        msg = BytesParser(policy = policy.default).parse(fp)
    text = msg.get_body(preferencelist=("plain")).get_content()

    #list of all tokens
    tokens = [line for line in text.split() if "token" in line]
    tokens = [i[36:].split("&")[0] for i in tokens]
    tokens = tokens[::2]

    #Token directory
    token_dict = {"app00"+str(i) : tokens[i-1] for i in range(1,10)}
    for i in range(10,21):
        token_dict["app0"+str(i)] = tokens[i-1]

    #Switch keys and values
    token_dict = {y:x for x,y in token_dict.items()}
    return token_dict

def score_stai(files_dir, save, base_name):

    #Answer columns
    answers = ["Q"+str(i) for i in range(1,21)]
    #Column names for Trait quiestionnaire
    #of the form Q1[1],Q1[2],Q1[3],...,Q1[20] 
    answers_trait = ["Q1[" +str(i) + "]" for i in range(1,21) ]
    #column_names = ["pers_id","comment", "date", "score", "time_to_complete(sec)"] +answers
    base_df = pd.DataFrame()


    for file in glob.glob(files_dir+"*"):
        file_name = os.path.basename(file)[len(base_name):-5]
        survey_type = survey_dict[file_name]
        df = pd.read_excel(file)
        if survey_type == "Trait":
            #If trait rename columns names
            df.columns = list(df.columns.drop(answers_trait))+answers

        df["score"] = df[answers].sum(axis = 1)
        # Add the time it took to complete
        df["time_to_complete(sec)"] = (pd.to_datetime(df["submitdate"])-pd.to_datetime(df["startdate"][0])).dt.seconds
        # Add the date it was completed
        df["date"] = pd.to_datetime(df["submitdate"]).dt.strftime("%Y-%m-%d %H:%M:%S")
        # Rename token to personal id
        df = df.rename({"token" : "pers_id"}, axis='columns')
        # Add if it is mock/real and before/after:
        df["comment"] = survey_type

        # Subset to only contain certain columns
        df = df[["pers_id","comment", "date", "score", "time_to_complete(sec)"]+ answers]
        base_df = pd.concat([df,base_df])
    
    if save:
        base_df.to_csv("STAI_scores.csv", index = False)
    return base_df

def compact_scores(stai_df, save, token_dict):
    comp_df = stai_df[["pers_id", "comment", "score", "time_to_complete(sec)"]]
    comp_df = comp_df.dropna()
    comp_df = comp_df.replace({"pers_id": token_dict})
    comp_df = comp_df.loc[comp_df["pers_id"].isin(list(token_dict.values()))]
    comp_df = comp_df.reset_index(drop = True)
    comp_df = comp_df[["pers_id", "comment", "score"]]
    comp_df = comp_df.pivot(index = "pers_id", columns = "comment", values = "score").reset_index()

    if save:
        comp_df.to_csv("STAI_scores_compact.csv", index = False)
    return comp_df

#Basename for the files
base_name = "results-survey"
#Survey dictionary
survey_dict = {"434315" : "Trait",
               "443767" : "Home_State",
               "238699" : "After_MR",
               "318579" : "Before_MR",
               "411894" : "After_Mock",
               "727961" : "Before_Mock"}
token_dict = get_tokens("Files_ig/App_id_token_links.eml")

# Dir to folder containing all excel files
response_dir = "Files_ig/Responses/"

#score the stai questionaires
score_stai(files_dir = response_dir, save = True, base_name = base_name)

#create compact dataframe
df = pd.read_csv("STAI_scores.csv")
compact_scores(stai_df = df, save = True, token_dict = token_dict)

print()
print("-----------------------------------------------")
print()
df = pd.read_csv("STAI_scores.csv")
print(df)

print()
print("-----------------------------------------------")
print()
df = pd.read_csv("STAI_scores_compact.csv" , header = [0,1] , index_col=[0])
print(df)