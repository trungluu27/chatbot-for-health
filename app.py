from flask import Flask, request, jsonify, render_template
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from src.helper import download_hugging_face_embeddings
from src.prompt import *
import os


app = Flask(__name__)

load_dotenv()

HUGGINGFACEHUB_API_TOKEN = os.environ.get("HUGGINGFACEHUB_API_TOKEN")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN

embeddings = download_hugging_face_embeddings()

vector_db_path = 'vector_db/db_faiss'

model_file = 'models/vinallama-7b-chat_q5_0.gguf'

def load_model(model_file):
    llm = CTransformers(
        model=model_file,
        model_type="llama",
        max_new_tokens=1024,
        temperature=0.01
    )
    return llm

def creart_prompt(template):
    prompt = PromptTemplate(template=template, input_variables=['context', 'question'])
    return prompt

def create_qa_chain(prompt, llm, db):
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(search_kwargs={"k":2}),
        chain_type_kwargs={"prompt": prompt}
    )
    return qa_chain

def read_vector_db():
    db = FAISS.load_local(vector_db_path, embeddings, allow_dangerous_deserialization=True)
    return db

llm = load_model(model_file)
prompt = creart_prompt(template)
db = read_vector_db()
llm_chain = create_qa_chain(prompt, llm, db)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatbot', methods=['GET', 'POST'])
def chat():
    msg = request.form['msg']
    input = msg
    print(input)
    response = llm_chain.invoke({'query': input})
    print('Response:', response['result'])
    return str(response['result'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
    