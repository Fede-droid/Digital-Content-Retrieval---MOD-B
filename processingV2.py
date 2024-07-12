import os
import re
from bs4 import BeautifulSoup
from collections import defaultdict
import nltk
from nltk.corpus import stopwords
import pickle

# Assicurati di aver scaricato le stopword di NLTK
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def tokenize(text):
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    tokens = text.lower().split()
    tokens = [token for token in tokens if token not in stop_words]
    return tokens

def extract_tokens_from_html(html_document):
    soup = BeautifulSoup(html_document, "html.parser")
    raw_text = soup.get_text(" ")
    tokens = tokenize(raw_text)
    return tokens

def scan_and_extract_tokens_and_paths(path):
    token_dict = defaultdict(list)
    file_paths = {}
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                # Leggi il contenuto del file
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Estrai i token dal contenuto del file
                tokens = extract_tokens_from_html(content)
                file_id = os.stat(file_path, follow_symlinks=False).st_ino  # Usa l'ID del file
                file_paths[file_id] = file_path
                # Aggiungi i file ID al dizionario per ciascun token
                for token in tokens:
                    if file_id not in token_dict[token]:
                        token_dict[token].append(file_id)
    return token_dict, file_paths

class TreeNode:
    def __init__(self, key, file_ids=None):
        self.key = key
        self.file_ids = file_ids if file_ids is not None else []
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None
    
    def insert(self, key, file_ids):
        if self.root is None:
            self.root = TreeNode(key, file_ids)
        else:
            self._insert(self.root, key, file_ids)
    
    def _insert(self, node, key, file_ids):
        if key < node.key:
            if node.left is None:
                node.left = TreeNode(key, file_ids)
            else:
                self._insert(node.left, key, file_ids)
        elif key > node.key:
            if node.right is None:
                node.right = TreeNode(key, file_ids)
            else:
                self._insert(node.right, key, file_ids)
        else:
            # Se il token già esiste, aggiorna la lista dei file IDs
            node.file_ids.extend(file_ids)

    def _print_ascii_tree(self, node, prefix="", is_left=True):
        ascii_tree = ""
        if not node:
            ascii_tree += (prefix + ("└── " if is_left else "┌── ") + "Vuoto\n")
            return ascii_tree

        if node.right:
            ascii_tree += self._print_ascii_tree(node.right, prefix + ("│   " if is_left else "    "), False)
        ascii_tree += (prefix + ("└── " if is_left else "┌── ") + f"{node.key}: {node.file_ids}\n")
        if node.left:
            ascii_tree += self._print_ascii_tree(node.left, prefix + ("    " if is_left else "│   "), True)

        return ascii_tree

    def print_ascii_tree(self):
        return self._print_ascii_tree(self.root)

# Percorso da scansionare
path_to_scan = r"D:\Downloaded Web Sites\food"
token_dictionary, file_paths = scan_and_extract_tokens_and_paths(path_to_scan)

# Creazione dell'albero binario dai token del dizionario
binary_tree = BinaryTree()
for token, file_ids in token_dictionary.items():
    binary_tree.insert(token, file_ids)

# Salva la rappresentazione ASCII dell'albero su un file
with open('V2outputTree.txt', 'w', encoding='utf-8') as f:
    f.write(binary_tree.print_ascii_tree())

# Salva l'albero binario popolato in un file utilizzando pickle
with open('binary_treeV2.pkl', 'wb') as file:
    pickle.dump(binary_tree, file)

# Salva il dizionario che mappa gli ID dei file ai loro percorsi in un file utilizzando pickle
with open('file_pathV2.pkl', 'wb') as file:
    pickle.dump(file_paths, file)
