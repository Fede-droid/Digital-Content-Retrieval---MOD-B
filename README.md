# DCR -modB - pt1
## Project Description
This project focuses on developing a search function for a specific subtree within a local file system. The main objective was to create a function that accepts a string of characters and finds matches in file names, folder names, or within file content itself.

## Tools Used
- MySQL Workbench
- Visual Studio Code
- GitHub
- LucidChart
- Wikipedia
- Windows 11 Pro

## Project Specifications
The project involves searching within a subtree with a minimum depth of six levels, containing a subtree named "DCRB" with a minimum depth of four levels and at least fifty files distributed over at least four levels.

## Project Implementation
A Python script was developed to scan a directory, gather information about files and folders, and store them in a MySQL database. Key operations of the script include:
- Creating database tables
- Inserting collected data
- Reading file contents

The search function returns key information such as the file name containing the input string, the full file path, the file ID, and the number of occurrences of the word in the file text. Indexes were used to improve search speed and efficiency.

## Conclusions
The project required meticulous planning and execution to ensure compliance with all specified requirements. The result is a robust and efficient search function for the local file system.

# DCR -modB - pt2
## Introduction
This report covers the second part of the Digital Content Retrieval project - mod B. I studied and implemented a retrieval system using a tree structure containing approximately 10,000 files on my computer. After implementing the system, I further developed the project based on two requests chosen from a list of options.

## Tools Used
- Visual Studio Code
- Wikipedia (Minecraft Wiki, Wookiepedia)
- Windows 11 Pro

## Intermediate Steps
1. **File Download**
   - I downloaded datasets from Wikipedia, specifically Minecraft Wiki and Star Wars Wiki, using Cyotek WebCopy to obtain a substantial number of files.
   - I then wrote a Python script to filter out only useful HTML files.

2. **HTML File Cleaning**
   - I created a Python script with Beautiful Soup to remove unnecessary elements from HTML files, retaining only relevant text.
   - This step improves the accuracy and efficiency of the retrieval system by reducing noise in the data.

3. **Stop Words Removal**
   - I used the NLTK library to remove stop words from texts, optimizing storage space and improving indexing speed and result accuracy.

## Retrieval System
- I studied and implemented a retrieval system by creating an indexing function and a search function.
- The indexing function creates an inverted index and stores it as a file, while the search function allows searching for terms in the inverted index, returning a list of documents containing the term.

## Group A Features
- I extended the search function to include synonyms of search terms using WordNet, improving vocabulary coverage and reducing the risk of failed queries.

## Group B Features
- I extended the indexing function using the Single Pass In Memory (SPIMI) algorithm, enhancing performance and memory usage during index creation.

## Data Structure Comparison
- I compared search performance using two different data structures: a binary tree and a dictionary created with the SPIMI algorithm.
- I concluded that the dictionary is more efficient in terms of search time and memory usage.

# Conclusion
The project took approximately one week, including study, code development, and bug resolution. I enjoyed the challenge and gained an understanding of the importance of indexes and search algorithms in improving information retrieval system performance.
