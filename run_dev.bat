@echo off
echo Ativando ambiente virtual...
call .\.venv\Scripts\activate.bat

echo Aplicando migracoes do banco de dados...
python manage.py migrate

echo.
echo ===============================================
echo   Iniciando servidor de desenvolvimento...
echo   Acesse em: http://127.0.0.1:8000
echo   Pressione CTRL+C para parar o servidor.
echo ===============================================
python manage.py runserver