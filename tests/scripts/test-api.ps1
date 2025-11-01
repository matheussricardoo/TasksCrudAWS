# Script Simplificado de Testes - Tasks CRUD API
$API_URL = "http://localhost:8080"

Write-Host "Testando API Tasks" -ForegroundColor Blue
Write-Host "API: $API_URL" -ForegroundColor Cyan
Write-Host ""

# 1. Health Check
Write-Host "1. Health Check" -ForegroundColor Green
curl "$API_URL/health"
Write-Host ""

# 2. Listar todas as tasks
Write-Host "2. Listar Todas as Tasks" -ForegroundColor Green
curl "$API_URL/tasks"
Write-Host ""

# 3. Buscar task específica
Write-Host "3. Buscar Task ID=1" -ForegroundColor Green
curl "$API_URL/tasks/1"
Write-Host ""

# 4. Criar nova task
Write-Host "4. Criar Nova Task" -ForegroundColor Green
$body = '{"title":"Teste PowerShell","description":"Task de teste","status":"pending","priority":"high"}'
curl -X POST "$API_URL/tasks" -H "Content-Type: application/json" -Body $body
Write-Host ""

# 5. Atualizar task
Write-Host "5. Atualizar Task ID=1" -ForegroundColor Green
$updateBody = '{"status":"in_progress"}'
curl -X PUT "$API_URL/tasks/1" -H "Content-Type: application/json" -Body $updateBody
Write-Host ""

# 6. Filtrar por status
Write-Host "6. Filtrar: status=pending" -ForegroundColor Green
curl "$API_URL/tasks?status=pending"
Write-Host ""

# 7. Filtrar por prioridade
Write-Host "7. Filtrar: priority=high" -ForegroundColor Green
curl "$API_URL/tasks?priority=high"
Write-Host ""

Write-Host "Testes concluídos!" -ForegroundColor Green
