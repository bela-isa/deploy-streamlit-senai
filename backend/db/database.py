from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import Session
import os
import json
from datetime import datetime
from backend.models.schemas import UsageLog
from dotenv import load_dotenv

load_dotenv()

# Garante que a pasta backend/db/ exista antes de criar o banco
os.makedirs("backend/db", exist_ok=True)

SQLALCHEMY_DATABASE_URL = "sqlite:///backend/db/usage.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Usage(Base):
    __tablename__ = "usage_logs"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(String)
    response = Column(String)
    tokens_used = Column(Integer)
    timestamp = Column(DateTime)

# Cria as tabelas no banco
Base.metadata.create_all(bind=engine)

def get_db():
    """Abre e fecha a sessão com o banco de dados"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def log_usage(db: Session, prompt: str, response: str, tokens: int):
    """Registra o uso da API no banco de dados"""
    try:
        usage_log = Usage(
            prompt=prompt,
            response=response,
            tokens_used=tokens,
            timestamp=datetime.utcnow()
        )
        db.add(usage_log)
        db.commit()
        return usage_log
    except Exception as e:
        db.rollback()
        raise Exception(f"Erro ao registrar uso: {str(e)}")

def get_usage_stats(db: Session):
    """Retorna estatísticas de uso"""
    try:
        total_requests = db.query(Usage).count()
        total_tokens = db.query(func.sum(Usage.tokens_used)).scalar() or 0
        
        return {
            "total_requests": total_requests,
            "total_tokens": total_tokens,
            "average_tokens": total_tokens / total_requests if total_requests > 0 else 0
        }
    except Exception as e:
        raise Exception(f"Erro ao obter estatísticas: {str(e)}")
