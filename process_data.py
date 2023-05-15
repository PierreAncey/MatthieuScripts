######################################################################################################################
# IMPORTS
######################################################################################################################
import os


######################################################################################################################
# SETTINGS
######################################################################################################################
# Precise the path to where the participants' folders are
path = r"C:\Users\Pierre\Documents\Unity\DataTest"


######################################################################################################################
# METHODS
######################################################################################################################
# Get the folders in the same directory as the script
def get_folders():
    """
    Get the folders in the same directory as the script

    Returns:
        list: The list of folders
    """

    # Declare the list of folders
    folders = []
    
    # Loop over all the files in the directory
    for folder in os.listdir(path):
        # Check if the file is a folder
        if os.path.isdir(os.path.join(path, folder)):
            # Add the folder to the list
            folders.append(folder)

    return folders



# Loop over all the folders. In each folder, rename the files with the folder name and keep the extension
def rename_files():
    """
    Loop over all the folders. In each folder, rename the files with the folder name and keep the extension

    Returns:
        void
    """

    # Get the folders
    folders = get_folders()

    # Show the folders
    print(folders)

    # Loop over the folders
    for folder in folders:
        # Loop over the files in the folder
        for file in os.listdir(os.path.join(path, folder)):
            # Check if the file is a file
            if os.path.isfile(os.path.join(path, folder, file)):
                # Get the extension of the file
                extension = os.path.splitext(file)[1]

                # Rename the file
                os.rename(os.path.join(path, folder, file), os.path.join(path, folder, folder + extension))



# Move all the .fbx and .controller files to the folder "Data/Animations" and all the .wav files to the folder "Data/Voices"
def move_files():
    """
    Move all the .fbx and .controller files to the folder "Data/Animations" and all the .wav files to the folder "Data/Voices"

    Returns:
        void
    """

    # Get the folders
    folders = get_folders()

    # Rename the files
    rename_files()

    # Create the folders "Data/Animations" and "Data/Voices" if they don't exist
    if not os.path.exists(os.path.join(path, "Data")):
        os.mkdir(os.path.join(path, "Data"))
    if not os.path.exists(os.path.join(path, "Data", "Animations")):
        os.mkdir(os.path.join(path, "Data", "Animations"))
    if not os.path.exists(os.path.join(path, "Data", "Voices")):
        os.mkdir(os.path.join(path, "Data", "Voices"))

    # Loop over the folders
    for folder in folders:
        # Loop over the files in the folder
        for file in os.listdir(os.path.join(path, folder)):
            # Check if the file is a file
            if os.path.isfile(os.path.join(path, folder, file)):
                # Get the extension of the file
                extension = os.path.splitext(file)[1]

                # Move the file to the correct folder
                if extension == ".fbx" or extension == ".controller":
                    os.rename(os.path.join(path, folder, file), os.path.join(path, "Data", "Animations", file))
                elif extension == ".wav":
                    os.rename(os.path.join(path, folder, file), os.path.join(path, "Data", "Voices", file))



######################################################################################################################
# MAIN
######################################################################################################################
# When running the script, move the files (to run the script, type "python process_data.py" with the terminal opened in the same directory as the script)
if __name__ == "__main__":
    move_files()