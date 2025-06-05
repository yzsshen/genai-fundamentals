import os
from dotenv import load_dotenv
load_dotenv()

from neo4j import GraphDatabase

# Connect to Neo4j database
driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"), 
    auth=(
        os.getenv("NEO4J_USERNAME"), 
        os.getenv("NEO4J_PASSWORD")
    )
)

# Create embedder

# Create retriever

# Search for similar items

# Parse results

# CLose the database connection
driver.close()
