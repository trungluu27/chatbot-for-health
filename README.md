# Chatbot-for-health

This project is an end-to-end Retrieval-Augmented Generation (RAG) chatbot designed for Vietnamese users. It leverages health-related data to provide accurate and relevant responses.

## Prerequisites
Before running the app.py file, please ensure the following steps are completed:

1. Download the llm 
    Create folder models. Then download model vinallama-7b-chat-GGUF from https://huggingface.co/vilm/vinallama-7b-chat-GGUF and save it in the folder models
2. Set Up the Environment Variables
    Create file .env and type your Hugging Face API token as shown below:

```bash
HUGGINGFACEHUB_API_TOKEN = 'your_api_token'
```
3. Download libraries

```bash
pip install -r requirements.txt
```