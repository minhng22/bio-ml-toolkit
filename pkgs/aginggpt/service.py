from typing import Optional, Dict, Any
import logging
from .model import AgingGPT
from .llm import get_random_loading_message

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

_aging_gpt_instance: Optional[AgingGPT] = None

def get_model_instance(knowledge_base_path: Optional[str] = None) -> AgingGPT:
    global _aging_gpt_instance
    
    if _aging_gpt_instance is None:
        logger.info("Initializing AgingGPT model")
        _aging_gpt_instance = AgingGPT(knowledge_base_path)
        
    return _aging_gpt_instance

def get_loading_message() -> str:
    """Get a funny loading message for the UI"""
    return get_random_loading_message()

def process_query(query_text: str) -> Dict[str, Any]:
    if not query_text or query_text.strip() == "":
        return {
            "response": "Please enter a question about aging biology.",
            "status": "error"
        }
    
    try:
        model = get_model_instance()
        response = model.query(query_text)
        
        return {
            "response": response,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)
        return {
            "response": "Sorry, I encountered an error while processing your question. Please try again.",
            "status": "error"
        }

def add_knowledge(content: str, source: str) -> Dict[str, Any]:
    try:
        model = get_model_instance()
        model.add_knowledge(content, source)
        
        return {
            "message": f"Successfully added new knowledge from {source}",
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error adding knowledge: {e}", exc_info=True)
        return {
            "message": f"Error adding knowledge: {str(e)}",
            "status": "error"
        }
