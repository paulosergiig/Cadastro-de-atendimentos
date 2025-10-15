import os
import sys
from waitress import serve
from django.core.management import execute_from_command_line
from django.core.wsgi import get_wsgi_application
from django.core.management.utils import get_random_secret_key

def main():
    # Define o caminho base. Funciona tanto em modo de desenvolvimento quanto no executável.
    if getattr(sys, 'frozen', False):
        # Estamos rodando no executável
        BASE_DIR = os.path.dirname(sys.executable)
        sys.path.append(sys._MEIPASS)
    else:
        # Estamos rodando como um script normal
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # --- LÓGICA NOVA PARA CRIAR O .ENV ---
    env_path = os.path.join(BASE_DIR, '.env')
    if not os.path.exists(env_path):
        print("Arquivo .env não encontrado. Criando um novo com valores padrão.")
        secret_key = get_random_secret_key()
        env_content = (
            f"SECRET_KEY='{secret_key}'\n"
            "DEBUG=False\n"
            "ALLOWED_HOSTS=127.0.0.1,localhost\n"
        )
        with open(env_path, 'w') as f:
            f.write(env_content)
    # ------------------------------------

    # Adiciona o diretório do projeto ao path para encontrar o settings.py
    sys.path.insert(0, BASE_DIR)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinicmanager.settings')

    # Garante que as pastas de dados existam
    os.makedirs(os.path.join(BASE_DIR, 'db_data'), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, 'media'), exist_ok=True)

    # Verifica se o comando 'createsuperuser' foi passado
    if len(sys.argv) > 1 and sys.argv[1] == 'createsuperuser':
        print("Executando createsuperuser...")
        execute_from_command_line([sys.argv[0], 'migrate']) # Roda migrate antes de criar o usuário
        execute_from_command_line([sys.argv[0], 'createsuperuser'])
    else:
        print("Aplicando migrações do banco de dados...")
        execute_from_command_line([sys.argv[0], 'migrate'])
        
        print("Iniciando o servidor em http://localhost:8000...")
        application = get_wsgi_application()
        serve(application, host='127.0.0.1', port=8000)

if __name__ == '__main__':
    main()