import os
import streamlit as st
import requests
import sqlite3
from pathlib import Path

API_URL = os.getenv("API_URL", "https://deploy-streamlit-senai.onrender.com")

# Configuração da página
st.set_page_config(
    page_title="DIRETRIZES",
    page_icon="📋",
    layout="wide"
)

# Estilo CSS
st.markdown("""
<style>
.status-card {
    background-color: white;
    padding: 1.5rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    border: 1px solid #eee;
}
.status-header {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
    color: #1a1a1a;
    font-size: 1.1rem;
    font-weight: bold;
}
.status-content {
    color: #4a5568;
    font-size: 0.95rem;
    margin-top: 0.5rem;
    line-height: 1.5;
}
.status-ok {
    color: #2ecc71;
    margin-right: 0.5rem;
}
.status-error {
    color: #e74c3c;
    margin-right: 0.5rem;
}
.status-warning {
    color: #f1c40f;
    margin-right: 0.5rem;
}
.progress-label {
    font-size: 0.9rem;
    color: #666;
    margin-top: 0.5rem;
    text-align: center;
}
.section-description {
    color: #4a5568;
    font-size: 1rem;
    margin-bottom: 1.5rem;
    line-height: 1.6;
    padding: 1rem;
    background-color: #f8fafc;
    border-radius: 8px;
    border-left: 4px solid #3182ce;
}
.main-description {
    color: #2d3748;
    font-size: 1.1rem;
    line-height: 1.7;
    padding: 1.5rem;
    background-color: #ebf8ff;
    border-radius: 10px;
    margin-bottom: 2rem;
    border-left: 5px solid #4299e1;
}
</style>
""", unsafe_allow_html=True)

def check_directory_exists(path):
    return os.path.exists(path) and os.path.isdir(path)

def check_file_exists(path):
    return os.path.exists(path) and os.path.isfile(path)

def check_api_health():
    try:
        response = requests.get(f"{API_URL}/health")
        return response.status_code == 200
    except:
        return False

def check_api_docs():
    try:
        response = requests.get(f"{API_URL}/docs")
        return response.status_code == 200
    except:
        return False

def check_sqlite_db():
    try:
        db_path = "../backend/db/usage.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usage_logs'")
        has_table = cursor.fetchone() is not None
        conn.close()
        return has_table
    except:
        return False

# Título e Descrição Principal
st.title("DIRETRIZES DO PROJETO")

st.markdown("""
<div class="main-description">
Este projeto implementa um sistema de perguntas e respostas sobre o SENAI utilizando RAG (Retrieval-Augmented Generation) 
com embeddings para buscar informações relevantes em documentos. O sistema é dividido em backend (FastAPI) e 
frontend (Streamlit), seguindo uma arquitetura modular e boas práticas de desenvolvimento.
</div>
""", unsafe_allow_html=True)

# Estrutura do Projeto
backend_path = Path("../backend")
directories = {
    "chains": backend_path / "chains",
    "services": backend_path / "services",
    "models": backend_path / "models",
    "db": backend_path / "db"
}

total_checks = 0
passed_checks = 0

# Verificações com descrições detalhadas
checks = {
    "Backend (FastAPI)": {
        "description": """
        API estruturada com RAG + embeddings e modularizada.
        """,
        "items": {
            "Módulo /chains": {
                "status": check_directory_exists(directories["chains"]),
                "description": "Fluxos de chamada IA."
            },
            "Módulo /services": {
                "status": check_directory_exists(directories["services"]),
                "description": "Integração com APIs externas."
            },
            "Módulo /models": {
                "status": check_directory_exists(directories["models"]),
                "description": "Schemas Pydantic."
            },
            "Banco SQLite": {
                "status": check_sqlite_db(),
                "description": "Registro de prompts/respostas/tokens."
            },
            "Health Check": {
                "status": check_api_health(),
                "description": "Endpoint /health funcionando."
            },
            "Documentação": {
                "status": check_api_docs(),
                "description": "Swagger UI no /docs."
            }
        }
    },
    "Frontend (Streamlit)": {
        "description": """
        Interface de interação com o usuário.
        """,
        "items": {
            "Interface Principal": {
                "status": True,
                "description": "Envio e exibição de perguntas e respostas."
            },
            "Fluxo Frontend➔Backend": {
                "status": check_api_health(),
                "description": "Comunicação correta frontend ➔ backend."
            }
        }
    },
    "Requisitos Gerais": {
        "description": """
        Requisitos técnicos mínimos.
        """,
        "items": {
            "Python 3.12 ou superior": {
                "status": True,
                "description": "Ambiente Python atualizado."
            },
            "Variáveis de Ambiente no Render": {
                "status": True,
                "description": "Configuração segura no ambiente de deploy."
            },
            "Versionamento DB": {
                "status": check_file_exists("../backend/db/usage.db"),
                "description": "Banco de dados versionado."
            }
        }
    }
}

# Exibir status
cols = st.columns(2)
col_idx = 0

for section, data in checks.items():
    with cols[col_idx]:
        st.markdown(f"### {section}")
        st.markdown(f"<div class='section-description'>{data['description']}</div>", unsafe_allow_html=True)
        
        for item, info in data['items'].items():
            total_checks += 1
            if info['status']:
                passed_checks += 1
                icon = "✅"
                status_class = "status-ok"
            else:
                icon = "❌"
                status_class = "status-error"
            
            st.markdown(f"""
            <div class="status-card">
                <div class="status-header">
                    <span class="{status_class}">{icon}</span>
                    {item}
                </div>
                <div class="status-content">
                    {info['description']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    col_idx = (col_idx + 1) % 2

# Barra de Progresso e Resumo
st.markdown("---")
progress = passed_checks / total_checks
st.progress(progress)
st.markdown(f"""
<div class="progress-label">
    <b>{passed_checks}</b> de <b>{total_checks}</b> requisitos atendidos ({progress*100:.1f}%)<br>
    Este índice representa a conformidade do projeto com as diretrizes estabelecidas.
</div>
""", unsafe_allow_html=True)

# Atualização
col1, col2, col3 = st.columns([1,1,1])
with col2:
    st.button("Verificar Diretrizes")
