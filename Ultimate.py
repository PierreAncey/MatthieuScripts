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
import time
import argparse


######################################################################################################################
# CMD TOOLS
######################################################################################################################
# Print progressive var (inspired from https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters)
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}%, {str(iteration+1)}/{str(total+1)}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        # print(f"\n\n{suffix}")
        print()

# Start time of the program
start_time = time.time()

# Argument parser
parser = argparse.ArgumentParser(description = 'Specify arguments if you want the action to occur')
parser.add_argument("-f", help="(DEBUG) Generate files", action="store_true")
parser.add_argument("-l", help="(DEBUG) Shows results in cmd", action="store_true")
parser.add_argument("-s", help="Does not save results matrix in a csv file", action="store_false")
args = parser.parse_args()


######################################################################################################################
# SETTINGS
######################################################################################################################
# Path to the folder where data is stored
path = r"C:\Users\Pierre\Documents\Unity\DataTest"

# Number of experiments
nbParticipants = 300

# Number of try (set to number of participants as a default)
nbTry = 20

# Nom du fichier csv contenant la correspondance pour l'anonmymisation
csvName = "Correspondance.csv"

# Name of avatars
avatarNames = ["F1", "F2", "F3", "M1", "M2", "M3"]

# Create folder (for debug purposes)
create_folders = args.f
# create_folders = True

# Print lists in terminal (for debug purposes)
check_list = args.l
# check_list = True

# Save results matrix in a csv file
save_results = args.s
# save_results = True


######################################################################################################################
# ARRAYS TO STORE INFORMATIONS
######################################################################################################################
# Columns
columns = []

# 3 men 3 women per line condition
init = ["m", "m", "m", "f", "f", "f"]

# Array to store the combinations
combinations = []

# Male names
male_names = ["m_PA", "m_PB", "m_PC", "m_PD", "m_PE", "m_PF", "m_PG", "m_PH", "m_PI", "m_PJ"]
female_names = ["f_ZA", "f_ZB", "f_ZC", "f_ZD", "f_ZE", "f_ZF", "f_ZG", "f_ZH", "f_ZI", "f_ZJ"]


######################################################################################################################
# FUNCTIONS
######################################################################################################################
# Define a function that checks if an element of a list belongs to another list at the same index
def are_items_same_place(l1, l2):
    result = False
    for i in range(len(l1)):
        if l1[i] == l2[i]:
            result = True
    return result

# Negate male/female list (i.e. take complementary)
def negate(list):
    result = []
    for i in range(len(list)):
        if list[i] == "m":
            result.append("f")
        else:
            result.append("m")
    return result

# Create column_i based on maleFiles, femaleFiles, combinations and column index
def create_column_i(maleFiles, femaleFiles, i):
    column_i = []
    male_index = 0
    female_index = 0
    for j in range(nbTry):
        if combinations[j][i] == "m":
            column_i.append(maleFiles[male_index])
            male_index += 1
        else:
            column_i.append(femaleFiles[female_index])
            female_index += 1
    return column_i


######################################################################################################################
# GENERATE FOLDERS
######################################################################################################################
# Boolean that checks if the folder Observers already exists
observer_exists = os.path.exists(path+r"/Observers/")

# Make print prettier
if (create_folders or (not observer_exists)):
    print("###############################################################################################")
    print("# FILE/FOLDER CREATIONS")
    print("###############################################################################################\n")

