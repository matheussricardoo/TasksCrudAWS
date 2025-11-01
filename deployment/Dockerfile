# Dockerfile - Tasks CRUD API
# Imagem otimizada para produção

FROM python:3.9-slim

# Informações do projeto
LABEL maintainer="Projeto AWS Learner Lab"
LABEL description="API REST para gerenciamento de tarefas"

# Diretório de trabalho
WORKDIR /app

# Copiar requirements primeiro (melhor cache do Docker)
COPY ../src/requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY ../src/app.py .

# Variáveis de ambiente padrão (serão sobrescritas no EC2)
ENV DB_HOST=localhost
ENV DB_USER=admin
ENV DB_PASSWORD=senha123
ENV DB_NAME=tasks_db
ENV PORT=8080

# Expor porta da API
EXPOSE 8080

# Health check (Docker verificará se o container está saudável)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')"

# Comando de inicialização (Gunicorn para produção)
# 2 workers = suficiente para projeto acadêmico
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "60", "app:app"]
