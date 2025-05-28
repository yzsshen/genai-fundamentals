import os
from dotenv import load_dotenv
load_dotenv()

# tag::setup[]
from neo4j import GraphDatabase

# Demo database credentials
uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")
driver = GraphDatabase.driver(uri, auth=(username, password))

# end::setup[]

# tag::retriever[]
from neo4j_graphrag.retrievers import Text2CypherRetriever
from neo4j_graphrag.llm import OpenAILLM

# Create LLM object
t2c_llm = OpenAILLM(model_name="gpt-4o")

# (Optional) Specify your own Neo4j schema
neo4j_schema = """
Node properties:
Person {name: STRING, born: INTEGER}
Movie {tagline: STRING, title: STRING, released: INTEGER}
Genre {name: STRING}
User {name: STRING}

Relationship properties:
ACTED_IN {role: STRING}
RATED {rating: INTEGER}

The relationships:
(:Person)-[:ACTED_IN]->(:Movie)
(:Person)-[:DIRECTED]->(:Movie)
(:User)-[:RATED]->(:Movie)
(:Movie)-[:IN_GENRE]->(:Genre)
"""

# Provide user input/query pairs for the LLM to use as examples
examples = [
    "USER INPUT: 'Get user ratings for the movie Toy Story?' QUERY: MATCH (u:User)-[r:RATED]->(m:Movie) WHERE m.title = 'Toy Story' RETURN r.rating"
]

# Build the retriever
retriever = Text2CypherRetriever(
    driver=driver,
    llm=t2c_llm,
    neo4j_schema=neo4j_schema,
    examples=examples,
)
# end::retriever[]

# tag::search[]
# result = retriever.search(query_text="What is the averaging user rating for the movie Toy Story?")

# for item in result.items:
#     print(item.content)
# end::search[]

# tag::graphrag[]
from neo4j_graphrag.generation import GraphRAG

llm = OpenAILLM(model_name="gpt-4o", model_params={"temperature": 0})
rag = GraphRAG(retriever=retriever, llm=llm)

# query_text = "Which movies did Hugo Weaving star in?"
query_text = "What is the highest rating for Goodfellas?"
response = rag.search(
    query_text=query_text,
    return_context=True
    )
print(response.answer)
print(response.retriever_result.items)
print(response.retriever_result.metadata["cypher"])
# end::graphrag[]
driver.close()
