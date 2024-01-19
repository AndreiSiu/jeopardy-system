import os
from whoosh.fields import Schema, TEXT
from whoosh.index import create_in
from tqdm import tqdm
import spacy

# Define the schema
schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True))

# Create the index
index_path = "./improved_indexer/Index_test"
if not os.path.exists(index_path):
    os.mkdir(index_path)
index = create_in(index_path, schema)

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Function to process text using spaCy
def process_text(text):
    doc = nlp(text)
    return " ".join(token.lemma_ for token in doc if not token.is_stop)

# Function to extract Wikipedia pages from a file
def extract_pages(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        # Extract titles and content from pages
        start_index = 0
        while True:
            title_start = content.find("[[", start_index)
            if title_start == -1:
                break
            title_end = content.find("]]", title_start + 2)
            if title_end == -1:
                break
            title = content[title_start + 2:title_end].strip()
            start_index = title_end + 2
            content_start = start_index
            content_end = content.find("[[", content_start)
            if content_end == -1:
                page_content = content[content_start:].strip()
                start_index = len(content)
            else:
                page_content = content[content_start:content_end].strip()
                start_index = content_end
            yield title, page_content

# Iterate through files in the "Dataset" folder
dataset_folder = "../DataSets/wikipediaPages"
file_list = [f for f in os.scandir(dataset_folder) if f.is_file()]
commit_interval = 5
writer = index.writer()

for idx, file_entry in enumerate(tqdm(file_list, desc="Indexing Progress", dynamic_ncols=True)):
    file_name = file_entry.name
    file_path = file_entry.path
    tqdm.write(f"Processing: {file_name}")
    # Iterate through Wikipedia pages in the file
    for title, content in extract_pages(file_path):
        # Process content using spaCy
        processed_content = process_text(content)
        # Add each page to the index
        writer.add_document(title=title, content=processed_content)

    # Commit in batches
    if (idx + 1) % commit_interval == 0:
        tqdm.write("Committing changes...")
        writer.commit()
        writer = index.writer()

# Final commit and close the writer
tqdm.write("Final commit and closing the writer...")
writer.commit()
