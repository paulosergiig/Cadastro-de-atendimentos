# ClinicManager - Software de Gestão de Pacientes

Bem-vindo ao ClinicManager! Este é um sistema completo para gerenciamento de pacientes, fichas de evolução, anamnese e relatórios, projetado para ser usado em clínicas por terapeutas e supervisores.

Este guia contém tudo o que você precisa para instalar e rodar o sistema, tanto em um ambiente de desenvolvimento (para programadores) quanto em um computador na clínica (para usuários finais).

## Seção 1: Instalação na Clínica (Recomendado: Docker)

Este método é o mais simples e seguro para usar o sistema na clínica. Ele usa uma tecnologia chamada Docker para rodar o programa de forma isolada e sem a necessidade de instalar Python ou outras dependências complexas no seu computador.

**Pré-requisitos:**
*   Um computador com Windows 10 ou 11.
*   Acesso à Internet para a instalação inicial.

---

### Passo-a-Passo (Copiar e Colar)

**1. Instale o Docker Desktop:**
   *   Vá para o site oficial do Docker: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
   *   Baixe o instalador para Windows e siga as instruções na tela. Pode ser necessário reiniciar o computador.
   *   Após a instalação, abra o Docker Desktop. Espere até que ele mostre um ícone verde na barra de tarefas, indicando que está pronto.

**2. Copie os Arquivos do Projeto:**
   *   Crie uma pasta em um local fácil de encontrar, por exemplo, `C:\ClinicManager`.
   *   Copie todos os arquivos do projeto (que você recebeu neste pacote) para dentro da pasta `C:\ClinicManager`.

**3. Configure as Variáveis de Ambiente:**
   *   Na pasta `C:\ClinicManager`, encontre o arquivo `.env.example`.
   *   Faça uma cópia deste arquivo e renomeie a cópia para `.env`.
   *   Abra o arquivo `.env` com o Bloco de Notas e altere as seguintes linhas:
     ```
     # ATENÇÃO: Altere esta chave para algo longo e secreto!
     SECRET_KEY='django-insecure-troque-esta-chave-secreta-agora'

     # Mude para False quando estiver em produção na clínica
     DEBUG=False

     # Coloque o endereço do computador onde o sistema vai rodar
     # Se for acessar apenas no próprio computador, use '127.0.0.1'
     # Se for acessar de outros computadores na mesma rede, use o IP do computador, ex: '192.168.1.10,127.0.0.1'
     ALLOWED_HOSTS=127.0.0.1,localhost
     ```
   *   **IMPORTANTE:** A `SECRET_KEY` deve ser trocada por qualquer texto longo e aleatório. Você pode usar um gerador online se desejar. `DEBUG` **DEVE** ser `False` para segurança.

**4. Inicie o Sistema:**
   *   Abra o **PowerShell** do Windows (procure por "PowerShell" no Menu Iniciar).
   *   Digite os comandos abaixo, um de cada vez, e pressione Enter após cada um.

     ```powershell
     # 1. Navegue até a pasta do projeto
     cd C:\ClinicManager

     # 2. Construa e inicie o sistema em segundo plano
     docker-compose up -d --build
     ```
   *   A primeira vez que rodar este comando pode demorar alguns minutos.
   *   Espere o processo terminar.

**5. Crie o Usuário Supervisor (Administrador):**
   *   Ainda no PowerShell, execute o comando abaixo para criar o primeiro usuário, que será o administrador do sistema.

     ```powershell
     docker-compose exec web python manage.py createsuperuser
     ```
   *   Você será solicitado a criar um **nome de usuário** (ex: `admin`), um **email** (opcional) e uma **senha**. Crie uma senha forte!

**Pronto!** O sistema está no ar.
*   **Acesso:** Abra seu navegador de internet (Chrome, Firefox, etc.) e acesse `http://localhost:8000`.
*   **Login:** Use o usuário e senha que você acabou de criar.

**Como parar o sistema:**
*   Abra o PowerShell na pasta `C:\ClinicManager` e digite: `docker-compose down`

