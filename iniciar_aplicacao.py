import os
import subprocess
import time
import webbrowser
import sys
from pathlib import Path

def obter_diretorio_base():
    """Retorna o diretório onde este script está localizado"""
    return Path(__file__).parent.absolute()

def iniciar_aplicacao():
    print("Iniciando aplicação SENAI...")
    
    diretorio_base = obter_diretorio_base()
    diretorio_backend = diretorio_base / "backend"
    diretorio_frontend = diretorio_base / "frontend"
    
    # Inicia o backend
    print("\nIniciando o backend...")
    backend_cmd = f"python -m uvicorn main:app --reload --port 8000"
    backend_processo = subprocess.Popen(backend_cmd, 
                                        cwd=diretorio_backend, 
                                        shell=True, 
                                        creationflags=subprocess.CREATE_NEW_CONSOLE)
    
    # Aguarda um pouco para o backend iniciar
    print("Aguardando o backend iniciar...")
    time.sleep(5)
    
    # Inicia o frontend
    print("Iniciando o frontend...")
    frontend_cmd = f"streamlit run 0_CHAT.py"
    frontend_processo = subprocess.Popen(frontend_cmd, 
                                        cwd=diretorio_frontend, 
                                        shell=True, 
                                        creationflags=subprocess.CREATE_NEW_CONSOLE)
    
    # Abre o navegador
    print("Abrindo navegador...")
    webbrowser.open("http://localhost:8501")
    
    print("\nAplicação iniciada!")
    print("Backend: http://localhost:8000/docs")
    print("Frontend: http://localhost:8501")
    
    print("\nPressione Ctrl+C para encerrar este script (os processos continuarão rodando)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nScript encerrado. As janelas do backend e frontend continuam abertas.")

if __name__ == "__main__":
    iniciar_aplicacao() 