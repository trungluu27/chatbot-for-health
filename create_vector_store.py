from src.helper import load_pdf_file, text_split, download_hugging_face_embeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

load_dotenv()

HUGGINGFACEHUB_API_TOKEN = os.environ.get("HUGGINGFACEHUB_API_TOKEN")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN

extracted_data=load_pdf_file(data='data/')
text_chunks=text_split(extracted_data)
embeddings = download_hugging_face_embeddings()

vector_db_path = 'vector_db/db_faiss'

def create_db():
    db = FAISS.from_documents(text_chunks, embeddings)
    db.save_local(vector_db_path)
    return db

create_db()

