# Usa imagem Python leve
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos da subpasta `backend`
COPY backend/ /app/


# Instala dependências
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expõe porta padrão
EXPOSE 8000

# Comando de execução, assumindo que o main.py está no /app/
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
