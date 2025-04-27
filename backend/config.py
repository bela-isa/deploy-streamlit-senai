import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações da API OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")

# Configurações do banco de dados
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db/usage.db")

# Configurações da aplicação
APP_NAME = os.getenv("APP_NAME", "Prova IA Generativa")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

# Configurações de documentos
DOCUMENTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'documents')) 