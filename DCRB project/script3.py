import os
import mysql.connector

def list_files_and_folders(root_dir):
    data = []
    for root, dirs, files in os.walk(root_dir):
        for directory in dirs:
            folder_path = os.path.join(root, directory)
            data.append([folder_path, "Folder", None, None, None])
        for file in files:
            file_path = os.path.join(root, file)
            size = os.path.getsize(file_path)
            file_name, file_extension = os.path.splitext(file)
            data.append([file_path, "File", size, file_name, file_extension])
    return data

def create_database(cursor, db_name):
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")

def create_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS file_info (
            id INT AUTO_INCREMENT PRIMARY KEY,
            path VARCHAR(255),
            type VARCHAR(255),
            size BIGINT,
            file_name VARCHAR(255),
            extension VARCHAR(255)
        )
    """)

def create_secondary_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS secondary (
            file_id INT,
            text LONGTEXT,
            FOREIGN KEY (file_id) REFERENCES file_info(id)
        )
    """)

def insert_data(cursor, data):
    sql = "INSERT INTO file_info (path, type, size, file_name, extension) VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(sql, data)

def read_file_content(file_path):
    with open(file_path, 'r', encoding='latin-1') as file:
        return file.read()

def connect_to_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Fedemysql99"
    )

def connect_to_db(db_name):
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Fedemysql99",
        database=db_name
    )

def populate_secondary_table(cursor, data):
    file_count = 0
    for row in data:
        if row[1] == 'File':
            try:
                file_content = read_file_content(row[0])
                cursor.execute("INSERT INTO secondary (file_id, text) VALUES ((SELECT id FROM file_info WHERE path = %s), %s)", (row[0], file_content))
                file_count += 1
                if file_count % 10 == 0:
                    connection.commit()  # Commit ogni 10 file
            except Exception as e:
                print(f"Errore durante la lettura del file {row[0]}: {e}")

# Connessione al server MySQL
try:
    connection = connect_to_mysql()

    if connection.is_connected():
        cursor = connection.cursor()
        print("Connessione al server MySQL riuscita")

        # Creazione del database se non esiste
        create_database(cursor, "dcrb")

        # Connessione al database appena creato
        connection.database = "dcrb"

        # Crea le tabelle da zero
        create_table(cursor)
        create_secondary_table(cursor)

        # Popola la tabella file_info
        root_directory = r'C:\xampp\htdocs\DCRB project'
        data = list_files_and_folders(root_directory)
        
        insert_data(cursor, data)
        connection.commit()

        # Popola la colonna text nella tabella secondary
        populate_secondary_table(cursor, data)
        connection.commit()

        print("Tabelle 'file_info' e 'secondary' create e dati inseriti correttamente")

except mysql.connector.Error as e:
    print("Errore durante la connessione al server MySQL:", e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
