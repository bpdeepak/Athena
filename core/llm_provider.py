import os
import logging
from abc import ABC, abstractmethod
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.embeddings import Embeddings
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings

logger = logging.getLogger(__name__)

class LLMProvider(ABC):
    @abstractmethod
    def get_chat_model(self) -> BaseChatModel:
        pass

    @abstractmethod
    def get_embeddings(self) -> Embeddings:
        pass

class GeminiProvider(LLMProvider):
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning("GEMINI_API_KEY is not set. GeminiProvider may fail.")
        
    def get_chat_model(self) -> BaseChatModel:
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0,
            google_api_key=self.api_key
        )
        
    def get_embeddings(self) -> Embeddings:
        return GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=self.api_key
        )

class OllamaProvider(LLMProvider):
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model = "llama3"
        
    def get_chat_model(self) -> BaseChatModel:
        return ChatOllama(
            base_url=self.base_url,
            model=self.model,
            temperature=0
        )
        
    def get_embeddings(self) -> Embeddings:
        return OllamaEmbeddings(
            base_url=self.base_url,
            model=self.model
        )

def get_llm_provider() -> LLMProvider:
    backend = os.getenv("LLM_BACKEND", "gemini").lower()
    if backend == "ollama":
        logger.info("Using Ollama backend")
        return OllamaProvider()
    else:
        logger.info("Using Gemini backend")
        return GeminiProvider()
