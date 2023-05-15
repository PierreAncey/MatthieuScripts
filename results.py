######################################################################################################################
# IMPORTS
######################################################################################################################
from genericpath import exists
from operator import index
import os  
import shutil
import random
import csv
from pathlib import Path
import pandas as pd


######################################################################################################################
# SETTINGS
######################################################################################################################
totalMoneyToGive = 20
# Path to the folder where data is stored
path = r"C:\Users\Pierre\Documents\Unity\DataTest"

generate = True


######################################################################################################################
# ARRAYS TO STORE INFORMATIONS
######################################################################################################################
folders = os.listdir(path+ "\\Observers")


######################################################################################################################
# GENERATE FOLDERS
######################################################################################################################
if generate:
    for i in range(len(folders)):
        df = pd.read_csv(path + "\\Observers" + "\\" + folders[i] + "\\Correspondance.csv", header=0)

        Money = [random.randrange(4) for i in range(5)]
        sum = 0
        for j in range(len(Money)):
            sum += Money[j]
        Money.append(totalMoneyToGive-sum)

        df["Money"] = Money
        df.to_csv(path + "\\Observers" +  "\\" + folders[i] + "\\Results.csv", index=False)


######################################################################################################################
# ADD MONEY TO THE CORRECT NAME
######################################################################################################################
# Clean the names
Names = os.listdir(path+r"/Animations")
for i in range(len(Names)):
    Names[i] = Names[i].replace(".controller", "")

# Add a money array
Money = [0 for i in range(len(Names))]

# Add the money to the correct name
for i in range(len(folders)):
    df = pd.read_csv(path + "\\Observers" + "\\" + folders[i] + "\\Results.csv", header=0)
    df['Name'] = df['Name'].apply(lambda x: x.replace(".mp4", ""))
    for index,row in df.iterrows():
        if row["Name"] in Names:
            Money[Names.index(row["Name"])] += row["Money"]
        else:
            raise Exception("Name not found")


######################################################################################################################
# WRITE THE CSV
######################################################################################################################
with open(path + "\\TotalResults.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Money"])
    for i in range(len(Names)):
        writer.writerow([Names[i], Money[i]])
