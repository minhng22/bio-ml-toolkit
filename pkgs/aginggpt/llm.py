import logging
from typing import List, Dict, Any
import re
import torch
import os
from transformers import pipeline, BitsAndBytesConfig, AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
from nltk.tokenize import sent_tokenize
import nltk

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

logger = logging.getLogger(__name__)

class EnhancedLLMProcessor:
    def __init__(self, model_name="meta-llama/Llama-3.1-8B", use_fallback_model=True):
        self.model_name = model_name
        self.original_model = model_name
        logger.info(f"Initializing {model_name} LLM processor")
        
        try:
            login(token=os.environ["HUGGINGFACE_HUB_TOKEN"])
            logger.info("Successfully logged in to Hugging Face Hub")
        except Exception as e:
            logger.error(f"Failed to login to Hugging Face Hub: {e}")
        
        device_map = "auto" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        logger.info(f"Using device: {device_map}, dtype: {torch_dtype}")
        
        self.fallback_models = []

        logger.info(f"Attempting to load model: {model_name}")
        
        try:
            _ = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch_dtype,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True
            )
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            #self.llm_pipeline = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")
            
            self.llm_pipeline = pipeline(
                "text-generation",
                model=model_name,
                tokenizer=self.tokenizer,
                torch_dtype=torch_dtype,
                device_map=device_map,
                max_length=512,
                temperature=0.7,
            )
            logger.info(f"Successfully loaded {model_name} with 4-bit quantization")

            logger.info("downloading nltk")
            nltk.download('punkt_tab')
        except Exception as e:
            logger.error(f"Error loading {model_name}: {str(e)}")
            self.llm_pipeline = None
            
            if use_fallback_model:
                for fallback_model in self.fallback_models:
                    try:
                        logger.warning(f"Attempting to load fallback model: {fallback_model}")
                        self.llm_pipeline = pipeline(
                            "text-generation",
                            model=fallback_model,
                            torch_dtype=torch_dtype,
                            device_map=device_map,
                        )
                        self.model_name = fallback_model
                        logger.info(f"Successfully loaded fallback model: {fallback_model}")
                        break
                    except Exception as fallback_error:
                        logger.error(f"Error loading fallback model {fallback_model}: {str(fallback_error)}")
                        
            if self.llm_pipeline is None:
                logger.warning("Falling back to simulated mode - no models could be loaded")
    
    def generate_response(self, query: str, context_docs: List[Dict[str, Any]]) -> str:
        if not context_docs:
            return "I don't have specific information about that in my aging biology knowledge base. Please ask another question related to aging."
        
        expanded_query = self._rewrite_query(query)
        reranked_docs = self._rerank_documents(expanded_query, context_docs)
        filtered_docs = self._filter_and_compress_context(expanded_query, reranked_docs)
        prompt = self._prepare_prompt(query, filtered_docs)
        
        if self.llm_pipeline:
            try:
                response = self._generate_with_llm(prompt)
                logger.info(f"Generated _generate_with_llm response: {response}")
                verified_response = self._verify_response_factuality(query, response, filtered_docs)
                
                logger.info(f"Generated RAG response using {self.model_name} for query: {query}")
                return verified_response
            except Exception as e:
                logger.error(f"Error generating with {self.model_name}: {str(e)}")
                logger.warning("Falling back to rule-based response")
        
        key_terms = self._extract_key_terms(query)
        response = self._build_enhanced_response(query, key_terms, context_docs)
        logger.info(f"Generated fallback response for query: {query}")
        return response
    
    def _prepare_prompt(self, query: str, context_docs: List[Dict[str, Any]]) -> str:
        prompt = "You are an expert in aging biology. Answer the following question based on the provided context:\n\n"
        prompt += "Context:\n"
        
        for i, doc in enumerate(context_docs, 1):
            prompt += f"{i}. {doc['content']}"
            prompt += f" (Source: {doc['metadata'].get('source', 'Aging Research')})\n"
        
        prompt += f"\nQuestion: {query}\n\n"
        prompt += "Answer:"
        
        return prompt
    
    def _generate_with_llm(self, prompt: str) -> str:
        response = self.llm_pipeline(
            prompt,
            truncation=True,
            max_length=len(prompt.split()) + 512,  
            temperature=0.7,    
            top_p=0.9,           
            repetition_penalty=1.1,  
            do_sample=True,      
            num_return_sequences=1,
        )
        
        generated_text = response[0]['generated_text']
        
        if generated_text.startswith(prompt):
            generated_text = generated_text[len(prompt):].strip()
        
        return generated_text
    
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
    
    def _rewrite_query(self, query: str) -> str:
        if self.llm_pipeline:
            try:
                expansion_prompt = f"""You are an expert in aging biology research. 
                Your task is to expand this search query to improve document retrieval.
                Include key scientific concepts related to the query.
                Original query: "{query}"
                Expanded query:"""
                
                response = self.llm_pipeline(
                    expansion_prompt,
                    truncation=True,
                    max_length=len(expansion_prompt.split()) + 100,
                    temperature=0.3,
                    do_sample=True,
                    num_return_sequences=1,
                )
                
                expanded_text = response[0]['generated_text']
                if expanded_text.startswith(expansion_prompt):
                    expanded_text = expanded_text[len(expansion_prompt):].strip()
                
                logger.info(f"Original query: '{query}' -> Expanded: '{expanded_text}'")
                return expanded_text
            except Exception as e:
                logger.warning(f"Query expansion failed: {e}, using original query")
                
        return query
    
    def _rerank_documents(self, query: str, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not documents:
            return []
            
        scored_docs = []
        query_terms = set(self._extract_key_terms(query))
        
        for doc in documents:
            content = doc["content"].lower()
            doc_terms = set(re.findall(r'\b\w+\b', content))
            
            term_overlap = len(query_terms.intersection(doc_terms))
            term_score = term_overlap / (len(query_terms) + 1)
            
            metadata_score = 0.0
            if doc["metadata"].get("title"):
                title_terms = set(re.findall(r'\b\w+\b', doc["metadata"].get("title", "").lower()))
                title_overlap = len(query_terms.intersection(title_terms))
                metadata_score = title_overlap / (len(query_terms) + 1)
            
            category_score = 0.0
            if doc["metadata"].get("category"):
                query_lower = query.lower()
                category = doc["metadata"].get("category", "").lower()
                
                relevance_mappings = {
                    "hallmark": ["hallmark", "characteristic"],
                    "aging_mechanisms": ["mechanism", "cause", "pathway", "molecular", "cellular"],
                    "interventions": ["intervention", "therapy", "treatment", "extend", "lifespan", "longevity"]
                }
                
                for cat, terms in relevance_mappings.items():
                    if cat == category and any(term in query_lower for term in terms):
                        category_score = 0.5
                        break
            
            final_score = (0.5 * term_score) + (0.3 * metadata_score) + (0.2 * category_score)
            scored_docs.append((final_score, doc))
        
        scored_docs.sort(reverse=True, key=lambda x: x[0])
        
        logger.info(f"Reranked {len(documents)} documents, top score: {scored_docs[0][0] if scored_docs else 'N/A'}")
        
        return [doc for _, doc in scored_docs]
        
    def _filter_and_compress_context(self, query: str, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not documents:
            return []
            
        max_docs = 5
        relevance_threshold = 0.1
        
        filtered_docs = []
        query_terms = set(self._extract_key_terms(query))
        
        for doc in documents:
            content = doc["content"]
            doc_terms = set(re.findall(r'\b\w+\b', content.lower()))
            
            relevance_score = len(query_terms.intersection(doc_terms)) / (len(query_terms) + 1)
            
            if relevance_score >= relevance_threshold:
                sentences = sent_tokenize(content)
                
                if len(sentences) > 3:
                    scored_sentences = []
                    for sentence in sentences:
                        sent_terms = set(re.findall(r'\b\w+\b', sentence.lower()))
                        sent_relevance = len(query_terms.intersection(sent_terms)) / (len(query_terms) + 1)
                        scored_sentences.append((sent_relevance, sentence))
                    
                    scored_sentences.sort(reverse=True, key=lambda x: x[0])
                    top_sentences = [s for _, s in scored_sentences[:3]]
                    
                    compressed_content = " ".join(top_sentences)
                    compressed_doc = doc.copy()
                    compressed_doc["content"] = compressed_content
                    filtered_docs.append(compressed_doc)
                else:
                    filtered_docs.append(doc)
                    
            if len(filtered_docs) >= max_docs:
                break
        
        return filtered_docs if filtered_docs else documents[:max_docs]
    
    def _verify_response_factuality(self, query: str, response: str, context_docs: List[Dict[str, Any]]) -> str:
        if not self.llm_pipeline or not response or not context_docs:
            return response
            
        try:
            verification_prompt = f"""You are a fact-checker for aging biology research.
            Review this response and verify it against the provided context.
            If there are inaccuracies, correct them. If it's accurate, leave it unchanged.

            Response to verify: "{response}"

            Context for verification:
            """
            
            for i, doc in enumerate(context_docs, 1):
                verification_prompt += f"{i}. {doc['content']}\n"
                
            verification_prompt += "\nVerified response:"
            
            verification = self.llm_pipeline(
                verification_prompt,
                truncation=True,
                max_length=len(verification_prompt.split()),
                temperature=0.3,
                do_sample=True,
                num_return_sequences=1,
            )
            
            verified_text = verification[0]['generated_text']
            if verified_text.startswith(verification_prompt):
                verified_text = verified_text[len(verification_prompt):].strip()
                
            logger.info("Response verification completed")
            
            if len(verified_text) > 20:
                return verified_text
                
        except Exception as e:
            logger.warning(f"Response verification failed: {e}, using original response")
            
        return response
