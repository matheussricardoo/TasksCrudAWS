<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=FF6600&height=200&section=header&text=TasksCrudAWS&fontSize=50&fontColor=fff&animation=twinkling&fontAlignY=40&desc=Flask%20|%20API%20Gateway%20|%20Lambda%20|%20RDS%20MySQL%20|%20Docker&descAlignY=60&descSize=18">

<p align="center">
  <i>Sistema completo de gerenciamento de tarefas (To-Do List) construído com arquitetura de microsserviços na AWS, implementando as melhores práticas de Cloud Computing.</i>
</p>

<p align="center">
  <i>Complete task management system (To-Do List) built with microservices architecture on AWS, implementing Cloud Computing best practices.</i>
</p>

### Projeto Integrador – Cloud Developing 2025/2

<div align="left">

**Grupo:**
1. Matheus Ricardo - Desenvolvimento, Infraestrutura AWS e Documentação
2. Priscila Herculano - Desenvolvimento, Testes e Infraestrutura AWS

</div>

### Technologies | Tecnologias

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask"/>
  <img src="https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white" alt="AWS"/>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL"/>
  <img src="https://img.shields.io/badge/API_Gateway-FF4F8B?style=for-the-badge&logo=amazonapigateway&logoColor=white" alt="API Gateway"/>
  <img src="https://img.shields.io/badge/Lambda-FF9900?style=for-the-badge&logo=awslambda&logoColor=white" alt="Lambda"/>
  <img src="https://img.shields.io/badge/RDS-527FFF?style=for-the-badge&logo=amazonrds&logoColor=white" alt="RDS"/>
