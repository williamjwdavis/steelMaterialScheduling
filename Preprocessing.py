# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 11:10:47 2018

@author: Will
"""

import pandas as pd
import numpy as np
import os

datList = []

df_DAT = []
df_MIX = []

count = 0

for filename in os.listdir("DAT_Excel_Files"):
    tempName = "DAT_Excel_Files/" + filename
    
    tempDf = pd.read_excel(tempName)
    df = pd.DataFrame()
    count = 0
    
    for index, row in tempDf.iterrows():
        #Gets the number of rows that are NaN, in this case we care about the ones that have 3 and 4 nulls
        if (row.isnull().sum() == 0):
            #first row with most of the columns
            if (count == 0):
                pass
            else:
                df1 = df
                df1["materialCode"] = df1["Tag"]
                df1["materialAmt"] = df1["Grade"]
                df1 = df1.drop(columns=["Tag","Grade","Oxygen","Power","Tap Wgt","Time"])
                df = pd.DataFrame()
            
        elif (row.isnull().sum() == 5):
            #row that tells the number of materials in a given location
            
            #Get the number of rows to iterate through for the next elif
            numRows = row[0]
            
        elif (row.isnull().sum() == 4):
            #row that contains a material code and a location
            print(row)
            df = df.append(row)
        count += 1 
        #print(row.isnull().sum())

        


for filename in os.listdir("DAT_Excel_Files"):
    tempName = "DAT_Excel_Files/" + filename
    if count == 0:
        df_DAT = pd.read_excel(tempName)
    else:
        df_DAT = df_DAT.append(pd.read_excel(tempName))    
    count = count+1

count = 0    
for filename in os.listdir("MIX_Excel_Files"):
    grade = ""
    
    seperator = '('
    grade = filename.split(seperator, 1)[0]
    
    tempName = "MIX_Excel_Files/" + filename
    
    if count == 0:
        df_MIX = pd.read_excel(tempName)
        df_MIX_newCol = []
    
        for index in range(len(df_MIX)):
            df_MIX_newCol.append(grade)
        
        df_MIX["Grade"] = df_MIX_newCol
    else:
        df_MIX_temp = pd.read_excel(tempName)
        df_MIX_newCol = []
        
        for index in range(len(df_MIX_temp)):
            df_MIX_newCol.append(grade)
        
        df_MIX_temp["Grade"] = df_MIX_newCol
        df_MIX = df_MIX.append(df_MIX_temp)
    count = count+1

df_DAT.to_excel("DAT_Analysis/DAT_Output.xlsx")
df_MIX.to_excel("MIX_Analysis/MIX_Output.xlsx")

"""
for filename in os.listdir("DAT"):
    datList.append(pd.read_excel(filename))

for filename in os.listdir("MIX"):
    datList.append(pd.read_excel(filename))
""" 
