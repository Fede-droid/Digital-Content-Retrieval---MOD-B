# © Federico, Cignoli - DCR-modB University Project

import os                           
import mysql.connector              

def list_files_and_folders(root_dir):
    data = []                       # Initialize an empty list to store file and folder data
    for root, dirs, files in os.walk(root_dir):  # Traverse the directory tree
        for directory in dirs:                    # Iterate over directories
            folder_path = os.path.join(root, directory)  # Get the full path of the directory
            data.append([folder_path, "Folder", None, None, None])  # Append directory info to data
        for file in files:                        # Iterate over files
            file_path = os.path.join(root, file)  # Get the full path of the file
            size = os.path.getsize(file_path)     # Get the size of the file
            file_name, file_extension = os.path.splitext(file)  # Split the file name and extension
            data.append([file_path, "File", size, file_name, file_extension])  # Append file info to data
    return data                                  # Return the collected data

def create_database(cursor, db_name):
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")  # Create the database if it doesn't exist

def create_table(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS file_info (
                      id INT AUTO_INCREMENT PRIMARY KEY, 
                      path VARCHAR(255), 
                      type VARCHAR(255), 
                      size BIGINT, 
                      file_name VARCHAR(255), 
                      extension VARCHAR(255))""")  # Create the file_info table if it doesn't exist

def create_secondary_table(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS secondary (
                      file_id INT, 
                      text LONGTEXT, 
                      FOREIGN KEY (file_id) REFERENCES file_info(id))""")  # Create the secondary table if it doesn't exist

def insert_data(cursor, data):
    sql = "INSERT INTO file_info (path, type, size, file_name, extension) VALUES (%s, %s, %s, %s, %s)"  # SQL query for inserting data
    cursor.executemany(sql, data)  # Execute the query with the provided data

def read_file_content(file_path):
    with open(file_path, 'r', encoding='latin-1') as file:  # Open the file with latin-1 encoding
        return file.read()  # Read and return the file content

def disable_foreign_key_check(cursor):
    cursor.execute("SET FOREIGN_KEY_CHECKS=0")  # Disable foreign key checks

def enable_foreign_key_check(cursor):
    cursor.execute("SET FOREIGN_KEY_CHECKS=1")  # Enable foreign key checks

def drop_table(cursor, table_name):
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")  # Drop the specified table if it exists

def connect_to_mysql():
    return mysql.connector.connect(  # Connect to the MySQL server
        host="localhost",
        user="root",
        password="Fedemysql99"
    )

def connect_to_db(db_name):
    return mysql.connector.connect(  # Connect to the specified database
        host="localhost",
        user="root",
        password="Fedemysql99",
        database=db_name
    )

# Connect to the MySQL server
try:
    connection = connect_to_mysql()

    if connection.is_connected():
        cursor = connection.cursor()
        print("Connected to MySQL server successfully")

        # Create the database if it doesn't exist
        create_database(cursor, "dcrb")

        # Connect to the newly created database
        connection.database = "dcrb"

        # Disable foreign key checks
        disable_foreign_key_check(cursor)

        # Drop tables if they exist
        drop_table(cursor, "secondary")
        drop_table(cursor, "file_info")

        # Create the tables from scratch
        create_table(cursor)
        create_secondary_table(cursor)

        # Enable foreign key checks
        enable_foreign_key_check(cursor)

        # Commit the changes
        connection.commit()
        print("Tables 'file_info' and 'secondary' created successfully")

except mysql.connector.Error as e:
    print("Error connecting to MySQL server:", e)

finally:
    if connection.is_connected():
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection

# Connect to the MySQL database
try:
    connection = connect_to_db("dcrb")

    if connection.is_connected():
        cursor = connection.cursor()
        print("Connected to MySQL database successfully")

        # Root directory to analyze
        root_directory = r'C:\xampp\htdocs\DCRB'

        # Get information on folders, subfolders, and files
        data = list_files_and_folders(root_directory)

        # Populate the file_info table with the collected data in batches of 10 items
        batch_size = 10
        for i in range(0, len(data), batch_size):
            insert_data(cursor, data[i:i + batch_size])
            connection.commit()  # Commit every 10 items

        # Populate the text column with file content in batches of 10 items
        file_count = 0
        for row in data:
            if row[1] == 'File':
                try:
                    file_content = read_file_content(row[0])
                    cursor.execute("INSERT INTO secondary (file_id, text) VALUES ((SELECT id FROM file_info WHERE path = %s), %s)", (row[0], file_content))
                    file_count += 1
                    if file_count % 10 == 0:
                        connection.commit()  # Commit every 10 files
                except Exception as e:
                    print(f"Error reading file {row[0]}: {e}")

        # Final commit for any remaining items
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()
        print("Data inserted into the database successfully")

except mysql.connector.Error as e:
    print("Error connecting to MySQL database:", e)
