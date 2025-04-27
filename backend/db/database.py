from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json
from sqlalchemy.sql import func
from ..config import DATABASE_URL

# Criar engine do SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Usage(Base):
    __tablename__ = "usage_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    prompt = Column(Text)  # Usando Text para prompts longos
    response = Column(Text)  # Usando Text para respostas longas
    tokens_used = Column(Integer)
    model_name = Column(String)  # Nome do modelo usado
    context_used = Column(Text)  # Documentos usados como contexto
    
    def to_dict(self):
        """Converte o registro para dicionário"""
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "prompt": self.prompt,
            "response": self.response,
            "tokens_used": self.tokens_used,
            "model_name": self.model_name,
            "context_used": json.loads(self.context_used) if self.context_used else []
        }

# Criar o banco de dados e as tabelas
Base.metadata.create_all(bind=engine)

def get_db():
    """Fornece uma sessão do banco de dados"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def log_usage(db, prompt: str, response: str, tokens: int, model: str, context: list):
    """Registra o uso da API no banco de dados"""
    try:
        usage_log = Usage(
            prompt=prompt,
            response=response,
            tokens_used=tokens,
            model_name=model,
            context_used=json.dumps(context)
        )
        db.add(usage_log)
        db.commit()
        return usage_log
    except Exception as e:
        db.rollback()
        raise Exception(f"Erro ao registrar uso: {str(e)}")

def get_usage_stats(db):
    """Retorna estatísticas de uso"""
    try:
        total_requests = db.query(Usage).count()
        total_tokens = db.query(Usage).with_entities(
            func.sum(Usage.tokens_used)
        ).scalar() or 0
        
        return {
            "total_requests": total_requests,
            "total_tokens": total_tokens,
            "average_tokens": total_tokens / total_requests if total_requests > 0 else 0
        }
    except Exception as e:
        raise Exception(f"Erro ao obter estatísticas: {str(e)}") 