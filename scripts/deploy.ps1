# ============================================================
# Script de Deploy - Tasks CRUD API (PowerShell)
# Deploy da aplicação no EC2 com Docker
# ============================================================

Write-Host "Iniciando deploy da API no EC2..." -ForegroundColor Blue
Write-Host "================================================" -ForegroundColor Blue

# ============================================================
# Variáveis de Ambiente (configure antes de executar)
# ============================================================

$DB_HOST = if ($env:DB_HOST) { $env:DB_HOST } else { "tasks-db.xxxxxxxxx.us-east-1.rds.amazonaws.com" }
$DB_USER = if ($env:DB_USER) { $env:DB_USER } else { "admin" }
$DB_PASSWORD = if ($env:DB_PASSWORD) { $env:DB_PASSWORD } else { "SuaSenhaSegura123" }
$DB_NAME = if ($env:DB_NAME) { $env:DB_NAME } else { "tasks_db" }

# ============================================================
# 1. Parar e remover container antigo (se existir)
# ============================================================

Write-Host "Parando container antigo..." -ForegroundColor Yellow
docker stop tasks-api 2>$null
docker rm tasks-api 2>$null

# ============================================================
# 2. Limpar imagens antigas (opcional)
# ============================================================

Write-Host "Limpando imagens antigas..." -ForegroundColor Yellow
docker image prune -f

# ============================================================
# 3. Build da nova imagem
# ============================================================

Write-Host "Construindo nova imagem Docker..." -ForegroundColor Yellow
docker build -t tasks-api:latest .

if ($LASTEXITCODE -eq 0) {
    Write-Host "Imagem construída com sucesso!" -ForegroundColor Green
} else {
    Write-Host "Erro ao construir imagem" -ForegroundColor Red
    exit 1
}

# ============================================================
# 4. Executar container
# ============================================================

Write-Host "Iniciando container..." -ForegroundColor Yellow
docker run -d `
  --name tasks-api `
  -p 8080:8080 `
  -e DB_HOST="$DB_HOST" `
  -e DB_USER="$DB_USER" `
  -e DB_PASSWORD="$DB_PASSWORD" `
  -e DB_NAME="$DB_NAME" `
  --restart unless-stopped `
  tasks-api:latest

if ($LASTEXITCODE -eq 0) {
    Write-Host "Container iniciado com sucesso!" -ForegroundColor Green
} else {
    Write-Host "Erro ao iniciar container" -ForegroundColor Red
    exit 1
}

# ============================================================
# 5. Verificar status
# ============================================================

Write-Host ""
Write-Host "Aguardando API inicializar (5 segundos)..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "Status do container:" -ForegroundColor Cyan
docker ps | Select-String "tasks-api"

Write-Host ""
Write-Host "Testando health check..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8080/health" -Method Get
    Write-Host "API respondendo: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "API ainda não respondeu" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Blue
Write-Host "Deploy concluído!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Blue
Write-Host ""
Write-Host "Informações úteis:" -ForegroundColor Cyan
Write-Host "   • API URL: http://localhost:8080"
Write-Host "   • Health: http://localhost:8080/health"
Write-Host "   • Logs: docker logs -f tasks-api"
Write-Host "   • Parar: docker stop tasks-api"
Write-Host ""
Write-Host "Para testar a API, execute:" -ForegroundColor Yellow
Write-Host "   .\scripts\test-api.ps1"
Write-Host ""
