# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 21:45:40 2019

@author: William
"""
import pandas as pd

class Tag:
    def __init__(self):
        self.tag = None #Categorical iteger
        self.grade = None #Categorical iteger
        self.power = None #Int
        self.oxygen = None #Int
        self.tapWeight = None #Int
        self.time = None #Int that is number of "days"
        
        "Each loc contains a dataframe with 2 columns that represent the material code and the amount for each location"
        self.loc1 = None #Dataframe
        self.loc2 = None #Dataframe
        self.loc3 = None #Dataframe
        
    def getTag(self):
        return self.tag
    def setTag(self, tag):
        self.tag = tag
    
    def getGrade(self):
        return self.grade
    def setGrade(self, grade):
        self.grade = grade

    def getPower(self):
        return self.power
    def setPower(self, power):
        self.power = power

    def getOxygen(self):
        return self.oxygen
    def setOxygen(self, oxygen):
        self.oxygen = oxygen

    def getTapWeight(self):
        return self.tapWeight
    def setTapWeight(self, tapWeight):
        self.tapWeight = tapWeight

    def getTime(self):
        return self.time
    def setTime(self, time):
        self.time = time

    def getLoc1(self):
        return self.loc1
    def setLoc1(self, loc1):
        self.loc1 = loc1

    def getLoc2(self):
        return self.loc2
    def setLoc2(self, loc2):
        self.loc2 = loc2    
        
    def getLoc3(self):
        return self.loc3
    def setLoc3(self, loc3):
        self.loc3 = loc3
        
    def preprocess(self, df): 
        for index, row in df.iterrows():
        
        #Gets the number of rows that are NaN, in this case we care about the ones that have 3 and 4 nulls
        row.isnull().sum()
        