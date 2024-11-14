# util.py
def load_llm(model: str):
    if model == 'openai':
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(
            model = "gpt-3.5-turbo", # "gpt-4o", "gpt-4", "gpt-3.5-turbo", "gpt-3.5", "gpt-3", "gpt-2", "gpt-1"
            temperature = 0
        )
    elif model == 'ollama':
        from langchain_ollama import ChatOllama
        llm = ChatOllama(
            model = 'llama3.2:3b-instruct-fp16',
            base_url = "http://localhost:11434",
            temperature = 0,
            verbose = True
        )
    return llm

def return_possible_models():
    import ollama

    # Get the list of available models
    models = [i['model'] for i in ollama.list()['models']]
    print(models)

def connect_to_sql_memory(ExperimentName: str):
    import sqlite3
    from langgraph.checkpoint.sqlite import SqliteSaver

    db_path = f"state_db/{ExperimentName}.db"
    conn = sqlite3.connect(db_path, check_same_thread=True)

    # checkpointer 
    memory = SqliteSaver(conn)

    return memory