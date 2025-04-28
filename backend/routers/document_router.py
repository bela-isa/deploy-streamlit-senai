from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
import os
from backend.services.document_service import DocumentService


router = APIRouter()
document_service = DocumentService()

class DocumentCreate(BaseModel):
    filename: str
    content: str

class Document(BaseModel):
    filename: str
    content: str
    added_at: datetime

@router.get("/documents", response_model=List[Document])
async def get_documents():
    """Retorna todos os documentos disponíveis"""
    try:
        # Forçar recarga dos documentos
        document_service._load_documents()
        
        documents = []
        for filename, content in document_service.documents.items():
            try:
                filepath = os.path.join(document_service.documents_dir, filename)
                if os.path.exists(filepath):
                    added_at = datetime.fromtimestamp(os.path.getctime(filepath))
                    
                    documents.append(Document(
                        filename=filename,
                        content=content,
                        added_at=added_at
                    ))
                else:
                    print(f"Arquivo não encontrado: {filepath}")  # Debug
            except Exception as e:
                print(f"Erro ao processar documento {filename}: {str(e)}")  # Debug
                continue
        
        print(f"Total de documentos retornados: {len(documents)}")  # Debug
        return documents
    except Exception as e:
        print(f"Erro ao listar documentos: {str(e)}")  # Debug
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents")
async def create_document(document: DocumentCreate):
    """Adiciona um novo documento"""
    try:
        document_service.add_document(document.filename, document.content)
        return {"message": "Documento adicionado com sucesso"}
    except Exception as e:
        print(f"Erro ao criar documento: {str(e)}")  # Debug
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/documents/{filename}")
async def delete_document(filename: str):
    """Remove um documento"""
    try:
        filepath = os.path.join(document_service.documents_dir, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            # Recarregar documentos
            document_service._load_documents()
            return {"message": "Documento removido com sucesso"}
        else:
            raise HTTPException(status_code=404, detail="Documento não encontrado")
    except Exception as e:
        print(f"Erro ao excluir documento: {str(e)}")  # Debug
        raise HTTPException(status_code=500, detail=str(e)) 
