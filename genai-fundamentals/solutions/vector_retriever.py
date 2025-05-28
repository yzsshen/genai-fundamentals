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

# tag::search[]
result = retriever.search(query_text="Toys come alive", top_k=5)

for item in result.items:
    print(item.content, item.metadata["score"])
# end::search[]

driver.close()