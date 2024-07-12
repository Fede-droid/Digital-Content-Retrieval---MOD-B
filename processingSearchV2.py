import pickle
from processingV2 import binary_tree

# Carica l'albero binario da un file pickle
with open('binaryTreeDCRB-PT2.pkl', 'rb') as file:
    binary_tree = pickle.load(file)

# Carica il dizionario che mappa gli ID dei file ai loro percorsi
with open('pathDCRB-PT2.pkl', 'rb') as file:
    file_paths = pickle.load(file)

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

# Esempio di utilizzo della funzione search_token per cercare un token
token_to_search = "yoda"
result = search_token(binary_tree.root, token_to_search)
if result:
    paths = get_file_paths(result)
    print(f"I file IDs associati al token '{token_to_search}' sono:")
    for file_id, path in paths.items():
        print(f"{file_id} -> {path}")
else:
    print(f"Il token '{token_to_search}' non è presente nell'albero binario.")
