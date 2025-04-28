import os
import streamlit as st
import requests
import json
from datetime import datetime

API_URL = os.getenv("API_URL", "https://deploy-streamlit-senai.onrender.com")

# Configuração da página
st.set_page_config(
    page_title="CHAT",
    page_icon="🤖",
    layout="wide"
)

# Configurar nome no menu lateral
st.sidebar._html = """
<style>
    [data-testid="stSidebarNav"] li:nth-child(1) div::before {
        content: "CHAT" !important;
    }
</style>
"""

# Estilo CSS personalizado
st.markdown("""
<style>
.chat-message {
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
    flex-direction: column;
}
.user-message {
    background-color: #e6f3ff;
    border-left: 5px solid #2b6cb0;
}
.assistant-message {
    background-color: #f0fff4;
    border-left: 5px solid #2f855a;
}
.context-info {
    font-size: 0.8rem;
    color: #666;
    margin-top: 0.5rem;
}
.token-info {
    font-size: 0.7rem;
    color: #888;
    text-align: right;
    margin-top: 0.3rem;
}
.prompt-suggestion {
    padding: 0.8rem;
    background-color: white;
    border: 1px solid #e2e8f0;
    border-radius: 0.5rem;
    margin-bottom: 0.5rem;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
}
.prompt-suggestion:hover {
    background-color: #f7fafc;
    border-color: #cbd5e0;
    transform: translateY(-1px);
}
.suggestions-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0;
}
.suggestions-title {
    color: #4a5568;
    font-size: 1rem;
    margin-bottom: 1rem;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# Título e descrição
st.title("💬 CHAT SENAI")
st.markdown("""
Este é um assistente que responde suas dúvidas sobre o SENAI usando documentos como referência.
""")

# Sugestões de prompts
if 'messages' not in st.session_state or not st.session_state.messages:
    st.markdown("<div class='suggestions-title'>🤔 Experimente perguntar:</div>", unsafe_allow_html=True)
    
    sugestoes = [
        "Quais são as áreas de atuação do SENAI?",
        "Como o SENAI contribui para a indústria brasileira?",
        "Que tipos de cursos o SENAI oferece?",
        "Como funciona a pesquisa aplicada no SENAI?",
        "Qual a história do SENAI?",
        "Como o SENAI apoia a inovação industrial?"
    ]
    
    st.markdown("<div class='suggestions-container'>", unsafe_allow_html=True)
    cols = st.columns(3)
    for idx, sugestao in enumerate(sugestoes):
        with cols[idx % 3]:
            if st.button(sugestao, key=f"sugestao_{idx}", use_container_width=True):
                # Adicionar pergunta ao histórico
                st.session_state.messages.append({"role": "user", "content": sugestao})
                
                # Mostrar indicador de "digitando"
                with st.status("Processando sua pergunta...", expanded=True) as status:
                    try:
                        # Fazer requisição para o backend
                        response = requests.post(
                            f"{API_URL}/question",
                            json={"question": sugestao}
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            
                            # Adicionar resposta ao histórico
                            st.session_state.messages.append({
                                "role": "assistant",
                                "response": data["answer"],
                                "context": data["context_used"],
                                "tokens": data["tokens_used"]
                            })
                            
                            status.update(label="Resposta gerada!", state="complete")
                            st.rerun()
                        else:
                            st.error("Erro ao processar a pergunta. Tente novamente.")
                            status.update(label="Erro ao processar", state="error")
                    
                    except Exception as e:
                        st.error(f"Erro ao conectar com o backend: {str(e)}")
                        status.update(label="Erro de conexão", state="error")
    st.markdown("</div>", unsafe_allow_html=True)

# Inicializar histórico de chat na sessão se não existir
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Função para extrair o nome do arquivo do conteúdo
def get_filename_from_content(content: str) -> str:
    # Aqui podemos adicionar mais mapeamentos conforme necessário
    content_map = {
        "O SENAI atua em mais de 28 áreas industriais": "senai_atuacao.txt",
        "O SENAI é o Serviço Nacional de Aprendizagem Industrial, uma instituição privada": "senai_descricao.txt",
        "O SENAI (Serviço Nacional de Aprendizagem Industrial) foi criado em 1942": "senai_historia.txt"
    }
    
    for key, filename in content_map.items():
        if content.startswith(key):
            return filename
    return "documento.txt"  # Nome genérico caso não encontre correspondência

# Exibir mensagens do histórico
for message in st.session_state.messages:
    with st.container():
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <div>🧑‍💻 <b>Você:</b> {message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <div>🤖 <b>Assistente:</b> {message["response"]}</div>
                <div class="context-info">
                    <b>Documentos consultados:</b><br>
                    {"<br>".join(f"📄 {get_filename_from_content(doc)}" for doc in message["context"])}
                </div>
                <div class="token-info">
                    Tokens utilizados: {message["tokens"]}
                </div>
            </div>
            """, unsafe_allow_html=True)

# Campo de entrada para a pergunta
question = st.chat_input("Digite sua pergunta sobre o SENAI...")

# Processar a pergunta quando enviada
if question:
    # Adicionar pergunta ao histórico
    st.session_state.messages.append({"role": "user", "content": question})
    
    # Mostrar a nova pergunta
    with st.container():
        st.markdown(f"""
        <div class="chat-message user-message">
            <div>🧑‍💻 <b>Você:</b> {question}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Mostrar indicador de "digitando"
    with st.status("Processando sua pergunta...", expanded=True) as status:
        try:
            # Fazer requisição para o backend
            response = requests.post(
                f"{API_URL}/question",
                json={"question": question}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Adicionar resposta ao histórico
                st.session_state.messages.append({
                    "role": "assistant",
                    "response": data["answer"],
                    "context": data["context_used"],
                    "tokens": data["tokens_used"]
                })
                
                # Mostrar a nova resposta
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <div>🤖 <b>Assistente:</b> {data["answer"]}</div>
                    <div class="context-info">
                        <b>Documentos consultados:</b><br>
                        {"<br>".join(f"📄 {get_filename_from_content(doc)}" for doc in data["context_used"])}
                    </div>
                    <div class="token-info">
                        Tokens utilizados: {data["tokens_used"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                status.update(label="Resposta gerada!", state="complete")
            else:
                st.error("Erro ao processar a pergunta. Tente novamente.")
                status.update(label="Erro ao processar", state="error")
        
        except Exception as e:
            st.error(f"Erro ao conectar com o backend: {str(e)}")
            status.update(label="Erro de conexão", state="error")

# Botão para limpar o histórico
if st.session_state.messages and st.button("Limpar Histórico"):
    st.session_state.messages = []
    st.rerun()
