# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 20:02:56 2023

@author: jimmy
"""
#To do list:
#Append type/color: Done
#If there was an engagement, how to track? Ask if turn is over and reappend?
#Ensure pulls current turn FP: Done
#Additional collumn for combat ineffective?
#Create dashboard
#Type of engagement (as an option) Track it too?
#Create notes column to define who is attacking who
#How to track multiple engagements same turn (turn 1a,b,c?)
#dashboard concept: Bar chart. Title=current turn. Display current str for blue, seperate chart for red. Dashed horizontal line showing threshold for combat ineffective

import pandas as pd
import numpy as np
import random




#Set roll range, here we could also create scenarios
roll=random.randrange(1,100)


#Import csv and set turn to 0
df = pd.read_csv(r'C:\Users\jimmy\OneDrive\Desktop\FP_tool\unit_sample.csv')
#df['Turn']=0
#turn=0

#Generate random fp numbers as an example
#df['Firepower']=np.random.randint(500,1000,size=16)


#Function for looking up a unit, we could create a new definition to include turn
def look(Brigade,Battalion,Turn):
    Br=Brigade
    Ba=Battalion
    #We want to grab the previous turn's unit strength
    Turn=Turn-1
    return df.loc[(df['Brigade'] == Br) & (df['Battalion'] == Ba) & (df['Turn']==Turn)]


def engagement(color): 
    bunits = int(input("Enter the number of {} units:".format(color)))
    #turn = int(input("Enter the turn number:"))
    bdf2 = pd.DataFrame(data=None,columns=["Brigade", "Battalion","Strength", "Firepower","Turn"])

    for _ in range(bunits):
        #Set roll range here, later we can adjust for type for attack/defense
        #roll=random.randrange(1,100)
        ubr = input("Enter Brigade ")
        uba = input("Enter Battalion ")

        #Load in cofm, we need to do this for each engagement now
        #Just restructure to load in blue first and then load red
        #Then do the battle roll, then apply attrition

        print ('The current unit strength is: \n',look(int(ubr),int(uba),turn))
        fp=look(int(ubr),int(uba),turn)['Firepower'].item()
        s=look(int(ubr),int(uba),turn)['Strength'].item()
        #s = input("Enter strength for {} brigade {} battalion".format(ubr,uba))
        bdf1 = pd.DataFrame(data=[[ubr,uba,s,fp,turn,color]],columns=["Brigade", "Battalion","Strength", "Firepower","Turn","Color"])

        bdf2 = pd.concat([bdf1,bdf2], axis=0)



    bdf2.index = range(len(bdf2.index))
    #print (bdf2, "Is this correct for {}?".format(color))
    return (bdf2)


def get_engagements(df):

    b=engagement('blue')
    r=engagement('red')
    bf=b['Firepower'].sum()
    rf=r['Firepower'].sum()
    
    bratio=bf/(bf+rf)
    #End function here and do attrit seperate?
    
    #Need to do blue attrition seperate from red
    #attr=((roll/100)*(100/(bratio*100)))/(bratio*(100/(bratio*100)*0.5))
    #This limits attrition to 100%
    
    #set attr formula
    battr=((roll/100)*(100/(bratio*100)))/(bratio*(100/(bratio*100)*0.5))
    battr=1/battr
    if battr>1:
       battr=1
    else:
        battr=battr
    
    rattr=1-battr
    
    b['Strength']=b['Strength']*battr
    r['Strength']=r['Strength']*rattr

    #df['Strength']=b['Stength']
    #df['Strength']=r['Stength']
    df=pd.concat([df,b], axis=0)
    df=pd.concat([df,r], axis=0)
    df.to_csv(r'C:\Users\jimmy\OneDrive\Desktop\FP_tool\unit_sample.csv',index=False)
    return df


#def print_df():

def copy_prev_turn(df,turn):
    turn=turn
    df=df
    df2= (df.loc[df['Turn']==(turn-1)])
    df2['Turn']=turn
    df=pd.concat([df,df2], axis=0)
    df.to_csv(r'C:\Users\jimmy\OneDrive\Desktop\FP_tool\unit_sample.csv',index=False)
    return df



if __name__ == '__main__':
    turn=int(input("Enter the turn number:"))
    copy_prev_turn(df,turn)
    df = pd.read_csv(r'C:\Users\jimmy\OneDrive\Desktop\FP_tool\unit_sample.csv')
    q='n'    
    while q == "n":
        #turn=input('What is the current turn')        
        unit_list = get_engagements(df)
        unit_list.to_csv(r'C:\Users\jimmy\OneDrive\Desktop\FP_tool\unit_sample.csv',index=False)
        print(unit_list)
        q=input("Is the turn over? y/n ") 
    #Cycle through until turn is over, append all unused units
    #Check to see if unit is on current turn list and if not, append
    #or easier option, copy dataframe, append new turn and then apply engagements to current turn
    #write to csv




#concat df2 to df
#apply attrition to df as opposed to making new rows (just copy over where they match)
