@echo off
echo Iniciando aplicacao SENAI...
echo.

echo Iniciando o backend...
start cmd /k "cd %~dp0backend && python -m uvicorn main:app --reload --port 8000"

echo Aguardando o backend iniciar...
timeout /t 5 /nobreak > nul

echo Iniciando o frontend...
start cmd /k "cd %~dp0frontend && streamlit run 0_CHAT.py"

echo.
echo Aplicacao iniciada!
echo Backend: http://localhost:8000/docs
echo Frontend: http://localhost:8501
echo.
echo Pressione qualquer tecla para fechar esta janela...
pause > nul 