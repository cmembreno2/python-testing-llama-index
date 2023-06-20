import os
import openai
from llama_index import VectorStoreIndex, SimpleDirectoryReader

openai.api_key = os.getenv("OPENAI_API_KEY")

def query(prompt):

    documents =  SimpleDirectoryReader('data').load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir='index')
    query_engine = index.as_query_engine()
    response = query_engine.query(prompt)

    results = {"response": response.response, "sources": response.source_nodes, "formated_sources": response.get_formatted_sources()}

    return results

print(query("What are the most important aspects of paul life?"))
