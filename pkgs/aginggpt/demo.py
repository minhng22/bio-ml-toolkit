import sys
from pathlib import Path
import logging

root_dir = Path(__file__).parent.parent.parent
sys.path.append(str(root_dir))

from pkgs.aginggpt.model import AgingGPT
from pkgs.aginggpt.data_loader import PubMedAbstractLoader

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def demo_aging_gpt():
    print("=" * 80)
    print("AgingGPT Demonstration".center(80))
    print("=" * 80)
    print("\nInitializing model...")
    
    model = AgingGPT()
    
    print("\nLoading sample PubMed abstracts...")
    loader = PubMedAbstractLoader()
    abstracts = loader.load("")
    
    for abstract in abstracts:
        model.add_knowledge(abstract["content"], abstract["metadata"].get("title", "PubMed"))
    
    print(f"Added {len(abstracts)} sample abstracts to the knowledge base")
    
    queries = [
        "What are the hallmarks of aging?",
        "How does caloric restriction affect lifespan?",
        "What is cellular senescence?",
        "Tell me about rapamycin and aging.",
        "How do mitochondria affect aging?"
    ]
    
    for i, query in enumerate(queries):
        print("\n" + "-" * 80)
        print(f"Query {i+1}: {query}")
        print("-" * 80)
        
        response = model.query(query)
        print("\nResponse:")
        print(response)
    
    print("\n" + "=" * 80)
    print("End of demonstration".center(80))
    print("=" * 80)

if __name__ == "__main__":
    demo_aging_gpt()