**Como reiniciar o sistema:**
*   Abra o PowerShell na pasta `C:\ClinicManager` e digite: `docker-compose up -d`

---

## Seção 2: Backup e Restauração

É **CRUCIAL** fazer backups regulares dos dados dos pacientes.

**Para fazer um backup:**
1.  Acesse a pasta do projeto (`C:\ClinicManager`).
2.  Copie os seguintes itens para um local seguro (pen drive, HD externo, nuvem):
    *   A pasta `db_data/` (contém o banco de dados).
    *   A pasta `media_data/` (contém os laudos e arquivos enviados).

**Para restaurar um backup:**
1.  Pare o sistema (`docker-compose down`).
2.  Substitua as pastas `db_data/` e `media_data/` pelas cópias do seu backup.
3.  Inicie o sistema novamente (`docker-compose up -d`).

---

## Seção 3: Instalação para Desenvolvimento (Windows + VSCode)

Esta seção é para usuários avançados ou programadores que desejam modificar o código.

**Pré-requisitos:**
*   [Python 3.11+](https://www.python.org/downloads/) (Marque a opção "Add Python to PATH" durante a instalação).
*   [Visual Studio Code](https://code.visualstudio.com/).

**Passo-a-Passo (PowerShell):**

1.  **Clone ou copie o projeto** para uma pasta.
2.  **Abra o PowerShell** nesta pasta.

3.  **Crie e ative um ambiente virtual:**
    ```powershell
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    ```

4.  **Instale as dependências:**
    ```powershell
    pip install -r requirements.txt
    ```

5.  **Configure o arquivo `.env`:**
    *   Copie `.env.example` para `.env`.
    *   Altere as variáveis como explicado na Seção 1. Para desenvolvimento, você pode manter `DEBUG=True`.

6.  **Aplique as migrações do banco de dados:**
    ```powershell
    python manage.py migrate
    ```

7.  **Crie um superusuário:**
    ```powershell
    python manage.py createsuperuser
    ```

8.  **(Opcional) Carregue dados de exemplo:**
    ```powershell
    python manage.py loaddata fixtures/initial_data.json
    ```

9.  **Inicie o servidor de desenvolvimento:**
    ```powershell
    python manage.py runserver
    ```
    *   Acesse o sistema em `http://127.0.0.1:8000`.

---

## Seção 4: Alternativa sem Docker (Implantação na Clínica)

Use este método apenas se não for possível instalar o Docker.

1.  **Instale o Python 3.11+** no computador da clínica (marque "Add Python to PATH").
2.  **Copie os arquivos do projeto** para `C:\ClinicManager`.
3.  **Abra o PowerShell** como Administrador.
4.  **Navegue até a pasta:** `cd C:\ClinicManager`.
5.  **Instale as dependências:** `pip install -r requirements.txt`.
6.  **Configure o arquivo `.env`** como na Seção 1 (garanta `DEBUG=False`).
7.  **Execute as migrações e crie o superusuário** (veja comandos na Seção 3).
8.  **Para rodar o sistema em modo de produção (com Waitress):**
    ```powershell
    waitress-serve --host 0.0.0.0 --port 8000 clinicmanager.wsgi:application
    ```
    *   O sistema estará acessível na rede local pelo IP do computador, na porta 8000.
    *   **Atenção:** A janela do PowerShell precisa ficar aberta. Fechá-la irá derrubar o sistema. Para rodar como um serviço do Windows, são necessários passos mais avançados.

---
## Seção 5: Usando com PostgreSQL (Avançado)

Para usar PostgreSQL em vez de SQLite (recomendado para instalações maiores):
1.  Modifique o `docker-compose.yml` para incluir um serviço de banco de dados Postgres.
2.  Instale o driver do psycopg2: `pip install psycopg2-binary`.
3.  Altere a configuração `DATABASES` em `clinicmanager/settings.py` para:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'clinicdb',
            'USER': 'clinicuser',
            'PASSWORD': 'strongpassword',
            'HOST': 'db', # ou o endereço do seu servidor de banco de dados
            'PORT': '5432',
        }
    }
    ```