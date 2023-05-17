# What are the scripts ? When and how to use them ?

## 1. process_data.py
### How to use
Please specify the value of the variable **path** under *Settings* in the script to where your participants' folders are.

Then, run the following command in the terminal:
```
python process_data.py
```

### When to use
After having downloaded the data from Switch Drive.

### What it does
For each participant folder, it will modify the contained files so that they have the same name as the folder. Finally, it will create a new structure of folders and files (see under) and move the modified files to the new structure according to their extension.

```
Data
    ├───Animations
    └───Voices
```

## 2. generate_observer_folders.py
### How to use
Please specify the value of the variable **path** under *Settings* in the script to where your "Data" folder is.

Then, run the following command in the terminal:
```
python generate_observer_folders.py
```

### When to use
After having run the Unity project to generate the videos.

### What it does
It will create the folders for the observers with anonymous videos (The real video names are stored in "Correspondance.csv"). Furthermore, the following conditions are respected:
- One real person can not be presented twice to one observer
- Each observer can not see the same avatar twice 
- Each video must be seen once


## 3. detect_money.py
### How to use
Please specify the value of the variable **path** under *Settings* in the script to where your "Data" folder is.

Then, run the following command in the terminal:
```
python detect_money.py
```

### When to use
After having used the website to collect the results.

### What it does
Combines all the money that each participant avatar has earned and stores it in a csv file ("TotalResults.csv").
