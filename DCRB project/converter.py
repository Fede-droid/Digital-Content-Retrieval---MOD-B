import os
import csv

def list_files_and_folders(root_dir):
    data = []
    for root, dirs, files in os.walk(root_dir):
        for directory in dirs:
            folder_path = os.path.join(root, directory)
            data.append([folder_path, "Folder", "-", "-"])
        for file in files:
            file_path = os.path.join(root, file)
            size = os.path.getsize(file_path)
            data.append([file_path, "File", size, "-"])
    return data

def write_to_csv(data, csv_file):
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Path', 'Type', 'Size (bytes)', 'Permissions'])
        for row in data:
            writer.writerow(row)

# Directory radice da analizzare
root_directory = r'C:\xampp\htdocs\DCRB'

# Ottieni le informazioni su cartelle, sottocartelle e file
data = list_files_and_folders(root_directory)

# Scrivi le informazioni in un file CSV
csv_file = 'file_info.csv'
write_to_csv(data, csv_file)

print("File CSV creato con successo:", csv_file)
