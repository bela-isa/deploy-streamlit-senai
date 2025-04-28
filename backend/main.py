from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from backend.models.schemas import QuestionRequest, QuestionResponse
from backend.db.database import get_db, Usage
from backend.chains.qa_chain import QAChain
from backend.routers.document_router import router as document_router
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title=os.getenv("APP_NAME", "Prova IA Generativa – Backend"),
    version=os.getenv("APP_VERSION", "1.0.0"),
    description="API para responder perguntas sobre o SENAI usando documentos com RAG"
)

# Adicionar o router de documentos
app.include_router(document_router, tags=["Documents"])

qa_chain = QAChain()

@app.get("/health", tags=["Utils"])
def health_check():
    return {"status": "ok"}

@app.post("/question", response_model=QuestionResponse, tags=["QA"])
def answer_question(
    question_request: QuestionRequest,
    db: Session = Depends(get_db)
):
    # Gerar resposta
    answer, context_used, tokens_used = qa_chain.get_answer(question_request.question)

    # Registrar uso no banco de dados
    usage_log = Usage(
        timestamp=datetime.utcnow(),
        prompt=question_request.question,
        response=answer,
        tokens_used=tokens_used
    )
    db.add(usage_log)
    db.commit()

    return QuestionResponse(
        answer=answer,
        context_used=context_used,
        tokens_used=tokens_used
    )
