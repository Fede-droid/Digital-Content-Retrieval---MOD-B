import mysql.connector

def search_word_in_files(word):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Fedemysql99",
            database="dcrb"
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Query per cercare la parola nei testi dei file
            text_query = """
                SELECT file_info.file_name, file_info.extension, file_info.id, file_info.path,
                       LENGTH(secondary.text) - LENGTH(REPLACE(secondary.text, %s, '')) AS text_word_count
                FROM secondary
                INNER JOIN file_info ON secondary.file_id = file_info.id
                WHERE secondary.text LIKE %s
            """
            search_word = '%' + word + '%'
            cursor.execute(text_query, (word, search_word))

            text_results = cursor.fetchall()

            # Query per cercare la parola nei nomi dei file e nei percorsi
            name_query = """
                SELECT file_name, path
                FROM file_info
                WHERE file_name LIKE %s OR path LIKE %s
            """
            name_search_word = '%' + word + '%'
            cursor.execute(name_query, (name_search_word, name_search_word))

            name_results = cursor.fetchall()

            if text_results:
                print("Risultati della ricerca per '{}':".format(word))
                for result in text_results:
                    print("Nome file:", result[0] + result[1])  # Concatena nome del file ed estensione
                    print("Percorso:", result[3])  # Stampa il percorso del file
                    print("ID file:", result[2])
                    print("Numero di occorrenze della parola nel testo del file:", result[4])
                    print("-" * 50)
                print("Numero di occorrenze della parola come nome di file o cartella:", len(name_results))
                print("Dettagli dei file e delle cartelle corrispondenti:")
                for name_result in name_results:
                    print("Nome file/cartella:", name_result[0])
                    print("Percorso:", name_result[1])
                    print("-" * 50)
            else:
                print("Nessun risultato trovato per '{}'.\n".format(word))

    except mysql.connector.Error as e:
        print("Errore durante la connessione al database MySQL:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connessione al database chiusa.")

# Esegui la funzione di ricerca
parola_da_cercare = input("Inserisci la parola da cercare nei file: ")
search_word_in_files(parola_da_cercare)
