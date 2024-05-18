import os
import mysql.connector

def list_files_and_folders(root_dir):
    data = []
    for root, dirs, files in os.walk(root_dir):
        for directory in dirs:
            folder_path = os.path.join(root, directory)
            data.append([folder_path, "Folder", None, None, None, None])  # Aggiungi None per l'ultima colonna 'text'
        for file in files:
            file_path = os.path.join(root, file)
            size = os.path.getsize(file_path)
            file_name, file_extension = os.path.splitext(file)
            text_content = None
            if file_extension.lower() == '.txt':  # Legge il contenuto del file solo se è un file di testo
                text_content = read_file_content(file_path)
            data.append([file_path, "File", size, file_name, file_extension, text_content])
    return data

def create_database(cursor, db_name):
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")

def create_combined_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS file_info (
            id INT AUTO_INCREMENT PRIMARY KEY,
            path VARCHAR(255),
            type VARCHAR(255),
            size BIGINT,
            file_name VARCHAR(255),
            extension VARCHAR(255),
            text LONGTEXT
        )
    """)

def insert_data(cursor, data):
    sql = """
        INSERT INTO file_info (path, type, size, file_name, extension, text)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(sql, data)

def read_file_content(file_path):
    with open(file_path, 'r', encoding='latin-1') as file:
        return file.read()

def disable_foreign_key_check(cursor):
    cursor.execute("SET FOREIGN_KEY_CHECKS=0")

def enable_foreign_key_check(cursor):
    cursor.execute("SET FOREIGN_KEY_CHECKS=1")

def drop_table(cursor, table_name):
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

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

        # Disabilita il controllo delle chiavi esterne
        disable_foreign_key_check(cursor)

        # Elimina la tabella se esiste
        drop_table(cursor, "file_info")

        # Crea la tabella combinata
        create_combined_table(cursor)

        # Riabilita il controllo delle chiavi esterne
        enable_foreign_key_check(cursor)

        # Commit delle modifiche
        connection.commit()
        print("Tabella 'file_info' creata correttamente")

except mysql.connector.Error as e:
    print("Errore durante la connessione al server MySQL:", e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()

# Connessione al database MySQL
try:
    connection = connect_to_db("dcrb")

    if connection.is_connected():
        cursor = connection.cursor()
        print("Connessione al database MySQL riuscita")

        # Directory radice da analizzare
        root_directory = r'C:\xampp\htdocs\DCRB'

        # Ottieni le informazioni su cartelle, sottocartelle e file
        data = list_files_and_folders(root_directory)

        # Popola la tabella file_info con i dati raccolti in batch di 10 elementi
        batch_size = 10
        for i in range(0, len(data), batch_size):
            insert_data(cursor, data[i:i + batch_size])
            connection.commit()  # Commit ogni 10 elementi

        # Commit finale per eventuali rimanenti
        connection.commit()

        # Chiusura della connessione
        cursor.close()
        connection.close()
        print("Dati inseriti correttamente nel database")

except mysql.connector.Error as e:
    print("Errore durante la connessione al database MySQL:", e)
