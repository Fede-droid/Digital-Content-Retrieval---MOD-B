#!/usr/bin/python3

import os
import nltk
from bs4 import BeautifulSoup
import re

def read_data_from_directory(directory_path, MAX_BATCH_SIZE):
    out = []
    with open("docs.txt", "w+", encoding='utf-8') as fout:

        file_paths = []
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith(".html") and len(file_paths) < MAX_BATCH_SIZE:
                    file_paths.append(os.path.join(root, file))

                if len(file_paths) == MAX_BATCH_SIZE:
                    for file_path in file_paths:
                        file_id = os.path.splitext(os.path.basename(file_path))[0]
                        with open(file_path, 'r', encoding='latin-1') as file:
                            content = file.read()
                        out.append((file_id, clean_html_reverse_posting_lists(content)))
                    for record in out:
                        fout.write("%s\t%s\n" % (record[0], record[1]))
                    file_paths = []
                    out = []

        # Process any remaining files
        if file_paths:
            for file_path in file_paths:
                file_id = os.path.splitext(os.path.basename(file_path))[0]
                with open(file_path, 'r', encoding='latin-1') as file:
                    content = file.read()
                out.append((file_id, clean_html_reverse_posting_lists(content)))

            for record in out:
                fout.write("%s\t%s\n" % (record[0], record[1]))

def create_postlist(filename_in, filename_out, stopwords, stem):
    fstem = open(stem, "a", encoding='utf-8')
    fout = open(filename_out, "w", encoding='utf-8')
    fsw = open(stopwords, "r", encoding='utf-8')
    stopwords_list = fsw.read()
    pl = {}
    with open(filename_in, "r", encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            line = line.split('\t')
            key = line[0]
            words = line[1].split(" ")
            words = [w for w in words if (len(w) > 3 and w not in stopwords_list)]    
            for word in words:
                word = word.lower()
                try:
                    pl[word].add(key)
                except Exception as e:
                    pl[word] = set()
                    pl[word].add(key)
    for word in pl:
        fout.write(word + "\n")
        for id in sorted(pl[word]):
            fout.write(id + "\n")        

def clean_html_reverse_posting_lists(html_string):
    remove_list = "$,./\\\"*+-€&!?ì^=)(%£@ç°#§:;)"
    pattern_latex = r'\\[a-zA-Z]+\{[^}]*\}|\[[^\]]*\]|\\[a-zA-Z]+'
    pattern_numbers = r'\d+'

    soup = BeautifulSoup(html_string, "html.parser")
    raw = soup.get_text()
    clean_text = raw.strip()  
    
    clean_text = re.sub(pattern_latex, '', clean_text)
    
    for char in remove_list:
        clean_text = clean_text.replace(char, " ")
    
    clean_text = re.sub(r'[^a-zA-Z0-9\s]', ' ', clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    
    clean_text = re.sub(pattern_numbers, '', clean_text)
    return clean_text

# Esegui la funzione di ricerca
directory_path = input("Inserisci il percorso della directory da scansionare: ")
read_data_from_directory(directory_path, 10)
#create_postlist("docs.txt", "postings.txt", "stopwords.txt")
