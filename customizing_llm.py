import os
import openai
from llama_index import LLMPredictor, VectorStoreIndex, ServiceContext, SimpleDirectoryReader
from langchain import OpenAI

openai.api_key = os.getenv("OPENAI_API_KEY")

def query_custom_llm(prompt):
    documents =  SimpleDirectoryReader('data').load_data()
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003"))
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
    index = VectorStoreIndex.from_documents(documents, service_context=service_context)
    query_engine = index.as_query_engine()
    return query_engine.query(prompt)

print(query_custom_llm("Who is the president of USA?"))
