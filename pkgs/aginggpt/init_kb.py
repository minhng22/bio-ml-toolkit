import sys
import argparse
import logging
from pathlib import Path

root_dir = Path(__file__).parent.parent.parent
sys.path.append(str(root_dir))

from pkgs.aginggpt.knowledge_base import KnowledgeBase
from pkgs.aginggpt.data_loader import JsonLoader, PubMedAbstractLoader

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_sample_data(kb_path=None):
    kb = KnowledgeBase(kb_path)
    
    sample_data_path = Path(__file__).parent / "sample_data.json"
    
    if sample_data_path.exists():
        logger.info(f"Loading sample data from {sample_data_path}")
        
        json_loader = JsonLoader()
        documents = json_loader.load(str(sample_data_path))
        
        for doc in documents:
            kb.add_document(doc["content"], doc["metadata"], doc.get("id"))
            
        logger.info(f"Added {len(documents)} documents from JSON file")
    else:
        logger.warning(f"Sample data file not found: {sample_data_path}")
    
    pubmed_loader = PubMedAbstractLoader()
    abstracts = pubmed_loader.load("")
    
    for abstract in abstracts:
        kb.add_document(
            abstract["content"], 
            abstract["metadata"],
            abstract.get("id")
        )
        
    logger.info(f"Added {len(abstracts)} simulated PubMed abstracts")
    
    total_docs = len(kb.get_all_documents())
    logger.info(f"Knowledge base now contains {total_docs} documents")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Initialize AgingGPT knowledge base')
    parser.add_argument('--kb-path', type=str, help='Path to knowledge base directory')
    args = parser.parse_args()
    
    load_sample_data(args.kb_path)
