import os
from typing import List, Dict
import json
from ..config import DOCUMENTS_DIR

class DocumentService:
    def __init__(self):
        self.documents_dir = DOCUMENTS_DIR
        print(f"Diretório de documentos: {self.documents_dir}")  # Debug
        self.documents: Dict[str, str] = {}
        self._load_documents()
    
    def _load_documents(self):
        """Carrega todos os documentos do diretório"""
        if not os.path.exists(self.documents_dir):
            print(f"Criando diretório: {self.documents_dir}")  # Debug
            os.makedirs(self.documents_dir)
        
        # Carregar todos os documentos do diretório
        print(f"Procurando documentos em: {self.documents_dir}")  # Debug
        for filename in os.listdir(self.documents_dir):
            if filename.endswith('.txt'):
                filepath = os.path.join(self.documents_dir, filename)
                print(f"Carregando documento: {filepath}")  # Debug
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        self.documents[filename] = f.read()
                except Exception as e:
                    print(f"Erro ao carregar {filepath}: {str(e)}")  # Debug
        
        print(f"Total de documentos carregados: {len(self.documents)}")  # Debug
    
    def get_all_documents(self) -> List[str]:
        """Retorna o conteúdo de todos os documentos"""
        # Recarregar documentos para garantir lista atualizada
        self._load_documents()
        return list(self.documents.values())
    
    def add_document(self, filename: str, content: str):
        """Adiciona um novo documento"""
        if not filename.endswith('.txt'):
            filename += '.txt'
        
        filepath = os.path.join(self.documents_dir, filename)
        print(f"Salvando documento em: {filepath}")  # Debug
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            self.documents[filename] = content
            print(f"Documento salvo com sucesso: {filename}")  # Debug
        except Exception as e:
            print(f"Erro ao salvar documento {filename}: {str(e)}")  # Debug
            raise 