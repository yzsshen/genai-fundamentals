import os
from dotenv import load_dotenv
load_dotenv()

from neo4j import GraphDatabase
uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")
driver = GraphDatabase.driver(uri, auth=(username, password))

# tag::embedder[]
from neo4j_graphrag.embeddings.openai import OpenAIEmbeddings

embedder = OpenAIEmbeddings(model="text-embedding-ada-002")
# end::embedder[]

# tag::retriever[]
from neo4j_graphrag.retrievers import VectorRetriever

retriever = VectorRetriever(
    driver,
    index_name="moviePlots",
    embedder=embedder,
    return_properties=["title", "plot"],
)
# end::retriever[]

# tag::graphrag[]
from neo4j_graphrag.generation import GraphRAG
from neo4j_graphrag.llm import OpenAILLM

# llm = OpenAILLM(model_name="gpt-4o", model_params={"temperature": 0})
llm = OpenAILLM(model_name="gpt-4o")
rag = GraphRAG(retriever=retriever, llm=llm)
query_text = "Give me 3 films about toys coming alive"
response = rag.search(query_text=query_text, retriever_config={"top_k": 5})
print(response.answer)
# end::graphrag[]


driver.close()