import json
import os
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

data_path = 'data/processed_data.json'
# data_path = 'data/a.txt'
vector_db_path = 'vector_db/'
embedding_model = "sentence-transformers/all-MiniLM-L6-v2"

def create_db(persist_directory):
    if not os.path.exists(persist_directory):
        os.makedirs(persist_directory)

    with open(data_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    data = [dt['segmented_text'] for dt in data]

    embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
    db = FAISS.from_texts(data, embeddings)
    db.save_local(persist_directory)
    return db

def load_db(persist_directory):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_db = FAISS.load_local(persist_directory, embeddings, allow_dangerous_deserialization=True)
    return vector_db

create_db(vector_db_path)