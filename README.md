<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=FF6600&height=200&section=header&text=TasksCrudAWS&fontSize=50&fontColor=fff&animation=twinkling&fontAlignY=40&desc=Flask%20|%20API%20Gateway%20|%20Lambda%20|%20RDS%20MySQL%20|%20Docker&descAlignY=60&descSize=18">

<p align="center">
  <i>Complete task management system (To-Do List) built with microservices architecture on AWS, implementing Cloud Computing best practices.</i>
</p>

</div>

### Cloud Developing 2025/2

<div align="left">

**Team:**
1. Matheus Ricardo - Development, AWS Infrastructure, and Documentation
2. Priscila Herculano - Development, Testing, and AWS Infrastructure

</div>

### Technologies

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
[![AWS](https://img.shields.io/badge/AWS-Deployed-orange.svg)](https://aws.amazon.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## Overview

<div align="left">

Task management system (To-Do List) built with complete AWS cloud architecture, implementing cloud computing best practices.

**Domain:** Task Management

**Why it was chosen:** The task management domain was selected for being widely understandable, relevant to various professional contexts, and ideal for demonstrating complete CRUD operations. Additionally, it allows implementing additional features such as statistical reports and different priority levels, showcasing integrations between multiple AWS services.

**What the CRUD does:** Allows creating, listing, updating, and deleting tasks with attributes such as title, description, status (pending, in progress, completed), priority (low, medium, high), and automatic timestamps. It also includes a reports endpoint that generates aggregated statistics about registered tasks.

</div>

### Key Features

<div align="center">

| Feature | Description |
|:---:|:---|
| **Containerized Backend** | EC2 + Docker |
| **Managed Database** | RDS MySQL (Private Subnet) |
| **API Gateway** | Unified entry point |
| **Serverless Function** | Lambda for reports |
| **Production-Ready** | Secure, scalable, replicable |

</div>

### Deployed Infrastructure

<div align="center">

| Component | URL / Endpoint | Type |
|:---:|:---|:---:|
| **API Gateway** | `https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/prod` | REST API |
| **Backend EC2** | `http://YOUR-PUBLIC-IP:8080` | Flask + Docker |
| **RDS MySQL** | `tasks-db.xxxxxxxxxx.us-east-1.rds.amazonaws.com` | Private DB |
| **Lambda Function** | `tasks-report` | Python 3.9 |

</div>

## Architecture

<div align="left">

**4-layer cloud architecture on AWS:**
1. **Gateway Layer** - API Gateway (unified entry point)
2. **Compute Layer** - EC2 + Docker & Lambda (microservices)
3. **Data Layer** - RDS MySQL (private subnet)
4. **Security Layer** - Security Groups + IAM Roles

</div>

<div align="center">

### Architecture Diagram

</div>

```
┌──────────────────────────────────────────────────────────────────────┐
│                            AWS CLOUD                                │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                     API GATEWAY (REST API)                    │  │
│  │     https://xxxxxxxxxx.execute-api.us-east-1...amazonaws.com  │  │
│  │   ┌─────────────────────┐      ┌──────────────────────┐       │  │
│  │   │ CRUD Resources      │      │ Report Resource      │       │  │
│  │   │ /tasks              │      │ /report              │       │  │
│  │   │ /tasks/{id}         │      │                      │       │  │
│  │   └──────────┬──────────┘      └──────────┬───────────┘       │  │
│  └──────────────┼────────────────────────────┼──────────────────┘  │
│                 │                             │                    │
│                 │ HTTP Proxy                  │ Lambda Integration │
│                 │                             │                    │
│       ┌─────────▼──────────┐        ┌────────▼─────────┐           │
│       │   EC2 Instance     │◄───────┤  Lambda Function │           │
│       │  (t2.micro)        │  HTTP  │  tasks-report    │           │
│       │   Docker           │  GET   │  (Python 3.9)    │           │
│       │   Flask API        │        │  Serverless      │           │
│       │   Python 3.9       │        │  Statistics      │           │
│       │   Port 8080        │        │  Timeout 30s     │           │
│       └──────┬───────┘     │        └──────────────────┘           │
│              │             │                                        │
│              │             │                                        │
│              │ MySQL Protocol                                       │
│              │                                                     │
│       ┌─────────▼──────────────────────┐                            │
│       │   RDS MySQL (db.t3.micro)      │  PRIVATE SUBNET            │
│       │   tasks-db.*.rds.amazonaws.com │                            │
│       │   Database: tasks_db           │                            │
│       │   9 tasks stored               │  Access only from EC2      │
│       └────────────────────────────────┘                            │
└──────────────────────────────────────────────────────────────────────┘
```

### Components

<div align="center">

| Layer | Service | Description |
|:---:|:---:|:---|
| **Backend** | EC2 + Docker | REST API Flask (Python 3.9) |
| **Database** | Amazon RDS | MySQL (db.t3.micro) private subnet |
| **Gateway** | API Gateway | CRUD routes → EC2 · `/report` → Lambda |
| **Serverless** | AWS Lambda | Consumes API, generates JSON statistics |
| **CI/CD** | Deploy Scripts | Automated deployment via SSH |

**Status:** All components active and working

</div>

### Security Implementation

<div align="center">

| Security Feature | Description |
|:---:|:---|
| **Private RDS** | Not accessible from Internet |
| **Security Groups** | Only EC2 can access RDS |
| **API Gateway Proxy** | Backend not directly exposed |
| **CORS Enabled** | Controlled by headers |
| **Environment Variables** | No hardcoded credentials |

</div>

## How to Run Locally

### Prerequisites

<div align="center">

| Tool | Version | Purpose |
|:---:|:---:|:---:|
| **Docker** | Latest | Container runtime |
| **Git** | Latest | Version control |
| **AWS Account** | Free Tier | Cloud deployment |

</div>

### Step by Step

<div align="left">

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

### Test API Locally

<div align="left">

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

## 4. API Endpoints

### Base URLs

<div align="center">

| Environment | URL | Status |
|:---:|:---|:---:|
| **Production** | `https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/prod` | Active |
| **Local Development** | `http://localhost:8080` | Local |

</div>

### Available Resources

<div align="center">

| Method | Endpoint | Description | Integration |
|:---:|:---|:---|:---:|
| `GET` | `/tasks` | List all tasks | HTTP → EC2 |
| `GET` | `/tasks/{id}` | Get specific task | HTTP → EC2 |
| `POST` | `/tasks` | Create new task | HTTP → EC2 |
| `PUT` | `/tasks/{id}` | Update existing task | HTTP → EC2 |
| `DELETE` | `/tasks/{id}` | Delete task | HTTP → EC2 |
| `GET` | `/report` | Statistical report | Lambda |

</div>

### Usage Examples

#### List All Tasks

```bash
curl https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/prod/tasks
```

**Response:**
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

#### Create New Task

```bash
curl -X POST https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/prod/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Implement CI/CD Pipeline",
    "description": "Configure CodePipeline and CodeBuild",
    "status": "pending",
    "priority": "medium"
  }'
```

#### Statistical Report (Lambda)

```bash
curl https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/prod/report
```

**Response:**
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

> **Note:** The `/report` endpoint is processed by a Lambda function that makes an HTTP GET request to the EC2 API and calculates aggregated statistics. Does not access RDS directly.

## Test Results

<div align="center">

### Test Status

**All endpoints have been tested and are working correctly!**

</div>

<div align="center">

| Test | Endpoint | Method | Status | Result |
|:---:|:---:|:---:|:---:|:---|
| **Passed** | `/tasks` | GET | 200 OK | 9 tasks listed |
| **Passed** | `/tasks/1` | GET | 200 OK | Task #1 returned |
| **Passed** | `/tasks` | POST | 200 OK | Task #10 created |
| **Passed** | `/tasks/10` | PUT | 200 OK | Task #10 updated |
| **Passed** | `/tasks/10` | DELETE | 200 OK | Task #10 deleted |
| **Passed** | `/report` | GET | 200 OK | Lambda returned stats |

</div>

### System Statistics (via Lambda)

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

## Replication Guide

### Prerequisites

<div align="center">

| Requirement | Description |
|:---:|:---|
| **AWS Account** | Active (Free Tier or standard) |
| **Git** | Version control |
| **SSH Client** | For EC2 connection |
| **REST Client** | Postman/Insomnia/curl |

</div>

### Complete Implementation Guide

This repository contains a complete step-by-step guide to replicate the entire infrastructure:

<p align="center">
  <a href="docs/GUIA_IMPLANTACAO.md">
    <img src="https://img.shields.io/badge/📘_COMPLETE_GUIDE-FF6600?style=for-the-badge&logo=readthedocs&logoColor=white" alt="Complete Guide"/>
  </a>
</p>

<div align="center">

### Guide Includes

| Phase | Content |
|:---:|:---|
| **1** | RDS MySQL Configuration |
| **2** | EC2 with Docker Setup |
| **3** | Lambda Function Creation |
| **4** | API Gateway Configuration |
| **5** | Integration Tests |

</div>

### Local Development

To test locally before deploying to AWS:

```bash
# Clone repository
git clone https://github.com/matheussricardoo/TasksCrudAWS.git
cd TasksCrudAWS

# Configure environment variables
cp .env.example .env
# Edit .env with your credentials

# Start environment with Docker Compose
docker-compose up -d

# Wait for initialization
docker-compose logs -f

# Test API
curl http://localhost:8080/tasks
```

<p align="center">
  <b>API running at:</b> <code>http://localhost:8080</code>
</p>

## Project Structure

```
TasksCrudAWS/
│
├── src/                        # Application source code
│   ├── app.py                  # Complete Flask API (CRUD + validation)
│   ├── lambda_report.py        # Lambda function for reports
│   └── requirements.txt        # Python dependencies
│
├── deployment/                 # Deployment files
│   ├── Dockerfile              # Flask API container
│   ├── docker-compose.yml      # Local environment (MySQL + API)
│   └── sql/
│       └── schema.sql          # MySQL database schema
│
├── tests/                      # Test and deploy scripts
│   └── scripts/
│       ├── deploy.sh           # Deploy script (Linux/Mac)
│       ├── deploy.ps1          # Deploy script (Windows)
│       ├── test-api.sh         # Automated tests (Linux/Mac)
│       ├── test-api.ps1        # Automated tests (Windows)
│       └── test-api-simple.ps1 # Simple tests (Windows)
│
├── docs/                       # Documentation
│   └── REFERENCIA_API.md       # Complete API documentation
│
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignored files
├── tasks-key.pem               # EC2 SSH key (not committed)
├── docs/GUIA_IMPLANTACAO.md    # Complete deployment guide
├── README.md                   # This file
└── LICENSE                     # MIT License
```

<div align="center">

### Essential Files for Replication

| File | Purpose |
|:---:|:---|
| `src/app.py` | API code |
| `src/lambda_report.py` | Lambda code |
| `deployment/Dockerfile` + `deployment/docker-compose.yml` | Containerization |
| `deployment/sql/schema.sql` | Database schema |
| `docs/GUIA_IMPLANTACAO.md` | Implementation guide |

</div>

## Additional Documentation

<div align="center">

| Document | Description |
|:---:|:---|
| [docs/GUIA_IMPLANTACAO.md](docs/GUIA_IMPLANTACAO.md) | Complete replication guide |
| [REFERENCIA_API.md](docs/REFERENCIA_API.md) | REST API documentation |

</div>

## Security & Best Practices

### Implemented

<div align="center">

| Security Feature | Description |
|:---:|:---|
| **RDS Private Subnet** | Database not exposed to Internet |
| **Restrictive Security Groups** | Only necessary ports |
| **Environment Variables** | No hardcoded credentials |
| **API Gateway Proxy** | Backend protected |
| **CORS Configured** | Security headers |
| **Input Validation** | Data sanitization |
| **Error Handling** | Appropriate error messages |
| **Structured Logs** | CloudWatch + Docker logs |

</div>

### Production Recommendations

<div align="center">

| Priority | Feature |
|:---:|:---|
| **High** | AWS Secrets Manager |
| **High** | JWT/OAuth Authentication |
| **Medium** | Rate Limiting |
| **Medium** | CloudWatch Alarms |
| **Low** | Auto Scaling |
| **Low** | Automated Backups |
| **Low** | CloudFront CDN |

</div>

## Cost Estimate

### AWS Free Tier (12 months)

<div align="center">

| Service | Free Tier Limit | Monthly Cost |
|:---:|:---|:---:|
| **EC2 t2.micro** | 750 hours/month | **FREE** |
| **RDS db.t3.micro** | 750 hours/month | **FREE** |
| **Lambda** | 1M requests/month | **FREE** |
| **API Gateway** | 1M calls/month | **FREE** |
| **Total** | - | **$0/month** |

</div>

### After Free Tier (us-east-1 region)

<div align="center">

| Service | Monthly Cost |
|:---:|:---:|
| **EC2 t2.micro** | ~$8/month |
| **RDS db.t3.micro** | ~$15/month |
| **Lambda** (100K req/month) | ~$0.20/month |
| **API Gateway** (100K req/month) | ~$0.35/month |
| **Data Transfer** | ~$1/month |
| **Estimated Total** | **~$25/month** |

</div>

> **Tip:** To reduce costs, use **RDS Aurora Serverless** or **DynamoDB** instead of traditional RDS.

## FAQ

<div align="center">

### How to debug on AWS?

</div>

<div align="left">

**CloudWatch Logs:**
```bash
# Lambda logs
aws logs tail /aws/lambda/tasks-report --follow

# EC2 logs (via SSH)
ssh -i tasks-key.pem ec2-user@YOUR-EC2-IP
docker logs -f tasks-api
```

</div>

## License

<div align="center">

<a href="LICENSE">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge" alt="License: MIT">
</a>

<p>
  <b>This project is licensed under the MIT License. See the <a href="LICENSE">LICENSE</a> file for details.</b>
</p>

</div>

## Authors

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

## Support

<div align="center">

**Found a problem or have questions?**

**Issues**: [GitHub Issues](https://github.com/matheussricardoo/TasksCrudAWS/issues)

</div>

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=FF6600&height=120&section=footer"/>

</div>
