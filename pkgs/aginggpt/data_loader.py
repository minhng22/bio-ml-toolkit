import json
import logging
from typing import List, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

class DataLoader:    
    def __init__(self):
        pass
    
    def load(self, source_path: str) -> List[Dict[str, Any]]:
        raise NotImplementedError("Subclasses must implement this method")

class TextFileLoader(DataLoader):    
    def load(self, source_path: str) -> List[Dict[str, Any]]:
        documents = []
        file_path = Path(source_path)
        
        if not file_path.exists():
            logger.error(f"File not found: {source_path}")
            return []
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            chunks = self._chunk_text(content)
            
            for i, chunk in enumerate(chunks):
                doc_id = f"{file_path.stem}_{i}"
                documents.append({
                    "id": doc_id,
                    "content": chunk,
                    "metadata": {
                        "source": str(file_path),
                        "chunk": i
                    }
                })
                
            logger.info(f"Loaded {len(documents)} chunks from {source_path}")
            return documents
            
        except Exception as e:
            logger.error(f"Error loading text file {source_path}: {e}")
            return []
    
    def _chunk_text(self, text: str, max_chunk_size: int = 1000) -> List[str]:
        paragraphs = text.split("\n\n")
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) > max_chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = paragraph
            else:
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph
        
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks

class JsonLoader(DataLoader):    
    def __init__(self, content_key: str = "content", metadata_key: str = "metadata"):
        super().__init__()
        self.content_key = content_key
        self.metadata_key = metadata_key
    
    def load(self, source_path: str) -> List[Dict[str, Any]]:
        documents = []
        file_path = Path(source_path)
        
        if not file_path.exists():
            logger.error(f"File not found: {source_path}")
            return []
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            if isinstance(data, list):
                for i, item in enumerate(data):
                    try:
                        content = item.get(self.content_key, "")
                        metadata = item.get(self.metadata_key, {})
                        metadata["source"] = str(file_path)
                        
                        doc_id = item.get("id", f"{file_path.stem}_{i}")
                        documents.append({
                            "id": doc_id,
                            "content": content,
                            "metadata": metadata
                        })
                    except Exception as e:
                        logger.error(f"Error processing JSON item: {e}")
                        continue
            else:
                content = data.get(self.content_key, "")
                metadata = data.get(self.metadata_key, {})
                metadata["source"] = str(file_path)
                
                doc_id = data.get("id", file_path.stem)
                documents.append({
                    "id": doc_id,
                    "content": content,
                    "metadata": metadata
                })
                
            logger.info(f"Loaded {len(documents)} documents from {source_path}")
            return documents
            
        except Exception as e:
            logger.error(f"Error loading JSON file {source_path}: {e}")
            return []

class PubMedAbstractLoader(DataLoader):
    def load(self, source_path: str) -> List[Dict[str, Any]]:
        documents = [
            {
                "id": "pmid_12345678",
                "content": "Recent studies have shown that cellular senescence is a significant contributor to aging and age-related diseases. Senescent cells accumulate with age and secrete inflammatory factors that can promote tissue dysfunction.",
                "metadata": {
                    "source": "PubMed",
                    "title": "Cellular Senescence in Aging",
                    "authors": "Smith J, Johnson A",
                    "year": "2023"
                }
            },
            {
                "id": "pmid_87654321",
                "content": "Mitochondrial dysfunction is implicated in aging processes. This study demonstrates that improving mitochondrial function through targeted interventions can extend lifespan in model organisms.",
                "metadata": {
                    "source": "PubMed",
                    "title": "Mitochondrial Function and Aging",
                    "authors": "Brown R, Davis T",
                    "year": "2022"
                }
            },
            {
                "id": "pmid_23456789",
                "content": "Rapamycin inhibits the mTOR pathway and has been shown to extend lifespan in multiple species. This review discusses the potential mechanisms and challenges of using rapamycin for aging interventions in humans.",
                "metadata": {
                    "source": "PubMed",
                    "title": "Rapamycin as an Aging Intervention",
                    "authors": "Wilson E, Garcia M",
                    "year": "2023"
                }
            }
        ]
        
        logger.info(f"Loaded {len(documents)} simulated PubMed abstracts")
        return documents
