import os
import re
from bs4 import BeautifulSoup
from collections import defaultdict, OrderedDict
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

def spimi_invert(token_stream, block_size_limit):
    block = OrderedDict()
    current_block_size = 0
    
    for token, doc_id in token_stream:
        if token not in block:
            block[token] = []
        if doc_id not in block[token]:
            block[token].append(doc_id)
            current_block_size += 1
        
        if current_block_size >= block_size_limit:
            yield block
            block = OrderedDict()
            current_block_size = 0
    
    if block:
        yield block

def scan_and_extract_tokens_and_paths(path):
    file_paths = {}
    token_stream = []
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
                # Aggiungi al token stream
                for token in tokens:
                    token_stream.append((token, file_id))
    return token_stream, file_paths

def merge_blocks(blocks):
    merged_index = defaultdict(list)
    for block in blocks:
        for token, doc_ids in block.items():
            merged_index[token].extend(doc_ids)
            merged_index[token] = list(set(merged_index[token]))
    return merged_index

def build_spimi_index(path, block_size_limit):
    token_stream, file_paths = scan_and_extract_tokens_and_paths(path)
    blocks = list(spimi_invert(token_stream, block_size_limit))
    merged_index = merge_blocks(blocks)
    return merged_index, file_paths

# Percorso da scansionare
path_to_scan = r"D:\Downloaded Web Sites\DCRB-PT2"
block_size_limit = 10000  # Limite della dimensione del blocco

# Costruisci l'indice utilizzando SPIMI
spimi_index, file_paths = build_spimi_index(path_to_scan, block_size_limit)

# Salva l'indice SPIMI e il dizionario dei percorsi dei file in file utilizzando pickle
with open('spimi_index_DCRB-PT2.pkl', 'wb') as file:
    pickle.dump(spimi_index, file)

with open('file_path_puntoB_DCRB-PT2.pkl', 'wb') as file:
    pickle.dump(file_paths, file)

# Visualizza parte dell'indice SPIMI per verifica
for token in list(spimi_index.keys())[:10]:  # Mostra i primi 10 token
    print(f"{token}: {spimi_index[token]}")
