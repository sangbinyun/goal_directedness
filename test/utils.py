# util.py
import os, getpass
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
import ollama
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
import json

def set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

def load_llm(model: str):
    if model == 'openai':
        llm = ChatOpenAI(
            model = "gpt-3.5-turbo", # "gpt-4o", "gpt-4", "gpt-3.5-turbo", "gpt-3.5", "gpt-3", "gpt-2", "gpt-1"
            temperature = 0
        )

    elif model == 'ollama':
        llm = ChatOllama(
            model = 'llama3.2:3b-instruct-fp16',
            base_url = "http://localhost:11434",
            temperature = 0,
            verbose = True
        )
        
    return llm

def return_possible_models():
    # Get the list of available models
    models = [i['model'] for i in ollama.list()['models']]
    print(models)

def connect_to_sql_memory(ExperimentName: str):
    db_path = f"state_db/{ExperimentName}.db"
    conn = sqlite3.connect(db_path, check_same_thread = False)

    # checkpointer 
    memory = SqliteSaver(conn)

    return memory

