import os
import logging
import chromadb
from chromadb.config import Settings
from llm_provider import get_llm_provider

logger = logging.getLogger(__name__)

CHROMA_HOST = os.getenv("CHROMA_HOST", "vector-db")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8002"))

class VectorIndexer:
    def __init__(self):
        try:
            self.client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT, settings=Settings(allow_reset=True))
            # Use chroma's built-in default embedding if our LLMProvider embeddings fail or are slow, 
            # but ideally we use the chosen LLM Provider's embeddings
            self.provider = get_llm_provider()
            self.embeddings = self.provider.get_embeddings()
            
            # Simple wrapper to match chroma's Expected embedding function interface
            class LangchainEmbeddingFunc:
                def __init__(self, lc_embeddings):
                    self.lc_embeddings = lc_embeddings
                def __call__(self, input: list[str]) -> list[list[float]]:
                    return self.lc_embeddings.embed_documents(input)
                    
            self.collection = self.client.get_or_create_collection(
                name="project_universe",
                embedding_function=LangchainEmbeddingFunc(self.embeddings)
            )
        except Exception as e:
            logger.error(f"Failed to connect to ChromaDB: {e}")
            self.client = None

    def sync_entity(self, event_type: str, entity_type: str, entity_id: str, fields: dict):
        if not self.client:
            logger.warning("Chroma client not initialized, skipping sync.")
            return

        logger.info(f"Syncing {entity_type} {entity_id} to Chroma from event {event_type}")
        
        # Only index fields that have dense text like descriptions
        text_content = ""
        metadata = {"entity_type": entity_type, "entity_id": entity_id}
        
        if "description" in fields and fields["description"]:
            text_content += fields["description"] + "\n"
        if "title" in fields and fields["title"]:
            text_content = fields["title"] + "\n" + text_content
            
        if not text_content.strip():
            logger.info(f"No text content to index for {entity_id}")
            return
            
        # Optional: Add other flat fields to metadata
        for k, v in fields.items():
            if isinstance(v, (str, int, float, bool)):
                metadata[k] = v
                
        # Upsert into Chroma
        self.collection.upsert(
            documents=[text_content],
            metadatas=[metadata],
            ids=[f"{entity_type}_{entity_id}"]
        )