# Creation of files (for debug purposes)
if create_folders:
    # Genereates folders with avatars' name and sexes (inside)
    for i in avatarNames:
        avatarfolder = path+r"/"+i
        # Creates folder if it doesn't exist yet
        if (not os.path.exists(avatarfolder)):
            os.mkdir(path+r"/"+i)
            print("Avatar folder created for "+i + " !")
        if (not os.path.exists(avatarfolder+r"/Male")):
            os.mkdir(path+r"/"+i+r"/Male")
            print("Male folder created for "+i + " !")
        if (not os.path.exists(avatarfolder+r"/Female")):
            os.mkdir(path+r"/"+i+r"/Female")
            print("Female folder created for "+i + " !")
            print("\n")

    # Generate nbTry/2 mp4 files for each avatar in male and female folders
    for i in avatarNames:
        avatarfolder = path+r"/"+i
        malefolder = avatarfolder +r"/Male"
        femalefolder = avatarfolder + r"/Female"
        for j in range(nbTry//2):
            Path(malefolder + r"/"+str(male_names[j])+r".mp4").touch()
            Path(femalefolder + r"/"+str(female_names[j])+r".mp4").touch()
            # Path(malefolder + r"/"+str(j)+r".mp4").touch()
            # Path(femalefolder + r"/"+str(j)+r".mp4").touch()
        print("Files created for avatar " + i + " !")

# Create a new folder for Observers if it doesn't exist yet
if (not observer_exists):
    os.mkdir(path+r"/Observers/")
    print("\nObservers folder created !")


######################################################################################################################
# CREATE COMBINATIONS
######################################################################################################################
# Create combinations (one random and one complementary)
for i in range(nbTry):
    temp = init.copy()
    random.shuffle(temp)
    combinations.append(temp)
    combinations.append(negate(temp))


######################################################################################################################
# SHUFFLE FILES TO RESPECT CONSTRAINTS:
# - ONE REAL PERSON CAN'T BE PRESENTED TWICE TO ONE OBSERVER
# - EACH OBSERVER CAN'T SEE THE SAME AVATAR TWICE 
# - EACH VIDEO MUST BE SEEN ONCE
######################################################################################################################
first_iteration = True
total_tries = 0
# Add all files for all avatars to the list with a shuffle
for i in range(len(avatarNames)):
    # Obtain all mp4 files for the current avatar
    maleFiles = os.listdir(path+r"/"+avatarNames[i]+r"/Male")
    femaleFiles = os.listdir(path+r"/"+avatarNames[i]+r"/Female")

    # Remove .mp4 extension from names
    maleFiles = [x[:-4] for x in maleFiles]
    femaleFiles = [x[:-4] for x in femaleFiles]
        
    if first_iteration:
        # Shuffle files' names
        random.shuffle(maleFiles)
        random.shuffle(femaleFiles)
        
        # Store male/female according to the order defined in combinations
        column_i = create_column_i(maleFiles, femaleFiles, i)
    elif (not first_iteration):
        tries = 0
        continue_while = True
        # Brute Force method
        while(continue_while):
            ok = True
            random.shuffle(maleFiles)
            random.shuffle(femaleFiles)
            column_i = create_column_i(maleFiles, femaleFiles, i)
            for k in range(i):
                if (are_items_same_place(columns[k], column_i)):
                    ok = False

            continue_while = not ok
            if continue_while:
                tries+=1
        # Count total number of shuffles        
        total_tries += tries

    # Store column_i in columns
    columns.append(column_i)

    # Set first_iteration to False
    first_iteration = False


######################################################################################################################
# RESULTS MATRIX
######################################################################################################################
# Add results to a matrix
results = []
for i in range(nbTry):
    results.append([])
    for j in range(len(avatarNames)):
        results[i].append(columns[j][i])
# print(results)


######################################################################################################################
# SAVE MATRIX OF AVATARS AND OBSERVER NUMBERS IN CSV FILE
######################################################################################################################
if save_results:
    # Create a csv file to store the results
    with open(path+r"/"+r"Observer_avatar_matrix.csv", 'w', newline="") as file:
        # Create a header
        writer = csv.writer(file)
        temp = avatarNames.copy()
        temp.insert(0, "Observer")
        writer.writerow(temp)

        # Add rows
        for j in range(nbTry):
            temp = results[j].copy()
            temp.insert(0, j)
            writer.writerow(temp)


######################################################################################################################
# CHECKS LIST
######################################################################################################################
if check_list:
    # Make print prettier
    print("\n###############################################################################################")
    print("# CHECK LISTS")
    print("###############################################################################################\n")

    # Results
    print("Results:")
    for i in range(nbTry):
        print(results[i])

    # Columns
    print("\n\nColumns:")
    for j in range(len(avatarNames)):
        print("Column "+str(j)+ ":\n", columns[j])

    # Total number of shuffles
    print("\n\nTotal number of tries: ", total_tries)


######################################################################################################################
# MAIN ALGORITHM TO PLACE VIDEOS ANONYMISED IN OBSERVER FOLDERS
######################################################################################################################
# Make print prettier
print("\n###############################################################################################")
print("# PROGRESS")
print("###############################################################################################\n")

# Initial progress bar
printProgressBar(0, 6*nbTry-1, prefix = 'Progress:', suffix = 'COMPLETE !', length = 50)

# Copies files in a new folder for an observer
for j in range(nbTry):
    folder = path+r"/Observers/"+str(j)

    # Remove precedent folders with the same name and create a new one
    if(os.path.exists(folder)):
        shutil.rmtree(folder)
    os.mkdir(folder)

    # Move files to a new folder for each observer and saves correspondance in csv file
    with open(folder+r"/"+csvName, 'w', newline='') as file:
        # Add header
        writer = csv.writer(file)
        writer.writerow(["Number", "Avatar", "Name"])

        # To allow random view of avatars
        k = [i for i in range(len(avatarNames))]
        random.shuffle(k)

        for i in range(len(avatarNames)):
            # Move files to observer folder
            if (combinations[j][i] == "m"):
                shutil.copyfile(path+r"/"+avatarNames[i]+r"/Male/"+columns[i][j]+".mp4" , folder+r"/"+str(k[i])+".mp4")
            else:
                shutil.copyfile(path+r"/"+avatarNames[i]+r"/Female/"+columns[i][j]+".mp4" , folder+r"/"+str(k[i])+".mp4")

            # Print progress bar
            # time.sleep(0.03)
            printProgressBar(6*j + i, 6*nbTry-1, prefix = 'Progress:', suffix = 'COMPLETE !', length = 50)
                
            writer.writerow([str(k[i]), avatarNames[k[i]], columns[i][j]])


# Print total time to run the program
print("\nProgram completed in: ", round(time.time()-start_time,2), " seconds")