</div>

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![AWS](https://img.shields.io/badge/AWS-Implantado-orange.svg)](https://aws.amazon.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerizado-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## Visão Geral

<div align="left">

**PT-BR:** Sistema de gerenciamento de tarefas (To-Do List) construído com arquitetura completa na nuvem AWS, implementando as melhores práticas de computação em nuvem.

**Domínio:** Gerenciamento de Tarefas (Task Management)

**Por que foi escolhido:** O domínio de gerenciamento de tarefas foi selecionado por ser amplamente compreensível, relevante para diversos contextos profissionais e ideal para demonstrar operações CRUD completas. Além disso, permite implementar funcionalidades adicionais como relatórios estatísticos e diferentes níveis de prioridade, showcasing integrações entre múltiplos serviços AWS.

**O que o CRUD faz:** Permite criar, listar, atualizar e deletar tarefas com atributos como título, descrição, status (pendente, em progresso, concluída), prioridade (baixa, média, alta) e timestamps automáticos. Inclui também um endpoint de relatórios que gera estatísticas agregadas sobre as tarefas cadastradas.

**EN:** Task management system (To-Do List) built with complete AWS cloud architecture, implementing cloud computing best practices.

**Domain:** Task Management

**Why it was chosen:** The task management domain was selected for being widely understandable, relevant to various professional contexts, and ideal for demonstrating complete CRUD operations. Additionally, it allows implementing additional features such as statistical reports and different priority levels, showcasing integrations between multiple AWS services.

**What the CRUD does:** Allows creating, listing, updating, and deleting tasks with attributes such as title, description, status (pending, in progress, completed), priority (low, medium, high), and automatic timestamps. It also includes a reports endpoint that generates aggregated statistics about registered tasks.

</div>

### Principais Características | Key Features

<div align="center">

| Feature / Recurso | Description EN | Descrição PT-BR |
|:---:|:---|:---|
| **Backend Containerizado** | EC2 + Docker | EC2 + Docker |
| **Banco de Dados Gerenciado** | RDS MySQL (Private Subnet) | RDS MySQL (Subnet Privada) |
| **API Gateway** | Unified entry point | Ponto de entrada unificado |
| **Função Serverless** | Lambda for reports | Lambda para relatórios |
| **Production-Ready** | Secure, scalable, replicable | Segura, escalável e replicável |

</div>

### Infraestrutura Implantada | Deployed Infrastructure

<div align="center">

| Component / Componente | URL / Endpoint | Type / Tipo |
|:---:|:---|:---:|
| **API Gateway** | `https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/prod` | REST API |
| **Backend EC2** | `http://SEU-IP-PUBLICO:8080` | Flask + Docker |
| **RDS MySQL** | `tasks-db.xxxxxxxxxx.us-east-1.rds.amazonaws.com` | Private DB |
| **Lambda Function** | `tasks-report` | Python 3.9 |

</div>

## Arquitetura | Architecture

<div align="left">

**EN:** 4-layer cloud architecture on AWS:
1. **Gateway Layer** - API Gateway (unified entry point)
2. **Compute Layer** - EC2 + Docker & Lambda (microservices)
3. **Data Layer** - RDS MySQL (private subnet)
4. **Security Layer** - Security Groups + IAM Roles

**PT-BR:** Arquitetura em nuvem de 4 camadas na AWS:
1. **Camada de Gateway** - API Gateway (entrada unificada)
2. **Camada de Computação** - EC2 + Docker & Lambda (microsserviços)
3. **Camada de Dados** - RDS MySQL (subnet privada)
4. **Camada de Segurança** - Security Groups + IAM Roles

</div>

<div align="center">

### Architecture Diagram | Diagrama de Arquitetura

</div>

```
┌──────────────────────────────────────────────────────────────────────┐
│                            AWS CLOUD                                  │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                     API GATEWAY (REST API)                      │  │
│  │     https://xxxxxxxxxx.execute-api.us-east-1...amazonaws.com   │  │
│  │                                                                 │  │
│  │   ┌─────────────────────┐      ┌──────────────────────┐      │  │
│  │   │ Recursos CRUD       │      │ Recurso Relatório    │      │  │
│  │   │ /tasks              │      │ /report              │      │  │
│  │   │ /tasks/{id}         │      │                      │      │  │
│  │   └──────────┬──────────┘      └──────────┬───────────┘      │  │
│  └──────────────┼────────────────────────────┼──────────────────┘  │
│                 │                             │                      │
│                 │ Proxy HTTP                  │ Integração Lambda    │
│                 │                             │                      │
│       ┌─────────▼──────────┐        ┌────────▼─────────┐           │
│       │                    │        │                  │            │
│       │   Instância EC2    │◄───────┤  Função Lambda   │            │
│       │  (t2.micro)        │  HTTP  │  tasks-report    │            │
│       │                    │  GET   │  (Python 3.9)    │            │
│       │  ┌──────────────┐  │        │                  │            │
│       │  │   Docker     │  │        │  Serverless      │            │
│       │  │              │  │        │  Estatísticas    │            │
│       │  │  API Flask   │  │        │  Timeout 30s     │            │
│       │  │  Python 3.9  │  │        └──────────────────┘            │
│       │  │  Porta 8080  │  │                                         │
│       │  └──────┬───────┘  │                                         │
│       │         │          │                                         │
│       └─────────┼──────────┘                                         │
│                 │                                                     │
│                 │ Protocolo MySQL                                     │
│                 │                                                     │
│       ┌─────────▼──────────────────────┐                            │
│       │   RDS MySQL (db.t3.micro)      │  SUBNET PRIVADA            │
│       │   tasks-db.*.rds.amazonaws.com │                            │
│       │                                 │  Sem acesso público        │
│       │   Database: tasks_db            │                            │
│       │   9 tarefas armazenadas         │  Acesso apenas do EC2      │
│       └─────────────────────────────────┘                            │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

### Componentes | Components

<div align="center">

| Camada / Layer | Serviço / Service | Descrição EN | Descrição PT-BR |
|:---:|:---:|:---|:---|
| **Backend** | EC2 + Docker | REST API Flask (Python 3.9) | API REST Flask (Python 3.9) |
| **Database** | Amazon RDS | MySQL (db.t3.micro) private subnet | MySQL (db.t3.micro) subnet privada |
| **Gateway** | API Gateway | CRUD routes → EC2 · `/report` → Lambda | Rotas CRUD → EC2 · `/report` → Lambda |
| **Serverless** | AWS Lambda | Consumes API, generates JSON statistics | Consome a API, gera estatísticas JSON |
| **CI/CD** | Deploy Scripts | Automated deployment via SSH | Deploy automatizado via SSH |

**Status:** Todos os componentes ativos e funcionando / All components active and working

</div>

### Implementação de Segurança | Security Implementation

<div align="center">

| Security Feature / Recurso de Segurança | Description EN | Descrição PT-BR |
|:---:|:---|:---|
| **Private RDS** | Not accessible from Internet | Não acessível pela Internet |
| **Security Groups** | Only EC2 can access RDS | Apenas EC2 pode acessar RDS |
| **API Gateway Proxy** | Backend not directly exposed | Backend não exposto diretamente |
| **CORS Enabled** | Controlled by headers | Controlado por headers |
| **Environment Variables** | No hardcoded credentials | Sem credenciais hardcoded |

</div>

## Como Rodar Localmente | How to Run Locally

### Pré-requisitos | Prerequisites

<div align="center">

| Tool / Ferramenta | Version / Versão | Purpose / Propósito |
|:---:|:---:|:---:|
| **Docker** | Latest | Container runtime |
| **Git** | Latest | Version control |
| **AWS Account** | Free Tier | Cloud deployment |

</div>

### Passo a Passo | Step by Step

<div align="left">

**PT-BR:**

```bash
# 1. Clonar repositório
git clone https://github.com/matheussricardoo/TasksCrudAWS.git
cd TasksCrudAWS

# 2. Configurar variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas credenciais do RDS

# 3. Iniciar ambiente com Docker Compose
docker-compose up --build

# 4. API estará disponível em:
# http://localhost:8080
```

**EN:**
```bash
# 1. Clone repository
git clone https://github.com/matheussricardoo/TasksCrudAWS.git
cd TasksCrudAWS

# 2. Configure environment variables
cp .env.example .env
# Edit .env file with your RDS credentials

# 3. Start environment with Docker Compose
docker-compose up --build

# 4. API will be available at:
# http://localhost:8080
```

</div>

### Testar API Localmente | Test API Locally

<div align="left">

**PT-BR:**

```bash
# Health check
curl http://localhost:8080/health

# Listar tarefas
curl http://localhost:8080/tasks

# Criar tarefa
curl -X POST http://localhost:8080/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Teste Local","priority":"high"}'
```

**EN:**
```bash
# Health check
curl http://localhost:8080/health

# List tasks
curl http://localhost:8080/tasks

# Create task
curl -X POST http://localhost:8080/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Local Test","priority":"high"}'
```

</div>

## 4. 📡 Endpoints da API | API Endpoints

### 🌐 URLs Base | Base URLs

<div align="center">

| Environment / Ambiente | URL | Status |
|:---:|:---|:---:|
| **Production** | `https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/prod` | Active |
| **Local Development** | `http://localhost:8080` | Local |

</div>

### Recursos Disponíveis | Available Resources

<div align="center">

| Método / Method | Endpoint | Descrição PT-BR | Description EN | Integração / Integration |
|:---:|:---|:---|:---|:---:|
| `GET` | `/tasks` | Listar todas as tarefas | List all tasks | HTTP → EC2 |
| `GET` | `/tasks/{id}` | Buscar tarefa específica | Get specific task | HTTP → EC2 |
| `POST` | `/tasks` | Criar nova tarefa | Create new task | HTTP → EC2 |
| `PUT` | `/tasks/{id}` | Atualizar tarefa existente | Update existing task | HTTP → EC2 |
| `DELETE` | `/tasks/{id}` | Deletar tarefa | Delete task | HTTP → EC2 |
| `GET` | `/report` | Relatório estatístico | Statistical report | Lambda |

</div>

### Exemplos de Uso | Usage Examples

#### Listar Todas as Tarefas

```bash
curl https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/prod/tasks
```

**Resposta:**
```json
{
  "success": true,
  "count": 9,
  "data": [
    {
      "id": 1,
      "title": "Configurar Infraestrutura AWS",
      "description": "Criar RDS, EC2, Security Groups...",
      "status": "completed",
      "priority": "high",
      "created_at": "2025-10-31T22:56:45Z",
      "updated_at": "2025-10-31T22:56:45Z"
    }
  ]
}
```

#### Criar Nova Tarefa

```bash
curl -X POST https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/prod/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Implementar Pipeline CI/CD",
    "description": "Configurar CodePipeline e CodeBuild",
    "status": "pending",
    "priority": "medium"
  }'
```

#### Relatório Estatístico (Lambda)

```bash
curl https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/prod/report
```

**Resposta:**
```json
{
  "statusCode": 200,
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
    }
  }
}
```

> **Nota PT-BR**: O endpoint `/report` é processado por uma função Lambda que faz uma requisição HTTP GET para a API do EC2 e calcula estatísticas agregadas. Não acessa o RDS diretamente.

> **Note EN**: The `/report` endpoint is processed by a Lambda function that makes an HTTP GET request to the EC2 API and calculates aggregated statistics. Does not access RDS directly.

## Resultados dos Testes | Test Results

<div align="center">

### Status dos Testes | Test Status

**Todos os endpoints foram testados e estão funcionando corretamente!**  
**All endpoints have been tested and are working correctly!**

</div>

<div align="center">

| Teste / Test | Endpoint | Método / Method | Status | Resultado EN | Resultado PT-BR |
|:---:|:---:|:---:|:---:|:---|:---|
| **Aprovado** | `/tasks` | GET | 200 OK | 9 tasks listed | 9 tarefas listadas |
| **Aprovado** | `/tasks/1` | GET | 200 OK | Task #1 returned | Tarefa #1 retornada |
| **Aprovado** | `/tasks` | POST | 200 OK | Task #10 created | Tarefa #10 criada |
| **Aprovado** | `/tasks/10` | PUT | 200 OK | Task #10 updated | Tarefa #10 atualizada |
| **Aprovado** | `/tasks/10` | DELETE | 200 OK | Task #10 deleted | Tarefa #10 deletada |
| **Aprovado** | `/report` | GET | 200 OK | Lambda returned stats | Lambda retornou estatísticas |

</div>

### Estatísticas do Sistema (via Lambda) | System Statistics (via Lambda)

```json
{
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
  "completion_rate": 22.22
}
```

## Guia de Replicação | Replication Guide

### Pré-requisitos | Prerequisites

<div align="center">

| Requirement / Requisito | Description EN | Descrição PT-BR |
|:---:|:---|:---|
| **AWS Account** | Active (Free Tier or standard) | Conta ativa (Free Tier ou padrão) |
| **Git** | Version control | Controle de versão |
| **SSH Client** | For EC2 connection | Para conexão com EC2 |
| **REST Client** | Postman/Insomnia/curl | Postman/Insomnia/curl |

</div>

### Guia Completo de Implementação | Complete Implementation Guide

<div align="left">

**PT-BR:**  
Este repositório contém um guia passo a passo completo para replicar toda a infraestrutura:

**EN:**  
This repository contains a complete step-by-step guide to replicate the entire infrastructure:

</div>

<p align="center">
  <a href="GUIA_IMPLANTACAO.md">
    <img src="https://img.shields.io/badge/📘_GUIA_COMPLETO-FF6600?style=for-the-badge&logo=readthedocs&logoColor=white" alt="Complete Guide"/>
  </a>
</p>

<div align="center">

### O Guia Inclui | Guide Includes

| Phase / Fase | Content EN | Conteúdo PT-BR |
|:---:|:---|:---|
| **1** | RDS MySQL Configuration | Configuração do RDS MySQL |
| **2** | EC2 with Docker Setup | Configuração do EC2 com Docker |
| **3** | Lambda Function Creation | Criação da Função Lambda |
| **4** | API Gateway Configuration | Configuração do API Gateway |
| **5** | Integration Tests | Testes de Integração |

</div>

### Desenvolvimento Local | Local Development

<div align="left">

**PT-BR:**  
Para testar localmente antes do deploy na AWS:

**EN:**  
To test locally before deploying to AWS:

</div>

```bash
# Clonar repositório
git clone https://github.com/matheussricardoo/TasksCrudAWS.git
cd TasksCrudAWS

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas credenciais

# Iniciar ambiente com Docker Compose
docker-compose up -d

# Aguardar inicialização
docker-compose logs -f

# Testar API
curl http://localhost:8080/tasks
```

<p align="center">
  <b>API rodando em / API running at:</b> <code>http://localhost:8080</code>
</p>

## Estrutura do Projeto | Project Structure

```
TasksCrudAWS/
│
├── app.py                      # API Flask completa (CRUD + validações)
├── lambda_report.py            # Função Lambda para relatórios
├── requirements.txt            # Dependências Python
├── Dockerfile                  # Container da API Flask
├── docker-compose.yml          # Ambiente local (MySQL + API)
├── .env.example                # Template de variáveis de ambiente
├── .gitignore                  # Arquivos ignorados pelo Git
├── tasks-key.pem               # Chave SSH do EC2 (não commitado)
│
├── sql/
│   └── schema.sql              # Schema do banco MySQL
│
├── scripts/
│   ├── deploy.sh               # Script de deploy (Linux/Mac)
│   ├── deploy.ps1              # Script de deploy (Windows)
│   ├── test-api.sh             # Testes automatizados (Linux/Mac)
│   ├── test-api.ps1            # Testes automatizados (Windows)
│   └── test-api-simple.ps1     # Testes simples (Windows)
│
├── docs/
│   └── REFERENCIA_API.md       # Documentação completa da API
│
├── GUIA_IMPLANTACAO.md         # Guia completo de implantação
├── README.md                   # Este arquivo
└── LICENSE                     # Licença MIT
```

<div align="center">

### Arquivos Essenciais para Replicação | Essential Files for Replication

| File / Arquivo | Purpose EN | Propósito PT-BR |
|:---:|:---|:---|
| `app.py` | API code | Código da API |
| `lambda_report.py` | Lambda code | Código da Lambda |
| `Dockerfile` + `docker-compose.yml` | Containerization | Containerização |
| `sql/schema.sql` | Database schema | Schema do banco |
| `docs/GUIA_IMPLANTACAO.md` | Implementation guide | Guia de implementação |

</div>

## Documentação Adicional | Additional Documentation

<div align="center">

| Documento / Document | Descrição PT-BR | Description EN |
|:---:|:---|:---|
| [GUIA_IMPLANTACAO.md](GUIA_IMPLANTACAO.md) | Guia completo de replicação | Complete replication guide |
| [REFERENCIA_API.md](docs/REFERENCIA_API.md) | Documentação da API REST | REST API documentation |

</div>

## Segurança e Boas Práticas | Security & Best Practices

### Implementado | Implemented

<div align="center">

| Security Feature / Recurso | Description EN | Descrição PT-BR |
|:---:|:---|:---|
| **RDS Private Subnet** | Database not exposed to Internet | Banco não exposto à Internet |
| **Restrictive Security Groups** | Only necessary ports | Apenas portas necessárias |
| **Environment Variables** | No hardcoded credentials | Sem credenciais hardcoded |
| **API Gateway Proxy** | Backend protected | Backend protegido |
| **CORS Configured** | Security headers | Headers de segurança |
| **Input Validation** | Data sanitization | Sanitização de dados |
| **Error Handling** | Appropriate error messages | Mensagens de erro apropriadas |
| **Structured Logs** | CloudWatch + Docker logs | CloudWatch + logs Docker |

</div>

### Recomendações para Produção | Production Recommendations

<div align="center">

| Priority / Prioridade | Feature EN | Funcionalidade PT-BR |
|:---:|:---|:---|
| **High** | AWS Secrets Manager | Gerenciamento de credenciais |
| **High** | JWT/OAuth Authentication | Autenticação de usuários |
| **Medium** | Rate Limiting | Proteção contra abuso |
| **Medium** | CloudWatch Alarms | Monitoramento proativo |
| **Low** | Auto Scaling | Escalabilidade automática |
| **Low** | Automated Backups | Recuperação de desastres |
| **Low** | CloudFront CDN | Cache e performance global |

</div>

## Estimativa de Custos | Cost Estimate

### AWS Free Tier (12 meses / 12 months)

<div align="center">

| Service / Serviço | Free Tier Limit | Monthly Cost / Custo Mensal |
|:---:|:---|:---:|
| **EC2 t2.micro** | 750 horas/mês · 750 hours/month | **GRÁTIS / FREE** |
| **RDS db.t3.micro** | 750 horas/mês · 750 hours/month | **GRÁTIS / FREE** |
| **Lambda** | 1M requisições/mês · 1M requests/month | **GRÁTIS / FREE** |
| **API Gateway** | 1M chamadas/mês · 1M calls/month | **GRÁTIS / FREE** |
| **Total** | - | **R$ 0/mês · $0/month** |

</div>

### Após Free Tier (região us-east-1 / us-east-1 region)

<div align="center">

| Service / Serviço | Monthly Cost / Custo Mensal |
|:---:|:---:|
| **EC2 t2.micro** | ~R$ 42/mês · ~$8/month |
| **RDS db.t3.micro** | ~R$ 75/mês · ~$15/month |
| **Lambda** (100K req/mês) | ~R$ 1/mês · ~$0.20/month |
| **API Gateway** (100K req/mês) | ~R$ 1,75/mês · ~$0.35/month |
| **Transferência de Dados / Data Transfer** | ~R$ 5/mês · ~$1/month |
| **Total Estimado** | **~R$ 125/mês · ~$25/month** |

</div>

> **Dica PT-BR:** Para reduzir custos, use **RDS Aurora Serverless** ou **DynamoDB** no lugar do RDS tradicional.

> **Tip EN:** To reduce costs, use **RDS Aurora Serverless** or **DynamoDB** instead of traditional RDS.

## Perguntas Frequentes | FAQ

<div align="center">

### Como fazer debug na AWS? | How to debug on AWS?

</div>

<div align="left">

**PT-BR: CloudWatch Logs:**
```bash
# Logs da Lambda
aws logs tail /aws/lambda/tasks-report --follow

# Logs do EC2 (via SSH)
ssh -i tasks-key.pem ec2-user@SEU-IP-EC2
docker logs -f tasks-api
```

**EN: CloudWatch Logs:**
```bash
# Lambda logs
aws logs tail /aws/lambda/tasks-report --follow

# EC2 logs (via SSH)
ssh -i tasks-key.pem ec2-user@YOUR-EC2-IP
docker logs -f tasks-api
```

</div>

## Licença | License

<div align="center">

<a href="LICENSE">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge" alt="License: MIT">
</a>

<p>
  <b>EN:</b> This project is licensed under the MIT License. See the <a href="LICENSE">LICENSE</a> file for details.<br>
  <b>PT-BR:</b> Este projeto está licenciado sob a Licença MIT. Veja o arquivo <a href="LICENSE">LICENSE</a> para mais detalhes.
</p>

</div>

## Autores

### Authors | Autores

<div align="center">
<table>
  <tr>
    <td align="center">
      <a href="https://github.com/matheussricardoo" target="_blank">
        <img src="https://avatars.githubusercontent.com/matheussricardoo" width="120px;" alt="Matheus Ricardo"/><br>
        <sub>
          <b>Matheus Ricardo</b>
        </sub>
      </a>
      <br>
      <a href="https://github.com/matheussricardoo" target="_blank">
        <img src="https://skillicons.dev/icons?i=github" width="32" alt="GitHub"/>
      </a>
      <a href="https://www.linkedin.com/in/matheus-ricardo-426452266/" target="_blank">
        <img src="https://skillicons.dev/icons?i=linkedin" width="32" alt="LinkedIn"/>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/PriHerculano" target="_blank">
        <img src="https://avatars.githubusercontent.com/PriHerculano" width="120px;" alt="Priscila Herculano"/><br>
        <sub>
          <b>Priscila Herculano</b>
        </sub>
      </a>
      <br>
      <a href="https://github.com/PriHerculano" target="_blank">
        <img src="https://skillicons.dev/icons?i=github" width="32" alt="GitHub"/>
      </a>
      <a href="https://www.linkedin.com/in/priscilaherculano/" target="_blank">
        <img src="https://skillicons.dev/icons?i=linkedin" width="32" alt="LinkedIn"/>
      </a>
    </td>
  </tr>
</table>
</div>

## Suporte

<div align="center">

**EN:** Found a problem or have questions?  
**PT-BR:** Encontrou algum problema ou tem dúvidas?

**Issues**: [GitHub Issues](https://github.com/matheussricardoo/TasksCrudAWS/issues)

</div>

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=FF6600&height=120&section=footer"/>

</div>
