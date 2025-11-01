#!/bin/bash

# ============================================================
# Script de Testes - Tasks CRUD API
# Testa todos os endpoints da API
# ============================================================

# Configurações
API_URL="${API_URL:-http://localhost:8080}"
BORDER="================================================"

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}${BORDER}${NC}"
echo -e "${BLUE}Testando API Tasks - CRUD Completo${NC}"
echo -e "${BLUE}${BORDER}${NC}"
echo -e "API URL: ${API_URL}"
echo ""

# ============================================================
# Função auxiliar para exibir testes
# ============================================================
test_endpoint() {
    local test_name=$1
    local method=$2
    local endpoint=$3
    local data=$4
    
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}TEST: ${test_name}${NC}"
    echo -e "${BLUE}${method} ${endpoint}${NC}"
    echo ""
    
    if [ -z "$data" ]; then
        curl -s -X ${method} "${API_URL}${endpoint}" | python -m json.tool || echo "Response não é JSON"
    else
        curl -s -X ${method} "${API_URL}${endpoint}" \
            -H "Content-Type: application/json" \
            -d "${data}" | python -m json.tool || echo "Response não é JSON"
    fi
    
    echo ""
    sleep 1
}

# ============================================================
# 1. Health Check
# ============================================================
test_endpoint "Health Check - Verificar API" "GET" "/health"

# ============================================================
# 2. Listar tarefas (inicial)
# ============================================================
test_endpoint "Listar Todas as Tarefas" "GET" "/tasks"

# ============================================================
# 3. Criar nova tarefa
# ============================================================
test_endpoint "Criar Nova Tarefa" "POST" "/tasks" \
'{
    "title": "Teste via Script",
    "description": "Tarefa criada pelo script de testes",
    "status": "pending",
    "priority": "high"
}'

# Capturar ID da tarefa criada (última tarefa)
TASK_ID=$(curl -s "${API_URL}/tasks" | python -c "import sys, json; data = json.load(sys.stdin); print(data['data'][0]['id'])" 2>/dev/null || echo "1")
echo -e "${YELLOW}ID da tarefa criada: ${TASK_ID}${NC}"
echo ""

# ============================================================
# 4. Buscar tarefa específica
# ============================================================
test_endpoint "Buscar Tarefa por ID (${TASK_ID})" "GET" "/tasks/${TASK_ID}"

# ============================================================
# 5. Atualizar tarefa
# ============================================================
test_endpoint "Atualizar Tarefa (${TASK_ID})" "PUT" "/tasks/${TASK_ID}" \
'{
    "status": "in_progress",
    "description": "Tarefa atualizada pelo script"
}'

# ============================================================
# 6. Listar tarefas com filtro (status)
# ============================================================
test_endpoint "Listar Tarefas - Filtro: status=pending" "GET" "/tasks?status=pending"

# ============================================================
# 7. Listar tarefas com filtro (priority)
# ============================================================
test_endpoint "Listar Tarefas - Filtro: priority=high" "GET" "/tasks?priority=high"

# ============================================================
# 8. Deletar tarefa
# ============================================================
test_endpoint "Deletar Tarefa (${TASK_ID})" "DELETE" "/tasks/${TASK_ID}"

# ============================================================
# 9. Verificar exclusão (deve retornar 404)
# ============================================================
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}TEST: Verificar Exclusão (deve retornar 404)${NC}"
echo -e "${BLUE}GET /tasks/${TASK_ID}${NC}"
echo ""

HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${API_URL}/tasks/${TASK_ID}")
if [ "$HTTP_STATUS" -eq 404 ]; then
    echo -e "${GREEN}Tarefa excluída com sucesso (HTTP 404)${NC}"
else
    echo -e "${RED}Erro: Tarefa ainda existe (HTTP ${HTTP_STATUS})${NC}"
fi
echo ""

# ============================================================
# 10. Listar tarefas (final)
# ============================================================
test_endpoint "Listar Todas as Tarefas (Final)" "GET" "/tasks"

# ============================================================
# Resumo
# ============================================================
echo -e "${BLUE}${BORDER}${NC}"
echo -e "${GREEN}Testes concluídos!${NC}"
echo -e "${BLUE}${BORDER}${NC}"
echo ""
echo -e "Endpoints testados:"
echo -e "   ✓ GET    /health"
echo -e "   ✓ GET    /tasks"
echo -e "   ✓ GET    /tasks/:id"
echo -e "   ✓ POST   /tasks"
echo -e "   ✓ PUT    /tasks/:id"
echo -e "   ✓ DELETE /tasks/:id"
echo -e "   ✓ GET    /tasks?status=X"
echo -e "   ✓ GET    /tasks?priority=X"
echo ""
echo -e "${YELLOW}Dica:${NC} Para testar contra API na AWS:"
echo -e "   export API_URL=http://seu-ip-ec2:8080"
echo -e "   bash scripts/test-api.sh"
echo ""
