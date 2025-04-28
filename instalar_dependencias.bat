@echo off
echo Instalando dependencias da aplicacao SENAI...
echo.

echo Instalando dependencias do backend...
cd %~dp0backend
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ERRO: Falha ao instalar dependencias do backend!
    pause
    exit /b 1
)

echo.
echo Instalando dependencias do frontend...
cd %~dp0frontend
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ERRO: Falha ao instalar dependencias do frontend!
    pause
    exit /b 1
)

echo.
echo Todas as dependencias foram instaladas com sucesso!
echo Agora voce pode executar o arquivo 'iniciar_aplicacao.bat' para iniciar a aplicacao.
echo.
pause 