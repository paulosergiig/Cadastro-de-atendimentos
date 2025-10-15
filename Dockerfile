# Use a imagem oficial do Python como imagem base
FROM python:3.11-slim-buster

# Define variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Define o diretório de trabalho
WORKDIR /app

# Instala as dependências
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do projeto
COPY . /app/

# Expõe a porta que o app vai rodar
EXPOSE 8000

# Comando para rodar a aplicação em produção
# Usamos waitress como um servidor de produção simples e eficaz para Windows/Linux
CMD ["waitress-serve", "--host", "0.0.0.0", "--port", "8000", "clinicmanager.wsgi:application"]