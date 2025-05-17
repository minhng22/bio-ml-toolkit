import logging
import numpy as np
from typing import List, Dict, Any
from .knowledge_base import KnowledgeBase

try:
    from sentence_transformers import SentenceTransformer
    HAVE_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAVE_SENTENCE_TRANSFORMERS = False

try:
    import faiss
    HAVE_FAISS = True
except ImportError:
    HAVE_FAISS = False

logger = logging.getLogger(__name__)

class VectorDatabase:    
    def __init__(self, knowledge_base: KnowledgeBase, embedding_model: str = "all-MiniLM-L6-v2"):
        self.knowledge_base = knowledge_base
        self.embedding_model_name = embedding_model
        self.embedding_model = None
        self.index = None
        self.documents = []
        self.embeddings = []
        
        if not HAVE_SENTENCE_TRANSFORMERS:
            logger.warning("sentence-transformers not installed. Using fallback search method.")
        if not HAVE_FAISS:
            logger.warning("faiss not installed. Using fallback search method.")
            
        self._initialize()
        
    def _initialize(self):
        self.documents = self.knowledge_base.get_all_documents()
        
        if HAVE_SENTENCE_TRANSFORMERS and HAVE_FAISS:
            try:
                self.embedding_model = SentenceTransformer(self.embedding_model_name)
                
                document_texts = [doc["content"] for doc in self.documents]
                self.embeddings = self.embedding_model.encode(document_texts)
                
                dimension = self.embeddings.shape[1]
                self.index = faiss.IndexFlatL2(dimension)
                self.index.add(np.array(self.embeddings).astype('float32'))
                
                logger.info(f"Initialized vector database with {len(self.documents)} documents")
                
            except Exception as e:
                logger.error(f"Error initializing vector database: {e}")
                self.embedding_model = None
                self.index = None
    
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        if self.embedding_model and self.index:
            query_embedding = self.embedding_model.encode([query])
            
            distances, indices = self.index.search(np.array(query_embedding).astype('float32'), top_k)
            
            results = []
            for idx in indices[0]:
                if idx >= 0 and idx < len(self.documents):
                    results.append(self.documents[idx])
            
            return results
        else:
            return self._keyword_search(query, top_k)
    
    def _keyword_search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        results = []
        query_terms = query.lower().split()
        
        for doc in self.documents:
            score = 0
            for term in query_terms:
                if term.lower() in doc["content"].lower():
                    score += 1
            
            if score > 0:
                results.append((doc, score))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, _ in results[:top_k]]
        
    def add_document(self, document: Dict[str, Any]):
        self.documents.append(document)
        
        if self.embedding_model and self.index:
            # Create embedding for the new document
            embedding = self.embedding_model.encode([document["content"]])
            
            # Add to the index
            self.index.add(np.array(embedding).astype('float32'))
            self.embeddings = np.vstack((self.embeddings, embedding))
            
        logger.info(f"Added document to vector database")
