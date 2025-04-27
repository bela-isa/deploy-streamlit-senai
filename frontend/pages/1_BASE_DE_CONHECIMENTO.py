import os
import streamlit as st
import requests
from datetime import datetime

API_URL = os.getenv("API_URL", "http://localhost:8000")

# Configuração da página
st.set_page_config(
    page_title="BASE DE CONHECIMENTO",
    page_icon="📚",
    layout="wide"
)

# Configurar nome no menu lateral
st.sidebar._html = """
<style>
    [data-testid="stSidebarNav"] li:nth-child(2) div::before {
        content: "BASE DE CONHECIMENTO" !important;
    }
</style>
"""

# Estilo CSS personalizado
st.markdown("""
<style>
.document-card {
    padding: 1.5rem;
    border-radius: 0.5rem;
    border: 1px solid #e2e8f0;
    margin-bottom: 1rem;
    background-color: white;
    transition: all 0.2s ease-in-out;
    position: relative;
}
.document-card:hover {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
.document-title {
    color: #2d3748;
    font-weight: bold;
    margin-bottom: 0.5rem;
    font-size: 1.1rem;
}
.document-content {
    color: #4a5568;
    font-size: 0.9rem;
    margin: 1rem 0;
    max-height: 300px;
    overflow-y: auto;
}
.document-info {
    color: #718096;
    font-size: 0.8rem;
    margin-top: 0.5rem;
}
.upload-zone {
    padding: 1.5rem;
    background-color: #f7fafc;
    border-radius: 0.5rem;
    margin-bottom: 2rem;
    display: flex;
    gap: 1rem;
    align-items: center;
}
.main-title {
    font-size: 2rem;
    margin-bottom: 1rem;
    color: #2d3748;
}
.section-title {
    font-size: 1.5rem;
    margin: 2rem 0 1rem 0;
    color: #2d3748;
}
.expand-button {
    color: #718096;
    opacity: 0.6;
    cursor: pointer;
    transition: opacity 0.2s;
    font-size: 0.9rem;
}
.expand-button:hover {
    opacity: 1;
    color: #2d3748;
}
</style>
""", unsafe_allow_html=True)

# Inicializar estado da sessão
if 'expanded_docs' not in st.session_state:
    st.session_state.expanded_docs = set()

# Título principal
st.markdown("<h1 class='main-title'>📚 BASE DE CONHECIMENTO</h1>", unsafe_allow_html=True)

# Seção de upload - Minimalista
st.markdown("<h2 class='section-title'>ADICIONAR DOCUMENTO</h2>", unsafe_allow_html=True)

# Descrição da funcionalidade
st.markdown("""
<div style='padding: 1rem; background-color: #f8fafc; border-radius: 0.5rem; margin-bottom: 1.5rem; border-left: 4px solid #3182ce;'>
    <p style='margin: 0; color: #4a5568; font-size: 0.95rem; line-height: 1.5;'>
        Aqui você pode contribuir com o conhecimento do assistente enviando arquivos de texto (.txt) contendo informações sobre o SENAI.
        Estes documentos serão utilizados como referência para responder às perguntas dos usuários no chat.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    uploaded_file = st.file_uploader("", type="txt")
with col2:
    if uploaded_file:
        if st.button("📤 Enviar"):
            try:
                content = uploaded_file.getvalue().decode("utf-8")
                filename = uploaded_file.name
                
                response = requests.post(
                    f"{API_URL}/documents",
                    json={"filename": filename, "content": content}
                )
                
                if response.status_code == 200:
                    st.success("✅ Documento adicionado!")
                    st.rerun()
                else:
                    st.error("Erro ao adicionar documento.")
            except Exception as e:
                st.error(f"Erro ao processar arquivo: {str(e)}")

# Lista de documentos
st.markdown("<h2 class='section-title'>Documentos Disponíveis</h2>", unsafe_allow_html=True)

try:
    response = requests.get(f"{API_URL}/documents")
    
    if response.status_code == 200:
        documents = response.json()
        
        if not documents:
            st.info("Nenhum documento encontrado.")
        
        # Grid de documentos
        for doc in documents:
            doc_id = f"doc_{doc['filename']}"
            is_expanded = doc_id in st.session_state.expanded_docs
            
            with st.container():
                col1, col2 = st.columns([11, 1])
                with col1:
                    st.markdown(f"""
                    <div class="document-card">
                        <div class="document-title">
                            {doc['filename']}
                        </div>
                        <div class="document-info">
                            Adicionado em: {datetime.fromisoformat(doc['added_at']).strftime('%d/%m/%Y %H:%M')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    expand_button = st.button(
                        "⬇️" if not is_expanded else "⬆️",
                        key=f"expand_{doc_id}",
                        help="Ler arquivo" if not is_expanded else "Recolher"
                    )
                    
                    if expand_button:
                        if is_expanded:
                            st.session_state.expanded_docs.remove(doc_id)
                        else:
                            st.session_state.expanded_docs.add(doc_id)
                        st.rerun()
                
                if is_expanded:
                    st.text_area(
                        "",
                        value=doc['content'],
                        height=300,
                        disabled=True,
                        key=f"content_{doc_id}"
                    )

except Exception as e:
    st.error(f"Erro ao carregar documentos: {str(e)}") 