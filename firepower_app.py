# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 20:02:56 2023

@author: jimmy
"""


import pandas as pd
import numpy as np
import random

#Set roll range, here we could also create scenarios
roll=random.randrange(1,100)


#Import csv and set turn to 0
df = pd.read_csv(r'C:\Users\jimmy\OneDrive\Desktop\FP_tool\unit_sample.csv')
df['Turn']=0
turn=0

#Generate random fp numbers as an example
df['Firepower']=np.random.randint(500,1000,size=16)


#Function for looking up a unit, we could create a new definition to include turn
def look(Brigade,Battalion):
    Br=Brigade
    Ba=Battalion
    return df.loc[(df['Brigade'] == Br) & (df['Battalion'] == Ba) & (df['Turn']==turn)]


def engagement(color): 
    bunits = int(input("Enter the number of {} units:".format(color)))
    turn = int(input("Enter the turn number:"))
    bdf2 = pd.DataFrame(data=None,columns=["Brigade", "Battalion","Strength", "Firepower","Turn"])

    for _ in range(bunits):
        #Set roll range here, later we can adjust for type for attack/defense
        #roll=random.randrange(1,100)
        ubr = input("Enter Brigade ")
        uba = input("Enter Battalion ")

        #Load in cofm, we need to do this for each engagement now
        #Just restructure to load in blue first and then load red
        #Then do the battle roll, then apply attrition

        print ('The current unit strength is: \n',look(int(ubr),int(uba)))
        fp=look(int(ubr),int(uba))['Firepower'].item()
        s=look(int(ubr),int(uba))['Strength'].item()
        #s = input("Enter strength for {} brigade {} battalion".format(ubr,uba))
        bdf1 = pd.DataFrame(data=[[ubr,uba,s,fp,turn]],columns=["Brigade", "Battalion","Strength", "Firepower","Turn"])

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
    
    #implement min -currently this can roll too high and make unit stronger
    attr=((roll/100)*(100/(bratio*100)))/(bratio*(100/(bratio*100)*0.5))
    
    
    b['Strength']=b['Strength']*attr
    df=pd.concat([df,b], axis=0)
    return df


#def print_df():
    

if __name__ == '__main__':
    unit_list = get_engagements(df)
    print(unit_list)
    #write to csv
    #df.to_csv(index=False)