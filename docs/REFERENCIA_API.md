<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=00C853&height=180&section=header&text=Referência%20da%20API&fontSize=45&fontColor=fff&animation=twinkling&fontAlignY=35&desc=Documentação%20Completa%20dos%20Endpoints%20REST&descAlignY=55&descSize=16">

</div>

# Referência da API - API CRUD de Tarefas

<div align="center">

**API RESTful para gerenciamento de tarefas com operações CRUD completas**

[![REST API](https://img.shields.io/badge/REST-API-green?style=for-the-badge)](https://restfulapi.net/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![AWS Lambda](https://img.shields.io/badge/AWS_Lambda-FF9900?style=for-the-badge&logo=awslambda&logoColor=white)](https://aws.amazon.com/lambda/)
[![JSON](https://img.shields.io/badge/JSON-000000?style=for-the-badge&logo=json&logoColor=white)](https://www.json.org/)

</div>

## Visão Geral

API RESTful para gerenciamento de tarefas com operações CRUD completas. Desenvolvida com Flask e Python, implantada na infraestrutura AWS.

**URL Base (Produção)**: `https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/prod`  
**URL Base (Local)**: `http://localhost:8080`

## Autenticação

A versão atual não requer autenticação. Todos os endpoints são publicamente acessíveis.

## Endpoints

### Coleção de Tarefas

#### Listar Todas as Tarefas

```http
GET /tasks
```

Retorna uma lista de todas as tarefas no sistema.

**Parâmetros de Consulta:**

| Parâmetro | Tipo | Descrição | Obrigatório |
|-----------|------|-----------|-------------|
| `status` | string | Filtrar por status (`pending`, `in_progress`, `completed`) | Não |
| `priority` | string | Filtrar por prioridade (`low`, `medium`, `high`) | Não |

**Resposta:**

```json
{
  "success": true,
  "count": 9,
  "data": [
    {
      "id": 1,
      "title": "Configurar Infraestrutura AWS",
      "description": "Criar RDS, EC2, Security Groups e configurações de rede",
      "status": "completed",
      "priority": "high",
      "created_at": "2025-10-31T22:56:45Z",
      "updated_at": "2025-10-31T22:56:45Z"
    }
  ]
}
```

**Códigos de Status:**

- `200 OK` - Sucesso
- `500 Internal Server Error` - Erro de conexão com banco de dados

#### Obter Tarefa Específica

```http
GET /tasks/{id}
```

Retorna detalhes de uma tarefa específica.

**Parâmetros de Caminho:**

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `id` | integer | ID da tarefa |

**Resposta:**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Configurar Infraestrutura AWS",
    "description": "Criar RDS, EC2, Security Groups e configurações de rede",
    "status": "completed",
    "priority": "high",
    "created_at": "2025-10-31T22:56:45Z",
    "updated_at": "2025-10-31T22:56:45Z"
  }
}
```

**Códigos de Status:**

- `200 OK` - Sucesso
- `404 Not Found` - Tarefa não encontrada
- `500 Internal Server Error` - Erro no banco de dados

#### Criar Tarefa

```http
POST /tasks
```

Cria uma nova tarefa.

**Corpo da Requisição:**

```json
{
  "title": "Implementar Pipeline CI/CD",
  "description": "Configurar CodePipeline e CodeBuild",
  "status": "pending",
  "priority": "medium"
}
```

**Validação de Campos:**

| Campo | Tipo | Obrigatório | Restrições |
|-------|------|-------------|------------|
| `title` | string | Sim | Máximo 200 caracteres |
| `description` | string | Não | Campo de texto |
| `status` | enum | Não | `pending` (padrão), `in_progress`, `completed` |
| `priority` | enum | Não | `low`, `medium` (padrão), `high` |

**Resposta:**

```json
{
  "success": true,
  "message": "Tarefa criada com sucesso",
  "data": {
    "id": 10,
    "title": "Implementar Pipeline CI/CD",
    "description": "Configurar CodePipeline e CodeBuild",
    "status": "pending",
    "priority": "medium",
    "created_at": "2025-11-01T00:00:44Z",
    "updated_at": "2025-11-01T00:00:44Z"
  }
}
```

**Códigos de Status:**

- `201 Created` - Sucesso
- `400 Bad Request` - Entrada inválida
- `500 Internal Server Error` - Erro no banco de dados

#### Atualizar Tarefa

```http
PUT /tasks/{id}
```

Atualiza uma tarefa existente. Apenas os campos fornecidos serão atualizados.

**Parâmetros de Caminho:**

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `id` | integer | ID da tarefa |

**Corpo da Requisição (atualização parcial suportada):**

```json
{
  "status": "in_progress",
  "priority": "high"
}
```

**Resposta:**

```json
{
  "success": true,
  "message": "Tarefa atualizada com sucesso",
  "data": {
    "id": 10,
    "title": "Implementar Pipeline CI/CD",
    "description": "Configurar CodePipeline e CodeBuild",
    "status": "in_progress",
    "priority": "high",
    "created_at": "2025-11-01T00:00:44Z",
    "updated_at": "2025-11-01T00:05:12Z"
  }
}
```

**Códigos de Status:**

- `200 OK` - Sucesso
- `404 Not Found` - Tarefa não encontrada
- `400 Bad Request` - Entrada inválida
- `500 Internal Server Error` - Erro no banco de dados

#### Deletar Tarefa

```http
DELETE /tasks/{id}
```

Deleta permanentemente uma tarefa.

**Parâmetros de Caminho:**

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `id` | integer | ID da tarefa |

**Resposta:**

```json
{
  "success": true,
  "message": "Tarefa deletada com sucesso"
}
```

**Códigos de Status:**

- `200 OK` - Sucesso
- `404 Not Found` - Tarefa não encontrada
- `500 Internal Server Error` - Erro no banco de dados

### Relatórios

#### Obter Relatório Estatístico

```http
GET /report
```

Retorna estatísticas agregadas sobre todas as tarefas. Este endpoint é processado por uma função AWS Lambda.

**Resposta:**

```json
{
  "statusCode": 200,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  },
  "body": {
    "success": true,
    "report": {
      "total_tasks": 9,
      "by_status": {
        "completed": 2,
        "in_progress": 2,
        "pending": 5
      },
      "by_priority": {
        "high": 5,
        "medium": 3,
        "low": 1
      },
      "completion_rate": 22.22,
      "completion_percentage": "22.22%"
    },
    "timestamp": "dcd84014-3422-4393-8a9c-03582eefd3f7"
  }
}
```

**Códigos de Status:**

- `200 OK` - Sucesso
- `500 Internal Server Error` - Erro na Lambda ou API

**Nota**: Este endpoint não acessa o banco de dados diretamente. Ele faz uma requisição HTTP para o endpoint `/tasks` e calcula as estatísticas dos dados retornados.

## Modelos de Dados

### Objeto Task

```typescript
{
  id: number;                    // Gerado automaticamente
  title: string;                 // Máximo 200 caracteres
  description: string | null;    // Campo de texto opcional
  status: "pending" | "in_progress" | "completed";
  priority: "low" | "medium" | "high";
  created_at: string;           // Timestamp ISO 8601
  updated_at: string;           // Timestamp ISO 8601
}
```

### Objeto Report

```typescript
{
  total_tasks: number;
  by_status: {
    [key: string]: number;      // Contagem por status
  };
  by_priority: {
    [key: string]: number;      // Contagem por prioridade
  };
  completion_rate: number;      // Porcentagem (0-100)
  completion_percentage: string; // String formatada
}
```

## Respostas de Erro

Todas as respostas de erro seguem este formato:

```json
{
  "success": false,
  "error": "Descrição da mensagem de erro"
}
```

### Códigos de Erro Comuns

| Código de Status | Descrição |
|------------------|-----------|
| `400 Bad Request` | Entrada inválida ou requisição malformada |
| `404 Not Found` | Recurso não encontrado |
| `500 Internal Server Error` | Erro no servidor ou banco de dados |

## Cabeçalhos CORS

Todos os endpoints incluem cabeçalhos CORS:

```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

---

## Limitação de Taxa

A implantação atual não implementa limitação de taxa.

Para implantação em produção, considere implementar:
- Throttling do API Gateway (1000 requisições/segundo)
- Limitação de taxa por cliente
- Proteção contra burst

## Exemplos

### Exemplos cURL

```bash
# Listar todas as tarefas
curl https://SUA-URL-API-GATEWAY.amazonaws.com/prod/tasks

# Obter tarefa específica
curl https://SUA-URL-API-GATEWAY.amazonaws.com/prod/tasks/1

# Criar tarefa
curl -X POST https://SUA-URL-API-GATEWAY.amazonaws.com/prod/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Nova Tarefa","priority":"high"}'

# Atualizar tarefa
curl -X PUT https://SUA-URL-API-GATEWAY.amazonaws.com/prod/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status":"completed"}'

# Deletar tarefa
curl -X DELETE https://SUA-URL-API-GATEWAY.amazonaws.com/prod/tasks/1

# Obter relatório
curl https://SUA-URL-API-GATEWAY.amazonaws.com/prod/report
```

### Exemplos Python

```python
import requests

BASE_URL = "https://SUA-URL-API-GATEWAY.amazonaws.com/prod"

# Listar tarefas
response = requests.get(f"{BASE_URL}/tasks")
tasks = response.json()

# Criar tarefa
new_task = {
    "title": "Nova Tarefa",
    "description": "Descrição da tarefa",
    "priority": "high"
}
response = requests.post(f"{BASE_URL}/tasks", json=new_task)

# Atualizar tarefa
update = {"status": "completed"}
response = requests.put(f"{BASE_URL}/tasks/1", json=update)

# Deletar tarefa
response = requests.delete(f"{BASE_URL}/tasks/1")

# Obter relatório
response = requests.get(f"{BASE_URL}/report")
report = response.json()
```

### Exemplos JavaScript

```javascript
const BASE_URL = 'https://SUA-URL-API-GATEWAY.amazonaws.com/prod';

// Listar tarefas
fetch(`${BASE_URL}/tasks`)
  .then(response => response.json())
  .then(data => console.log(data));

// Criar tarefa
fetch(`${BASE_URL}/tasks`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    title: 'Nova Tarefa',
    priority: 'high'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));

// Atualizar tarefa
fetch(`${BASE_URL}/tasks/1`, {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    status: 'completed'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));

// Deletar tarefa
fetch(`${BASE_URL}/tasks/1`, {
  method: 'DELETE'
})
  .then(response => response.json())
  .then(data => console.log(data));

// Obter relatório
fetch(`${BASE_URL}/report`)
  .then(response => response.json())
  .then(data => console.log(data));
```

## Registro de Alterações

### Versão 1.0 (Atual)

- Lançamento inicial
- Operações CRUD completas para tarefas
- Endpoint de relatórios baseado em Lambda
- Integração com API Gateway
- Suporte CORS

## Suporte

Para problemas ou perguntas sobre a API:
- GitHub Issues: https://github.com/matheussricardoo/TasksCrudAWS/issues

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=00C853&height=120&section=footer"/>

</div>