import pickle
from nltk.corpus import wordnet
import nltk

nltk.download('wordnet')

from processingV2 import binary_tree

# Carica l'albero binario da un file pickle
with open('binaryTreeDCRB-PT2.pkl', 'rb') as file:
    binary_tree = pickle.load(file)

# Carica il dizionario che mappa gli ID dei file ai loro percorsi
with open('pathDCRB-PT2.pkl', 'rb') as file:
    file_paths = pickle.load(file)

# Funzione per ottenere i sinonimi di una parola utilizzando WordNet
def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().lower())
    return synonyms

# Funzione per cercare un token nell'albero binario con debug
def search_token(node, token):
    steps = []  # Lista per tracciare i passaggi
    while node:
        steps.append(f"Comparing {token} with {node.key}")
        if token == node.key:
            steps.append(f"Token found: {node.key}")
            print("\n".join(steps))  # Stampa tutti i passaggi
            return node.file_ids
        elif token < node.key:
            steps.append(f"Going left from {node.key}")
            node = node.left
        else:
            steps.append(f"Going right from {node.key}")
            node = node.right
    steps.append("Token not found")
    print("\n".join(steps))  # Stampa tutti i passaggi
    return None

# Funzione per ottenere i percorsi dei file dagli ID dei file
def get_file_paths(file_ids):
    return {file_id: file_paths[file_id] for file_id in file_ids if file_id in file_paths}

def main():
    token_to_search = "car"
    synonyms = get_synonyms(token_to_search)

    # Stampa i sinonimi trovati
    print(f"I sinonimi del token '{token_to_search}' sono: {synonyms}")

    # Inizializza un set per raccogliere tutti i file IDs trovati
    all_file_ids = set()

    # Cerca il token originale e i suoi sinonimi
    for token in synonyms:
        result = search_token(binary_tree.root, token)
        if result:
            all_file_ids.update(result)

    if all_file_ids:
        paths = get_file_paths(all_file_ids)
        print(f"I file IDs associati al token '{token_to_search}' e ai suoi sinonimi sono:")
        for file_id, path in paths.items():
            print(f"{file_id} -> {path}")
    else:
        print(f"Il token '{token_to_search}' e i suoi sinonimi non sono presenti nell'albero binario.")


if __name__ == "__main__":
    main()

