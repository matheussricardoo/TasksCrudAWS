
FROM python:3.12-slim

LABEL maintainer="Projeto AWS Learner Lab"
LABEL description="API REST para gerenciamento de tarefas"

WORKDIR /app

COPY src/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/app.py .

ENV DB_HOST=localhost
ENV DB_USER=admin
ENV DB_PASSWORD=senha123
ENV DB_NAME=tasks_db
ENV PORT=8080

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')"

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "60", "app:app"]
