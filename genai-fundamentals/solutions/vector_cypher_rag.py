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
from neo4j_graphrag.retrievers import VectorCypherRetriever

retrieval_query = """
MATCH (node)<-[r:RATED]-()
RETURN 
  node.title AS title, node.plot AS plot, score AS similarityScore, 
  collect { MATCH (node)-[:IN_GENRE]->(g) RETURN g.name } as genres, 
  collect { MATCH (node)<-[:ACTED_IN]->(a) RETURN a.name } as actors, 
  avg(r.rating) as userRating
ORDER BY userRating DESC
"""

retriever = VectorCypherRetriever(
    driver,
    index_name="moviePlots",
    embedder=embedder,
    retrieval_query=retrieval_query,
)
# end::retriever[]

# tag::graphrag[]
from neo4j_graphrag.generation import GraphRAG
from neo4j_graphrag.llm import OpenAILLM

# llm = OpenAILLM(model_name="gpt-4o", model_params={"temperature": 0})
llm = OpenAILLM(model_name="gpt-4o")
rag = GraphRAG(
    retriever=retriever, 
    llm=llm
    )

query_text = "Find an action film about travelling to other planets"
response = rag.search(
    query_text=query_text, 
    retriever_config={"top_k": 5}, 
    return_context=True
    )

print(response.answer)
print(response.retriever_result.items)

# end::graphrag[]


driver.close()