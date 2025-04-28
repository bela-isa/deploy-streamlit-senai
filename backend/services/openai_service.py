from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import List, Tuple
import httpx

load_dotenv()

class OpenAIService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY não encontrada nas variáveis de ambiente")
        
        # Configura cliente HTTP (se precisar proxy)
        http_client = None
        if os.getenv("HTTPS_PROXY"):
            http_client = httpx.Client(proxies={"https": os.getenv("HTTPS_PROXY")})
        
        # Inicializa o client OpenAI
        self.client = OpenAI(
            api_key=api_key,
            http_client=http_client,
            timeout=60.0  # timeout maior para embeddings
        )

        self.chat_model = os.getenv("CHAT_MODEL", "gpt-3.5-turbo")
        self.embeddings_model = os.getenv("EMBEDDINGS_MODEL", "text-embedding-3-small")
    
    def get_embedding(self, text: str) -> List[float]:
        """Gera embedding para um texto"""
        try:
            response = self.client.embeddings.create(
                model=self.embeddings_model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"Erro ao gerar embedding: {str(e)}")
    
    def get_completion(self, prompt: str, context: str = "") -> Tuple[str, int]:
        """Gera resposta de chat usando o modelo configurado"""
        try:
            messages = [
                {"role": "system", "content": "Você é um assistente especializado em responder perguntas sobre o SENAI com precisão e clareza."},
                {"role": "user", "content": f"Use este contexto para responder à pergunta:\n\nContexto: {context}\n\nPergunta: {prompt}"}
            ]
            
            response = self.client.chat.completions.create(
                model=self.chat_model,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content, response.usage.total_tokens
        except Exception as e:
            raise Exception(f"Erro ao gerar resposta: {str(e)}")
