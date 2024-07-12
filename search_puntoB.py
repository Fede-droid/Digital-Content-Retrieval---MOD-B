import pickle

def load_spimi_index(index_file, paths_file):
    with open(index_file, 'rb') as f:
        spimi_index = pickle.load(f)
    
    with open(paths_file, 'rb') as f:
        file_paths = pickle.load(f)
    
    return spimi_index, file_paths

def search_term(spimi_index, file_paths, term):
    term = term.lower()
    if term in spimi_index:
        file_ids = spimi_index[term]
        return [file_paths[file_id] for file_id in file_ids]
    else:
        return []

def main():
    index_file = 'spimi_index_DCRB-PT2.pkl'
    paths_file = 'file_path_puntoB_DCRB-PT2.pkl'
    
    # Carica l'indice SPIMI e i percorsi dei file
    spimi_index, file_paths = load_spimi_index(index_file, paths_file)
    
    # Termine da cercare
    term = input("Inserisci il termine da cercare: ")
    
    # Cerca il termine nell'indice
    result_paths = search_term(spimi_index, file_paths, term)
    
    if result_paths:
        print(f"Il termine '{term}' è presente nei seguenti file:")
        for path in result_paths:
            print(path)
    else:
        print(f"Il termine '{term}' non è stato trovato in nessun file.")

if __name__ == "__main__":
    main()






"""import pickle

def load_spimi_index(index_file, paths_file):
    with open(index_file, 'rb') as f:
        spimi_index = pickle.load(f)
    
    with open(paths_file, 'rb') as f:
        file_paths = pickle.load(f)
    
    return spimi_index, file_paths

def search_term(spimi_index, term):
    term = term.lower()
    if term in spimi_index:
        file_ids = spimi_index[term]
        return file_ids
    else:
        return []

def main():
    index_file = 'spimi_index.pkl'
    paths_file = 'file_path_puntoB.pkl'
    
    # Carica l'indice SPIMI e i percorsi dei file
    spimi_index, file_paths = load_spimi_index(index_file, paths_file)
    
    # Termine da cercare
    term = input("Inserisci il termine da cercare: ")
    
    # Cerca il termine nell'indice
    result_file_ids = search_term(spimi_index, term)
    
    if result_file_ids:
        print(f"Il termine '{term}' è presente nei seguenti file ID:")
        for file_id in result_file_ids:
            print(file_id)
    else:
        print(f"Il termine '{term}' non è stato trovato in nessun file.")

if __name__ == "__main__":
    main()
"""