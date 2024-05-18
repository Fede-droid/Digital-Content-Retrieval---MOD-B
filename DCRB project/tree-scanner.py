#C:\xampp\htdocs\DCRB project

import os

def list_files_and_folders(root_dir):
    for root, dirs, files in os.walk(root_dir):
        print("Current directory:", root)
        print("Subdirectories:", dirs)
        print("Files:", files)
        print("-" * 50)

# Esempio di utilizzo
root_directory = r'C:\xampp\htdocs\DCRB project'
list_files_and_folders(root_directory)
