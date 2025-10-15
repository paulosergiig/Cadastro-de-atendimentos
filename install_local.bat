@echo off
echo Criando ambiente virtual...
python -m venv .venv

echo Ativando ambiente virtual e instalando dependencias...
call .\.venv\Scripts\activate.bat && pip install -r requirements.txt

echo.
echo Copiando .env.example para .env...
copy .env.example .env

echo.
echo ======================================================
echo  Instalacao concluida!
echo  1. Edite o arquivo .env com suas configuracoes.
echo  2. Rode 'run_dev.bat' para iniciar o servidor.
echo ======================================================
pause