# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 11:10:47 2018

@author: Will
"""

import pandas as pd
import numpy as np
import os
import Tag
import pickle

def checkNumTags(df):
    #Count the number of tags in the dataframe
    count = 0
    for index, row in df.iterrows():
        if (row.isnull().sum() == 0):
            count += 1
    return count

def preprocessTag(df, gradeDict, grade):
    """
    Preprocesses and individual Tag Excel Sheet into Tag Objects that are held 
    in a Dictionary of arrays where each key corresponds to an array of tag objects
    """
    tempDf = pd.DataFrame()
    
    #innerCount is used to track the number of rows we've iterated through and comes this to numRows 
    #to determine if we've reached the end of that loc
    innerCount = 0
    
    #locCount counts which loc we're at so we know whether to put the dataframe in loc1, loc2, or loc3
    locCount = 0
    
    for index, row in df.iterrows():
        #Gets the number of rows that are NaN, in this case we care about the ones that have 3 and 4 nulls
        if (row.isnull().sum() == 0):
            #instantiate a new obj and append it to the dictionary's array
            obj = Tag.Tag()
            #Call the setInitialRow function that sets all of the attributes other the loc1, loc2, and loc3
            obj.setInitialRow(row)
            
            #appends the object we just created to the end of the array 
            gradeDict[grade].append(obj)
            
            
        elif (row.isnull().sum() == 5):
            #row that tells the number of materials in a given location
            innerCount=0
            locCount += 1
            
            #Get the number of rows to iterate through for the next elif
            numRows = row[0]
            
        elif (row.isnull().sum() == 4):
            #row that contains a material code and a location
            tempDf = tempDf.append(row)
            
            #Finishes up by renaming the columns, dropping the ones we don't need
            #and the distributing the df in loc1,2,or 3 depending on which count we're on
            if (numRows == innerCount):
                tempDf["materialCode"] = tempDf["Tag"]
                tempDf["materialAmt"] = tempDf["Grade"]
                tempDf = tempDf.drop(columns=["Tag","Grade","Oxygen","Power","Tap Wgt","Time"])
                tempDf = pd.DataFrame()
                
                if (locCount == 1):
                    gradeDict[grade][len(gradeDict[grade])-1].setLoc1(tempDf)
                elif (locCount == 2):
                    gradeDict[grade][len(gradeDict[grade])-1].setLoc2(tempDf)
                elif (locCount == 3):
                    gradeDict[grade][len(gradeDict[grade])-1].setLoc3(tempDf)

        innerCount += 1
        
def dat(gradeDict):
    for filename in os.listdir("DAT_Excel_Files"):
        #Iterates through each DAT file and reads it in as a dtaaframe
        tempName = "DAT_Excel_Files/" + filename
        tempDf = pd.read_excel(tempName)
        
        #numTags = checkNumTags(data)
        
        #Get the part of the filename that determines what grade is being discussed
        grade = filename[0:len(filename)-10]
        
        #Each grade is repreented by an array of the tags
        gradeDict[grade] = []
        
        #Populate the gradeDict with arrays of Tag objects
        preprocessTag(tempDf, gradeDict, grade)
    
def exportDict(dictionary):
    f = open("DAT_Analysis/gradeDict.pk1","wb")
    pickle.dump(dictionary,f)
    f.close()

def mix(df_MIX):
    #Iterate through the MIX excel files into one Excel sheet that includes the grade as well 
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
    return df_MIX

if __name__ == "__main__":
    df_MIX = []
    gradeDict={}

    #Peform the preprocessing
    dat(gradeDict)
    df_MIX = mix(df_MIX)
    
    #Export the results
    exportDict(gradeDict)    
    df_MIX.to_excel("MIX_Analysis/MIX_Output.xlsx")
