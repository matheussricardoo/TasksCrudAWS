#!/bin/bash

# ============================================================
# Script de Deploy - Tasks CRUD API
# Deploy da aplicação no EC2 com Docker
# ============================================================

set -e  # Para execução em caso de erro

echo "Iniciando deploy da API no EC2..."
echo "================================================"

# ============================================================
# Variáveis de Ambiente (configure antes de executar)
# ============================================================

# Informações do banco RDS (obtenha do console AWS)
export DB_HOST="${DB_HOST:-tasks-db.xxxxxxxxx.us-east-1.rds.amazonaws.com}"
export DB_USER="${DB_USER:-admin}"
export DB_PASSWORD="${DB_PASSWORD:-SuaSenhaSegura123}"
export DB_NAME="${DB_NAME:-tasks_db}"

# ============================================================
# 1. Parar e remover container antigo (se existir)
# ============================================================

echo "Parando container antigo..."
docker stop tasks-api 2>/dev/null || echo "Nenhum container rodando"
docker rm tasks-api 2>/dev/null || echo "Nenhum container para remover"

# ============================================================
# 2. Limpar imagens antigas (opcional)
# ============================================================

echo "Limpando imagens antigas..."
docker image prune -f

# ============================================================
# 3. Build da nova imagem
# ============================================================

echo "Construindo nova imagem Docker..."
docker build -t tasks-api:latest .

if [ $? -eq 0 ]; then
    echo "Imagem construída com sucesso!"
else
    echo "Erro ao construir imagem"
    exit 1
fi

# ============================================================
# 4. Executar container
# ============================================================

echo "Iniciando container..."
docker run -d \
  --name tasks-api \
  -p 8080:8080 \
  -e DB_HOST="${DB_HOST}" \
  -e DB_USER="${DB_USER}" \
  -e DB_PASSWORD="${DB_PASSWORD}" \
  -e DB_NAME="${DB_NAME}" \
  --restart unless-stopped \
  tasks-api:latest

if [ $? -eq 0 ]; then
    echo "Container iniciado com sucesso!"
else
    echo "Erro ao iniciar container"
    exit 1
fi

# ============================================================
# 5. Verificar status
# ============================================================

echo ""
echo "Aguardando API inicializar (5 segundos)..."
sleep 5

echo ""
echo "Status do container:"
docker ps | grep tasks-api

echo ""
echo "Testando health check..."
curl -f http://localhost:8080/health || echo "API ainda não respondeu"

echo ""
echo "================================================"
echo "Deploy concluído!"
echo "================================================"
echo ""
echo "Informações úteis:"
echo "   • API URL: http://localhost:8080"
echo "   • Health: http://localhost:8080/health"
echo "   • Logs: docker logs -f tasks-api"
echo "   • Parar: docker stop tasks-api"
echo ""
echo "Para testar a API, execute:"
echo "   bash scripts/test-api.sh"
echo ""
