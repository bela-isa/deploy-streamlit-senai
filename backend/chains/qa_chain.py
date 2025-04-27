from services.openai_service import OpenAIService
from services.document_service import DocumentService
from typing import List, Tuple
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class QAChain:
    def __init__(self):
        self.openai_service = OpenAIService()
        self.document_service = DocumentService()
        self.documents: List[Tuple[str, List[float]]] = []
        self._initialize_documents()
    
    def _initialize_documents(self):
        """Carrega e processa todos os documentos"""
        # Recarregar documentos a cada consulta para garantir dados atualizados
        self.documents = []
        for doc in self.document_service.get_all_documents():
            self.add_document(doc)
    
    def add_document(self, text: str):
        """Adiciona um documento à base de conhecimento"""
        embedding = self.openai_service.get_embedding(text)
        self.documents.append((text, embedding))
    
    def get_relevant_context(self, query: str, top_k: int = 3) -> List[str]:
        """Recupera os documentos mais relevantes para a query"""
        # Recarregar documentos para garantir que temos os mais recentes
        self._initialize_documents()
        
        if not self.documents:
            return []
            
        query_embedding = self.openai_service.get_embedding(query)
        
        # Calcular similaridade com todos os documentos
        similarities = []
        for _, doc_embedding in self.documents:
            similarity = cosine_similarity(
                np.array(query_embedding).reshape(1, -1),
                np.array(doc_embedding).reshape(1, -1)
            )[0][0]
            similarities.append(similarity)
        
        # Pegar os top_k documentos mais similares
        top_indices = np.argsort(similarities)[-top_k:][::-1]  # Ordem decrescente
        return [self.documents[i][0] for i in top_indices]
    
    def get_answer(self, question: str) -> Tuple[str, List[str], int]:
        """Gera uma resposta para a pergunta usando o contexto relevante"""
        relevant_docs = self.get_relevant_context(question)
        context = "\n".join(relevant_docs) if relevant_docs else ""
        
        answer, tokens_used = self.openai_service.get_completion(question, context)
        return answer, relevant_docs, tokens_used 