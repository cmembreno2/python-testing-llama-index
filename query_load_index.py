import os
import openai
from llama_index import StorageContext, load_index_from_storage



openai.api_key = os.getenv("OPENAI_API_KEY")

def query(prompt):
    storage_context = StorageContext.from_defaults(persist_dir='index')
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()
    return query_engine.query(prompt)

print(query("What are the most important aspects of paul life?"))
