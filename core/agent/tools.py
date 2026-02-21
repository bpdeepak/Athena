from langchain_core.tools import tool
import os
import httpx
import logging
from neo4j import GraphDatabase

logger = logging.getLogger(__name__)

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://graph-db:7687")
NEO4J_USER = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

SIM_API_URL = os.getenv("SIM_API_URL", "http://sim-api:8001")

@tool
def query_graph_database(cypher_query: str) -> str:
    """Queries the Neo4j Knowledge Graph. Use this to find relationships between Tasks, Epics, Users, and Risks."""
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        with driver.session() as session:
            result = session.run(cypher_query)
            records = [record.data() for record in result]
        driver.close()
        return str(records)
    except Exception as e:
        logger.error(f"Graph query failed: {e}")
        return f"Error querying graph: {e}"

@tool
def search_vector_database(query: str) -> str:
    """Performs semantic search on ChromaDB. Use this to find unstructured context from descriptions and titles."""
    import chromadb
    from chromadb.config import Settings
    from llm_provider import get_llm_provider
    try:
        CHROMA_HOST = os.getenv("CHROMA_HOST", "vector-db")
        CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8002"))
        client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT, settings=Settings(allow_reset=True))
        
        provider = get_llm_provider()
        embeddings = provider.get_embeddings()
        
        class LangchainEmbeddingFunc:
            def __init__(self, lc_embeddings):
                self.lc_embeddings = lc_embeddings
            def __call__(self, input: list[str]) -> list[list[float]]:
                return self.lc_embeddings.embed_documents(input)
                
        collection = client.get_collection(
            name="project_universe",
            embedding_function=LangchainEmbeddingFunc(embeddings)
        )
        results = collection.query(query_texts=[query], n_results=3)
        return str(results["documents"])
    except Exception as e:
        logger.error(f"Vector search failed: {e}")
        return f"Error searching vector DB: {e}"

@tool
def take_sim_action(api_endpoint: str, method: str, payload: dict) -> str:
    """Executes an action on the Project Universe Simulator. E.g., method='PUT', api_endpoint='/stories/STORY-1'."""
    try:
        url = f"{SIM_API_URL}{api_endpoint}"
        with httpx.Client() as client:
            if method.upper() == "POST":
                response = client.post(url, json=payload)
            elif method.upper() == "PUT":
                response = client.put(url, json=payload)
            else:
                return "Unsupported method"
                
            response.raise_for_status()
            return f"Success: {response.json()}"
    except Exception as e:
        return f"Failed to execute action: {e}"
