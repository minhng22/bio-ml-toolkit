import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class KnowledgeBase:    
    def __init__(self, base_path: Optional[str] = None):
        if base_path:
            self.base_path = Path(base_path)
        else:
            self.base_path = Path.home() / ".aging_gpt_kb"
            
        self.docs_path = self.base_path / "documents"
        self._ensure_directories()
        
        self.documents = self._load_documents()
        logger.info(f"Initialized knowledge base with {len(self.documents)} documents")
    
    def _ensure_directories(self):
        os.makedirs(self.base_path, exist_ok=True)
        os.makedirs(self.docs_path, exist_ok=True)
    
    def _load_documents(self) -> List[Dict[str, Any]]:
        documents = []
        
        for file_path in self.docs_path.glob("*.json"):
            try:
                with open(file_path, "r") as f:
                    doc_data = json.load(f)
                    documents.append(doc_data)
            except Exception as e:
                logger.error(f"Error loading document {file_path}: {e}")
        
        if not documents:
            documents = self._load_default_knowledge()
            
        return documents
    
    def _load_default_knowledge(self) -> List[Dict[str, Any]]:
        default_docs = [
            {
                "id": "hallmarks_aging_1",
                "content": "Aging is characterized by nine hallmarks: genomic instability, telomere attrition, epigenetic alterations, loss of proteostasis, deregulated nutrient sensing, mitochondrial dysfunction, cellular senescence, stem cell exhaustion, and altered intercellular communication.",
                "metadata": {"source": "Hallmarks of Aging, López-Otín et al., 2013", "category": "aging_mechanisms"}
            },
            {
                "id": "caloric_restriction_1",
                "content": "Caloric restriction has been shown to extend lifespan in various model organisms including yeast, worms, flies, and mice.",
                "metadata": {"source": "Caloric Restriction Research", "category": "interventions"}
            },
            {
                "id": "cell_senescence_1",
                "content": "Senescent cells accumulate with age and secrete pro-inflammatory cytokines, chemokines, and extracellular matrix proteases, collectively known as the senescence-associated secretory phenotype (SASP).",
                "metadata": {"source": "Cellular Senescence Research", "category": "aging_mechanisms"}
            },
            {
                "id": "rapamycin_1",
                "content": "Rapamycin, which inhibits the mTOR pathway, has been shown to extend lifespan in mice and is being studied for its potential anti-aging effects in humans.",
                "metadata": {"source": "mTOR Inhibition Research", "category": "interventions"}
            },
            {
                "id": "mitochondria_1",
                "content": "Mitochondrial dysfunction is a key hallmark of aging, characterized by reduced efficiency in the electron transport chain and increased production of reactive oxygen species.",
                "metadata": {"source": "Mitochondrial Theory of Aging", "category": "aging_mechanisms"}
            }
        ]
        
        for doc in default_docs:
            self.add_document(doc["content"], doc["metadata"], doc.get("id"))
            
        return default_docs
    
    def add_document(self, content: str, metadata: Dict[str, Any], doc_id: Optional[str] = None):
        if not doc_id:
            # Generate an ID based on the number of existing documents
            doc_id = f"doc_{len(self.documents) + 1}"
            
        document = {
            "id": doc_id,
            "content": content,
            "metadata": metadata
        }
        
        file_path = self.docs_path / f"{doc_id}.json"
        try:
            with open(file_path, "w") as f:
                json.dump(document, f, indent=2)
                
            self.documents.append(document)
            logger.info(f"Added document with ID: {doc_id}")
            
        except Exception as e:
            logger.error(f"Error adding document: {e}")
    
    def get_all_documents(self) -> List[Dict[str, Any]]:
        return self.documents
    
    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        for doc in self.documents:
            if doc["id"] == doc_id:
                return doc
        return None
        
    def search_documents(self, query: str) -> List[Dict[str, Any]]:
        query_terms = query.lower().split()
        results = []
        
        for doc in self.documents:
            score = 0
            content = doc["content"].lower()
            
            for term in query_terms:
                if term in content:
                    score += 1
                    
            if score > 0:
                results.append((doc, score))
                
        results.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, _ in results]
