import os
import mysql.connector

def list_files_and_folders(root_dir):
    data = []
    for root, dirs, files in os.walk(root_dir):
        for directory in dirs:
            folder_path = os.path.join(root, directory)
            data.append([folder_path, "Folder", None, None, None])  # Aggiungi None come valore per l'estensione e il nome del file
        for file in files:
            file_path = os.path.join(root, file)
            size = os.path.getsize(file_path)
            file_name, file_extension = os.path.splitext(file)
            data.append([file_path, "File", size, file_name, file_extension])  # Aggiungi il nome del file e l'estensione
    return data

def create_table(cursor):
    cursor.execute("DROP TABLE IF EXISTS file_info")  # Elimina la tabella se esiste già
    cursor.execute("CREATE TABLE file_info (id INT AUTO_INCREMENT PRIMARY KEY, path VARCHAR(255), type VARCHAR(10), size BIGINT, file_name VARCHAR(255), extension VARCHAR(10))")

def create_secondary_table(cursor):
    cursor.execute("DROP TABLE IF EXISTS secondary")  # Elimina la tabella se esiste già
    cursor.execute("CREATE TABLE secondary (file_id INT, text LONGTEXT, FOREIGN KEY (file_id) REFERENCES file_info(id))")

def insert_data(cursor, data):
    sql = "INSERT INTO file_info (path, type, size, file_name, extension) VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(sql, data)

def read_file_content(file_path):
    with open(file_path, 'r', encoding='latin-1') as file:
        return file.read()

def disable_foreign_key_check(cursor):
    cursor.execute("SET FOREIGN_KEY_CHECKS=0")

def enable_foreign_key_check(cursor):
    cursor.execute("SET FOREIGN_KEY_CHECKS=1")

def drop_table(cursor, table_name):
    cursor.execute("DROP TABLE IF EXISTS {}".format(table_name))

# Connessione al database MySQL
try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Fedemysql99",
        database="dcr"
    )

    if connection.is_connected():
        cursor = connection.cursor()
        print("Connessione al database MySQL riuscita")

        # Disabilita il controllo delle chiavi esterne
        disable_foreign_key_check(cursor)

        # Elimina le righe dalla tabella 'secondary' che fanno riferimento a 'file_info'
        cursor.execute("DELETE FROM secondary WHERE file_id IN (SELECT id FROM file_info)")

        # Elimina la tabella 'file_info'
        drop_table(cursor, "file_info")

        # Riabilita il controllo delle chiavi esterne
        enable_foreign_key_check(cursor)

        # Commit delle modifiche e chiusura della connessione
        connection.commit()
        cursor.close()
        connection.close()
        print("Tabella 'file_info' eliminata correttamente")

except mysql.connector.Error as e:
    print("Errore durante la connessione al database MySQL:", e)


# Connessione al database MySQL
try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Fedemysql99",
        database="dcr"
    )

    if connection.is_connected():
        cursor = connection.cursor()
        print("Connessione al database MySQL riuscita")

        # Directory radice da analizzare
        root_directory = r'C:\xampp\htdocs\DCRB'

        # Ottieni le informazioni su cartelle, sottocartelle e file
        data = list_files_and_folders(root_directory)

        # Crea la tabella file_info nel database
        create_table(cursor)

        # Popola la tabella file_info con i dati raccolti
        insert_data(cursor, data)

        # Crea la tabella secondary nel database
        create_secondary_table(cursor)

        # Popola la colonna text con il contenuto dei file
        for row in data:
            if row[1] == 'File':
                file_content = read_file_content(row[0])
                cursor.execute("INSERT INTO secondary (file_id, text) VALUES ((SELECT id FROM file_info WHERE path = %s), %s)", (row[0], file_content))

        # Commit delle modifiche e chiusura della connessione
        connection.commit()
        cursor.close()
        connection.close()
        print("Dati inseriti correttamente nel database")

except mysql.connector.Error as e:
    print("Errore durante la connessione al database MySQL:", e)
