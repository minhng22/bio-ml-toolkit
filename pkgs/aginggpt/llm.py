import logging
from typing import List, Dict, Any
import re

logger = logging.getLogger(__name__)

class EnhancedLLMProcessor:
    def __init__(self, model_name="simulated-aging-bio-gpt"):
        self.model_name = model_name
        logger.info(f"Initialized {model_name} LLM processor")
    
    def generate_response(self, query: str, context_docs: List[Dict[str, Any]]) -> str:
        if not context_docs:
            return "I don't have specific information about that in my aging biology knowledge base. Please ask another question related to aging."
        key_terms = self._extract_key_terms(query)
        
        response = self._build_enhanced_response(query, key_terms, context_docs)
        
        logger.info(f"Generated response for query: {query[:30]}...")
        return response
    
    def _extract_key_terms(self, query: str) -> List[str]:
        common_words = {"the", "a", "an", "in", "on", "at", "to", "for", "with", "by", 
                        "is", "are", "was", "were", "be", "been", "being", "have", "has", 
                        "had", "do", "does", "did", "can", "could", "will", "would", "about"}
        
        words = re.findall(r'\b\w+\b', query.lower())
        return [word for word in words if word not in common_words and len(word) > 2]
    
    def _build_enhanced_response(self, query: str, key_terms: List[str], context_docs: List[Dict[str, Any]]) -> str:
        if any(term in query.lower() for term in ["hallmark", "hallmarks", "characteristic", "characteristics"]):
            return self._generate_hallmarks_response(context_docs)
            
        elif any(term in query.lower() for term in ["intervention", "extend", "lifespan", "longevity", "treatment"]):
            return self._generate_interventions_response(query, context_docs)
            
        elif any(term in query.lower() for term in ["mechanism", "cause", "pathway", "molecular", "cellular"]):
            return self._generate_mechanisms_response(query, context_docs)
            
        else:
            return self._generate_default_response(query, context_docs)
    
    def _generate_hallmarks_response(self, context_docs: List[Dict[str, Any]]) -> str:
        hallmarks_docs = [doc for doc in context_docs if "hallmark" in doc["content"].lower()]
        
        if hallmarks_docs:
            response = "## Hallmarks of Aging\n\n"
            response += "The scientific understanding of aging has converged on nine hallmarks that contribute to the aging process:\n\n"
            
            hallmarks_doc = next((doc for doc in hallmarks_docs if "nine hallmarks" in doc["content"].lower()), None)
            if hallmarks_doc:
                hallmarks_text = hallmarks_doc["content"]
                if ":" in hallmarks_text:
                    hallmarks_list = hallmarks_text.split(":")[1].strip().split(", ")
                    for i, hallmark in enumerate(hallmarks_list):
                        response += f"{i+1}. **{hallmark.strip()}**\n"
                    
                    response += f"\nSource: {hallmarks_doc['metadata'].get('source', 'Research on Aging Hallmarks')}\n\n"
                    
                    response += "These hallmarks represent the primary mechanisms that contribute to age-related decline in organisms. Understanding these processes is crucial for developing interventions that may slow or reverse aspects of aging."
                else:
                    response += hallmarks_text
            else:
                response += "The key hallmarks include genomic instability, telomere attrition, epigenetic alterations, loss of proteostasis, deregulated nutrient sensing, mitochondrial dysfunction, cellular senescence, stem cell exhaustion, and altered intercellular communication."
                
            return response
        else:
            return "Aging is characterized by several hallmarks, including genomic instability, telomere attrition, and cellular senescence. These processes contribute to the gradual decline in physiological function that we recognize as aging."
    
    def _generate_interventions_response(self, query: str, context_docs: List[Dict[str, Any]]) -> str:
        intervention_docs = [doc for doc in context_docs 
                              if doc["metadata"].get("category") == "interventions" 
                              or any(term in doc["content"].lower() for term in ["intervention", "restrict", "treatment", "therapy", "extend", "lifespan"])]
        
        if intervention_docs:
            response = "## Interventions in Aging Research\n\n"
            response += "Several interventions have shown promise in extending lifespan or healthspan in model organisms:\n\n"
            
            for doc in intervention_docs:
                response += f"- **{doc['content']}**\n"
                response += f"  Source: {doc['metadata'].get('source', 'Aging Research')}\n\n"
                
            response += "Research on these interventions is ongoing, with a focus on translating findings from model organisms to potential applications in human aging."
            
            return response
        else:
            return "Several interventions have shown promise in aging research, including caloric restriction, rapamycin, senolytics (compounds that eliminate senescent cells), and NAD+ precursors. Research is ongoing to understand how these interventions might be applied to promote healthy aging in humans."
    
    def _generate_mechanisms_response(self, query: str, context_docs: List[Dict[str, Any]]) -> str:
        mechanism_docs = [doc for doc in context_docs 
                           if doc["metadata"].get("category") == "aging_mechanisms" 
                           or any(term in doc["content"].lower() for term in ["mechanism", "pathway", "molecular", "cellular"])]
        
        if mechanism_docs:
            response = "## Molecular and Cellular Mechanisms of Aging\n\n"
            
            for doc in mechanism_docs:
                response += f"- {doc['content']}\n"
                response += f"  Source: {doc['metadata'].get('source', 'Aging Research')}\n\n"
                
            response += "These mechanisms interact in complex ways to drive the aging phenotype. Understanding these interactions is a key focus of current aging research."
            
            return response
        else:
            return "Aging involves complex molecular and cellular mechanisms, including accumulation of DNA damage, protein misfolding, cellular senescence, and chronic inflammation. These processes interact to drive the physiological changes associated with aging."
    
    def _generate_default_response(self, query: str, context_docs: List[Dict[str, Any]]) -> str:
        response = f"## Information on Aging Biology\n\n"
        response += f"Based on your query about '{query}', here's what current research indicates:\n\n"
        
        for doc in context_docs:
            response += f"- {doc['content']}\n"
            response += f"  Source: {doc['metadata'].get('source', 'Aging Research')}\n\n"
            
        response += "This information represents current understanding in the field of aging biology and is subject to revision as new research emerges."
        
        return response
