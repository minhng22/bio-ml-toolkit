import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging
from .knowledge_base import KnowledgeBase
from .llm import EnhancedLLMProcessor

logger = logging.getLogger(__name__)

@dataclass
class Document:
    content: str
    metadata: Dict[str, Any]
    
class Retriever:
    def __init__(self, knowledge_base_path: str = None):
        self.kb = KnowledgeBase(knowledge_base_path)
        self.documents = []
        
        try:
            from .vector_db import VectorDatabase
            self.vector_db = VectorDatabase(self.kb)
            self.use_vector_db = True
            logger.info("Using vector database for retrieval")
        except ImportError:
            self.use_vector_db = False
            logger.warning("Vector database dependencies not installed. Using basic retrieval.")
        
        self._initialize_knowledge_base()
        
    def _initialize_knowledge_base(self):
        kb_docs = self.kb.get_all_documents()
        
        self.documents = [
            Document(
                content=doc["content"],
                metadata=doc["metadata"]
            )
            for doc in kb_docs
        ]
        
        logger.info(f"Initialized knowledge base with {len(self.documents)} documents")
    
    def add_document(self, content: str, metadata: Dict[str, Any]):
        self.kb.add_document(content, metadata)
        
        self.documents.append(Document(content=content, metadata=metadata))
        
        if hasattr(self, 'use_vector_db') and self.use_vector_db:
            try:
                doc_dict = {"content": content, "metadata": metadata}
                self.vector_db.add_document(doc_dict)
            except Exception as e:
                logger.error(f"Error adding document to vector database: {e}")
        
    def retrieve(self, query: str, top_k: int = 3) -> List[Document]:
        if hasattr(self, 'use_vector_db') and self.use_vector_db:
            try:
                results = self.vector_db.search(query, top_k=top_k)
                
                return [
                    Document(
                        content=doc["content"],
                        metadata=doc["metadata"]
                    )
                    for doc in results
                ]
            except Exception as e:
                logger.error(f"Error using vector database: {e}")
                logger.info("Falling back to keyword search")
        
        results = []
        query_terms = query.lower().split()
        
        for doc in self.documents:
            score = 0
            for term in query_terms:
                if term.lower() in doc.content.lower():
                    score += 1
            
            if score > 0:
                results.append((doc, score))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, _ in results[:top_k]]

class LLMProcessor:
    def __init__(self):
        self.processor = EnhancedLLMProcessor()
    
    def generate(self, query: str, context_docs: List[Document]) -> str:
        context_dicts = [
            {
                "content": doc.content,
                "metadata": doc.metadata
            }
            for doc in context_docs
        ]
        
        return self.processor.generate_response(query, context_dicts)

class AgingGPT:
    def __init__(self, knowledge_base_path: str = None):
        self.retriever = Retriever(knowledge_base_path)
        self.llm_processor = LLMProcessor()
        
    def query(self, query_text: str, top_k: int = 3) -> str:
        try:
            retrieved_docs = self.retriever.retrieve(query_text, top_k=top_k)
            
            response = self.llm_processor.generate(query_text, retrieved_docs)
            
            logger.info(f"Generated response for query: {query_text}")
            return response
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return f"Sorry, I encountered an error while processing your question. Please try again."
            
    def add_knowledge(self, content: str, source: str):
        self.retriever.add_document(content, {"source": source})
        logger.info(f"Added new knowledge from source: {source}")
