<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0078D4&height=180&section=header&text=Guia%20de%20Implantação%20AWS&fontSize=40&fontColor=fff&animation=twinkling&fontAlignY=35&desc=Passo%20a%20Passo%20Completo%20para%20Deploy%20na%20Nuvem&descAlignY=55&descSize=16">

</div>

# Guia de Implantação AWS - API CRUD de Tarefas

<div align="center">

**Instruções completas para implantar a infraestrutura na AWS**

[![AWS](https://img.shields.io/badge/AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)](https://aws.amazon.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

</div>

## Visão Geral

Este guia fornece instruções passo a passo para implantar a infraestrutura completa da API CRUD de Tarefas na AWS. A implantação inclui EC2 com Docker, RDS MySQL, função Lambda e API Gateway.

### Infraestrutura de Referência Implantada

- **API Gateway**: `https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/prod`
- **Backend EC2**: `http://SEU-IP-PUBLICO:8080` (Flask containerizado)
- **RDS MySQL**: `tasks-db.xxxxxxxxxx.us-east-1.rds.amazonaws.com` (privado)
- **Função Lambda**: `tasks-report` (Python 3.9)

### Requisitos Implementados

| Requisito | Status |
|-----------|--------|
| Backend containerizado (EC2 + Docker) | Implementado |
| API REST/JSON (Flask) | Implementado |
| RDS MySQL em subnet privada | Implementado |
| API Gateway roteando CRUD para EC2 | Implementado |
| Função Lambda para /report | Implementado |
| Lambda consome API via HTTP (não RDS) | Implementado |
| Arquitetura segura e escalável | Implementado |

## Pré-requisitos

### Ferramentas Necessárias

- Conta AWS (Free Tier ou padrão)
- Docker Desktop instalado
- Git instalado
- Cliente SSH
- Cliente REST (Postman/Insomnia/curl)

### Verificar Instalações

```bash
# Docker
docker --version

# Git
git --version

# AWS CLI (opcional)
aws --version
```

## Fase 1: Instância EC2 com Docker

### Passo 1.1: Lançar Instância EC2

1. Acessar Console AWS → EC2 → Instâncias → Executar instância
2. Configurar:
   - **Nome**: tasks-api-server
   - **AMI**: Amazon Linux 2
   - **Tipo de instância**: t2.micro (elegível ao Free Tier)
   - **Par de chaves**: Criar novo ou usar existente (baixar arquivo .pem)
   - **Rede**: VPC padrão
   - **Grupo de segurança**: Criar novo com regras:
     - SSH (22) - Seu IP
     - TCP Personalizado (8080) - Qualquer lugar (ou IPs específicos)

3. **Armazenamento**: 8 GB gp2 (padrão)
4. Clicar em **Executar instância**
5. Aguardar até **Estado da instância** mostrar **Executando**
6. Copiar **Endereço IPv4 público**
7. **Importante**: Copiar também o **ID do Security Group** criado (será usado para configurar RDS na próxima fase)

### Passo 1.2: Conectar ao EC2

```bash
# Definir permissões corretas para o arquivo de chave
chmod 400 tasks-key.pem

# Conectar via SSH
ssh -i "tasks-key.pem" ec2-user@SEU-IP-PUBLICO-EC2
```

### Passo 1.3: Instalar Docker

```bash
# Atualizar sistema
sudo yum update -y

# Instalar Docker
sudo yum install docker -y

# Iniciar serviço Docker
sudo service docker start

# Adicionar usuário ao grupo docker
sudo usermod -a -G docker ec2-user

# Sair e entrar novamente para aplicar mudanças de grupo
exit
```

```bash
# Reconectar
ssh -i "tasks-key.pem" ec2-user@SEU-IP-PUBLICO-EC2

# Verificar instalação do Docker
docker --version
```

### Passo 1.4: Clonar Repositório

```bash
# Clonar projeto
git clone https://github.com/matheussricardoo/TasksCrudAWS.git
cd TasksCrudAWS
```

**Observação**: Não configure as variáveis de ambiente ainda — faremos isso após criar o RDS na próxima fase.

## Fase 2: Banco de Dados RDS MySQL

### Passo 2.1: Criar Instância RDS

1. Acessar Console AWS → RDS
2. Clicar em **Criar banco de dados**
3. Configurar:
   - **Mecanismo**: MySQL 8.0
   - **Modelo**: Free tier (ou Produção para uso real)
   - **Instância DB**: db.t3.micro
   - **Nome de usuário mestre**: `admin`
   - **Senha mestre**: Criar senha forte e **anotar** (será usada no .env)
   - **Nome do banco inicial**: `tasks_db`

4. Configuração de Rede:
   - **VPC**: Mesma VPC da instância EC2
   - **Grupo de sub-rede**: Padrão
   - **Acesso público**: **Não** (importante para segurança)
   - **Grupo de segurança VPC**: Criar novo

5. Configuração Adicional:
   - **Nome do banco inicial**: `tasks_db`
   - **Retenção de backup**: 7 dias (recomendado)
   - **Monitoramento**: Habilitar Enhanced Monitoring

6. Clicar em **Criar banco de dados**
7. Aguardar até o status mostrar **Disponível** (pode levar 5-10 minutos)
8. Copiar **Endpoint** (ex: `tasks-db.xxxxx.us-east-1.rds.amazonaws.com`) — **anote** para usar no .env

### Passo 2.2: Configurar Security Group do RDS

1. Console AWS → EC2 → Security Groups
2. Localizar o security group do RDS (criado automaticamente)
3. Clicar em **Editar regras de entrada**
4. Adicionar regra:
   - **Tipo**: MySQL/Aurora
   - **Protocolo**: TCP
   - **Porta**: 3306
   - **Origem**: Selecionar o **Security Group do EC2** (copiar ID do SG do EC2 criado na Fase 1)
   - **Descrição**: "Permitir EC2 acessar RDS"

5. Salvar regras

### Passo 2.3: Configurar Variáveis de Ambiente no EC2

Agora que o RDS está criado, volte ao EC2 e configure o arquivo `.env`:

```bash
# SSH para EC2 (se ainda não estiver conectado)
ssh -i "tasks-key.pem" ec2-user@SEU-IP-PUBLICO-EC2

# Entrar no diretório do projeto
cd TasksCrudAWS

# Criar arquivo .env
nano .env
```

Adicionar o seguinte conteúdo (substituir pelos valores reais):

```env
DB_HOST=seu-endpoint-rds.us-east-1.rds.amazonaws.com
DB_PORT=3306
DB_USER=admin
DB_PASSWORD=sua-senha-db-anotada
DB_NAME=tasks_db
```

Salvar e sair (Ctrl+O, Enter, Ctrl+X)

### Passo 2.4: Criar Schema do Banco de Dados

Conectar ao RDS a partir do EC2 e criar a tabela:

```bash
# Instalar cliente MySQL no EC2 (se ainda não estiver instalado)
sudo yum install mysql -y

# Conectar ao RDS
mysql -h seu-endpoint-rds.us-east-1.rds.amazonaws.com -u admin -p
# Digite a senha quando solicitado

# Criar schema (cole os comandos SQL)
CREATE DATABASE IF NOT EXISTS tasks_db;
USE tasks_db;

CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status ENUM('pending', 'in_progress', 'completed') DEFAULT 'pending',
    priority ENUM('low', 'medium', 'high') DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

# Inserir dados de exemplo (opcional)
INSERT INTO tasks (title, description, status, priority) VALUES
('Configurar AWS Infrastructure', 'Criar RDS, EC2, Security Groups e configurações de rede', 'completed', 'high'),
('Desenvolver API REST', 'Implementar endpoints CRUD em Flask com validações', 'completed', 'high'),
('Criar função Lambda', 'Desenvolver Lambda para geração de relatórios estatísticos', 'in_progress', 'high');

# Verificar dados inseridos
SELECT * FROM tasks;

# Sair do MySQL
exit;
```

### Passo 2.5: Construir e Executar Container Docker

Agora que o RDS está configurado e o `.env` criado, podemos construir e rodar o container:

```bash
# Ainda no diretório TasksCrudAWS no EC2
# Construir imagem Docker
docker build -t tasks-api:latest .

# Executar container
docker run -d \
  --name tasks-api \
  --restart unless-stopped \
  -p 8080:8080 \
  --env-file .env \
  tasks-api:latest

# Verificar se o container está rodando
docker ps

# Checar logs (verificar conexão com RDS)
docker logs tasks-api
```

### Passo 2.6: Testar API

```bash
# Testar do EC2
curl http://localhost:8080/tasks

# Testar do seu computador
curl http://SEU-IP-PUBLICO-EC2:8080/tasks
```

Resposta esperada:
```json
{
  "success": true,
  "count": 3,
  "data": [
    {
      "id": 1,
      "title": "Configurar AWS Infrastructure",
      "status": "completed",
      ...
    },
    ...
  ]
}
```

## Fase 3: Função Lambda

### Passo 3.1: Criar Função Lambda

1. Acessar Console AWS → Lambda
2. Clicar em **Criar função**
3. Configurar:
   - **Nome da função**: `tasks-report`
   - **Runtime**: Python 3.9
   - **Arquitetura**: x86_64
   - **Função de execução**: 
     - Para AWS Learner Lab: Usar **LabRole** existente
     - Para AWS padrão: Criar nova função com permissões básicas

4. Clicar em **Criar função**

### Passo 3.2: Adicionar Código da Função

1. Na aba **Código**, substituir o conteúdo por:

```python
import json
import urllib3
import os

API_URL = os.getenv('API_URL', 'http://localhost:8080/tasks')
http = urllib3.PoolManager()

def lambda_handler(event, context):
    """
    Função Lambda para gerar estatísticas de tarefas.
    Consome a API do EC2 via HTTP e calcula estatísticas agregadas.
    """
    
    try:
        print(f"Gerando relatório de tarefas...")
        print(f"URL da API: {API_URL}")
        
        # Fazer requisição HTTP para API do EC2
        response = http.request('GET', API_URL, timeout=10.0)
        
        if response.status != 200:
            raise Exception(f"API retornou status {response.status}")
        
        # Parsear resposta
        data = json.loads(response.data.decode('utf-8'))
        tasks = data.get('data', [])
        
        # Calcular estatísticas
        total = len(tasks)
        by_status = {}
        by_priority = {}
        
        for task in tasks:
            status = task.get('status', 'unknown')
            priority = task.get('priority', 'unknown')
            
            by_status[status] = by_status.get(status, 0) + 1
            by_priority[priority] = by_priority.get(priority, 0) + 1
        
        completed = by_status.get('completed', 0)
        completion_rate = round((completed / total * 100), 2) if total > 0 else 0
        
        # Construir relatório
        report = {
            'total_tasks': total,
            'by_status': by_status,
            'by_priority': by_priority,
            'completion_rate': completion_rate,
            'completion_percentage': f"{completion_rate}%"
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET,OPTIONS'
            },
            'body': json.dumps({
                'success': True,
                'report': report,
                'timestamp': context.aws_request_id if context else 'local-test'
            })
        }
        
    except Exception as e:
        print(f"Erro ao gerar relatório: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': False,
                'error': str(e)
            })
        }
```

2. Clicar em **Deploy** para salvar mudanças

### Passo 3.3: Configurar Variáveis de Ambiente

1. Ir para aba **Configuração** → **Variáveis de ambiente**
2. Clicar em **Editar**
3. Adicionar variável:
   - **Chave**: `API_URL`
   - **Valor**: `http://SEU-IP-PUBLICO-EC2:8080/tasks`

4. Salvar mudanças

### Passo 3.4: Ajustar Timeout

1. Ir para aba **Configuração** → **Configuração geral**
2. Clicar em **Editar**
3. Definir **Tempo limite**: 30 segundos
4. Salvar mudanças

### Passo 3.5: Testar Função Lambda

1. Ir para aba **Teste**
2. Criar novo evento de teste:
   - **Nome do evento**: `test-report`
   - **Modelo**: `hello-world` (padrão)

3. Clicar em **Testar**
4. Verificar se a resposta mostra estatísticas

Resposta esperada:
```json
[
  {
    "category": "doce",
    "created_at": "Thu, 06 Nov 2025 23:44:25 GMT",
    "flavor": "chocolate",
    "id": 1,
    "name": "Brigadeiro Gourmet",
    "price": 3.5,
    "stock": 25,
    "updated_at": "Thu, 06 Nov 2025 23:44:25 GMT"
  },
  {
    "category": "doce",
    "created_at": "Thu, 06 Nov 2025 23:44:25 GMT",
    "flavor": "coco",
    "id": 2,
    "name": "Beijinho Premium",
    "price": 3.5,
    "stock": 20,
    "updated_at": "Thu, 06 Nov 2025 23:44:25 GMT"
  },
  {
    "category": "torta",
    "created_at": "Thu, 06 Nov 2025 23:44:25 GMT",
    "flavor": "chocolate",
    "id": 3,
    "name": "Torta de Chocolate",
    "price": 45.0,
    "stock": 5,
    "updated_at": "Thu, 06 Nov 2025 23:44:25 GMT"
  },
  {
    "category": "torta",
    "created_at": "Thu, 06 Nov 2025 23:44:25 GMT",
    "flavor": "morango",
    "id": 4,
    "name": "Torta de Morango",
    "price": 48.0,
    "stock": 3,
    "updated_at": "Thu, 06 Nov 2025 23:44:25 GMT"
  },
  {
    "category": "doce",
    "created_at": "Thu, 06 Nov 2025 23:44:25 GMT",
    "flavor": "coco",
    "id": 5,
    "name": "Quindim",
    "price": 4.0,
    "stock": 15,
    "updated_at": "Thu, 06 Nov 2025 23:44:25 GMT"
  },
  {
    "category": "doce",
    "created_at": "Thu, 06 Nov 2025 23:44:25 GMT",
    "flavor": "caramelo",
    "id": 6,
    "name": "Pudim de Leite",
    "price": 35.0,
    "stock": 8,
    "updated_at": "Thu, 06 Nov 2025 23:44:25 GMT"
  },
  {
    "category": "torta",
    "created_at": "Thu, 06 Nov 2025 23:44:25 GMT",
    "flavor": "lim\u00e3o",
    "id": 7,
    "name": "Torta de Lim\u00e3o",
    "price": 42.0,
    "stock": 2,
    "updated_at": "Thu, 06 Nov 2025 23:44:25 GMT"
  },
  {
    "category": "doce",
    "created_at": "Thu, 06 Nov 2025 23:44:25 GMT",
    "flavor": "chocolate",
    "id": 8,
    "name": "Trufa de Chocolate",
    "price": 2.5,
    "stock": 50,
    "updated_at": "Thu, 06 Nov 2025 23:44:25 GMT"
  }
```

## Fase 4: API Gateway

### Passo 4.1: Criar REST API

1. Acessar Console do API Gateway
2. Clicar em **Criar API**
3. Escolher **API REST** (não privada)
4. Configurar:
   - **Nome da API**: TasksAPI
   - **Tipo de endpoint**: Regional

5. Clicar em **Criar API**

### Passo 4.2: Criar Recursos

#### Recurso: /tasks

1. Clicar em **Ações** → **Criar recurso**
2. Configurar:
   - **Nome do recurso**: tasks
   - **Caminho do recurso**: /tasks
   - Habilitar **CORS** se necessário

3. Clicar em **Criar recurso**

#### Recurso: /tasks/{id}

1. Selecionar recurso `/tasks`
2. Clicar em **Ações** → **Criar recurso**
3. Configurar:
   - **Nome do recurso**: {id}
   - **Caminho do recurso**: /tasks/{id}

4. Clicar em **Criar recurso**

#### Recurso: /report

1. Selecionar raiz `/`
2. Clicar em **Ações** → **Criar recurso**
3. Configurar:
   - **Nome do recurso**: report
   - **Caminho do recurso**: /report

4. Clicar em **Criar recurso**

### Passo 4.3: Criar Métodos

#### Método: GET /tasks

1. Selecionar recurso `/tasks`
2. Clicar em **Ações** → **Criar método** → **GET**
3. Configurar:
   - **Tipo de integração**: HTTP
   - **Método HTTP**: GET
   - **URL do endpoint**: `http://SEU-IP-PUBLICO-EC2:8080/tasks`
   - **Manuseio de conteúdo**: Passthrough

4. Salvar

#### Método: POST /tasks

1. Selecionar recurso `/tasks`
2. Clicar em **Ações** → **Criar método** → **POST**
3. Configurar:
   - **Tipo de integração**: HTTP
   - **Método HTTP**: POST
   - **URL do endpoint**: `http://SEU-IP-PUBLICO-EC2:8080/tasks`

4. Salvar

#### Método: GET /tasks/{id}

1. Selecionar recurso `/tasks/{id}`
2. Clicar em **Ações** → **Criar método** → **GET**
3. Configurar:
   - **Tipo de integração**: HTTP
   - **Método HTTP**: GET
   - **URL do endpoint**: `http://SEU-IP-PUBLICO-EC2:8080/tasks/{id}`

4. Salvar

#### Método: PUT /tasks/{id}

1. Selecionar recurso `/tasks/{id}`
2. Clicar em **Ações** → **Criar método** → **PUT**
3. Configurar similarmente ao GET

#### Método: DELETE /tasks/{id}

1. Selecionar recurso `/tasks/{id}`
2. Clicar em **Ações** → **Criar método** → **DELETE**
3. Configurar similarmente ao GET

#### Método: GET /report (Lambda)

1. Selecionar recurso `/report`
2. Clicar em **Ações** → **Criar método** → **GET**
3. Configurar:
   - **Tipo de integração**: Função Lambda
   - **Região da Lambda**: Sua região (ex: us-east-1)
   - **Função Lambda**: tasks-report

4. Confirmar prompt de permissão
5. Salvar

### Passo 4.4: Implantar API

1. Clicar em **Ações** → **Implantar API**
2. Configurar:
   - **Estágio de implantação**: Novo estágio
   - **Nome do estágio**: prod
   - **Descrição**: Implantação de produção

3. Clicar em **Implantar**
4. Copiar **URL de invocação** (ex: `https://xxxxxxxx.execute-api.us-east-1.amazonaws.com/prod`)

## Fase 5: Testes

### Testar Todos os Endpoints

```bash
# Definir URL da API
API_URL="https://sua-url-api-gateway.amazonaws.com/prod"

# Testar GET /tasks
curl $API_URL/tasks

# Testar POST /tasks
curl -X POST $API_URL/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Tarefa Teste","description":"Testando API","priority":"high","status":"pending"}'

# Testar GET /tasks/{id}
curl $API_URL/tasks/1

# Testar PUT /tasks/{id}
curl -X PUT $API_URL/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status":"completed"}'

# Testar DELETE /tasks/{id}
curl -X DELETE $API_URL/tasks/1

# Testar GET /report (Lambda)
curl $API_URL/report
```

### Verificar Resultados

Todos os endpoints devem retornar HTTP 200 e respostas JSON apropriadas.

## Solução de Problemas

### Problemas Comuns

#### Falha na Conexão com RDS

- Verificar se Security Group permite IP do EC2
- Checar se endpoint do RDS está correto
- Verificar credenciais no arquivo .env

#### API do EC2 Não Responde

```bash
# Checar status do container Docker
docker ps

# Checar logs do container
docker logs tasks-api

# Reiniciar container se necessário
docker restart tasks-api
```

#### Timeout da Lambda

- Verificar variável de ambiente API_URL
- Checar logs de execução da Lambda no CloudWatch
- Garantir que EC2 está acessível da Lambda

#### Erro 502 no API Gateway

- Verificar se IP público do EC2 não mudou
- Atualizar URLs de integração do API Gateway
- Re-implantar API

## Manutenção

### Atualizar Código da Aplicação

```bash
# SSH para EC2
ssh -i "tasks-key.pem" ec2-user@SEU-IP-EC2

# Baixar últimas mudanças
cd TasksCrudAWS
git pull origin main

# Reconstruir e reiniciar container
docker build -t tasks-api:latest .
docker stop tasks-api
docker rm tasks-api
docker run -d \
  --name tasks-api \
  --restart unless-stopped \
  -p 8080:8080 \
  --env-file .env \
  tasks-api:latest
```

### Monitorar Logs

```bash
# Logs do Docker
docker logs -f tasks-api

# Logs da Lambda (usando AWS CLI)
aws logs tail /aws/lambda/tasks-report --follow
```

### Backup do Banco de Dados

```bash
# Criar backup
mysqldump -h seu-endpoint-rds.amazonaws.com -u admin -p tasks_db > backup.sql

# Restaurar backup
mysql -h seu-endpoint-rds.amazonaws.com -u admin -p tasks_db < backup.sql
```

## Otimização de Custos

### Uso do Free Tier

- EC2 t2.micro: 750 horas/mês (grátis por 12 meses)
- RDS db.t3.micro: 750 horas/mês (grátis por 12 meses)
- Lambda: 1M requisições/mês (sempre grátis)
- API Gateway: 1M requisições/mês (grátis por 12 meses)

### Parar Recursos Quando Não Necessário

```bash
# Parar instância EC2 (via console ou CLI)
aws ec2 stop-instances --instance-ids i-xxxxx

# Parar instância RDS (via console ou CLI)
aws rds stop-db-instance --db-instance-identifier tasks-db
```

## Checklist de Segurança

- [ ] RDS em subnet privada (sem acesso público)
- [ ] Security Group do EC2 restringe SSH para IPs específicos
- [ ] Senha forte do banco de dados
- [ ] Variáveis de ambiente para credenciais (sem hardcode)
- [ ] Patches de segurança regulares (yum update)
- [ ] Throttling do API Gateway configurado
- [ ] Alarmes do CloudWatch para atividade incomum
- [ ] Backups regulares habilitados


## Próximos Passos

1. Configurar domínio personalizado para API Gateway
2. Adicionar certificado SSL/TLS
3. Implementar autenticação (JWT/OAuth)
4. Configurar alarmes do CloudWatch
5. Configurar Auto Scaling para EC2
6. Implementar pipeline CI/CD

## Suporte

Para problemas ou perguntas:
- GitHub Issues: https://github.com/matheussricardoo/TasksCrudAWS/issues

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0078D4&height=120&section=footer"/>

</div>


