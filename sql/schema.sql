-- ============================================================
-- Schema do Banco de Dados - Tasks CRUD API
-- Projeto: AWS Learner Lab - Sistema de Tarefas
-- Banco: MySQL (Amazon RDS)
-- ============================================================

-- Criar banco de dados (se não existir)
CREATE DATABASE IF NOT EXISTS tasks_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE tasks_db;

-- ============================================================
-- Tabela: tasks
-- Descrição: Armazena todas as tarefas do sistema
-- ============================================================

CREATE TABLE IF NOT EXISTS tasks (
    -- ID único da tarefa (auto incremento)
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Título da tarefa (obrigatório)
    title VARCHAR(200) NOT NULL,
    
    -- Descrição detalhada (opcional)
    description TEXT,
    
    -- Status da tarefa
    -- Valores: pending, in_progress, completed
    status ENUM('pending', 'in_progress', 'completed') 
        DEFAULT 'pending' 
        NOT NULL,
    
    -- Prioridade da tarefa
    -- Valores: low, medium, high
    priority ENUM('low', 'medium', 'high') 
        DEFAULT 'medium' 
        NOT NULL,
    
    -- Data de criação (automática)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Data da última atualização (automática)
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Índices para melhorar performance das consultas
    INDEX idx_status (status),
    INDEX idx_priority (priority),
    INDEX idx_created_at (created_at)
    
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Tabela de tarefas do sistema CRUD';

-- ============================================================
-- Dados de Exemplo (opcional - para testes)
-- ============================================================

-- Inserir tarefas de exemplo
INSERT INTO tasks (title, description, status, priority) VALUES
('Configurar AWS Infrastructure', 'Criar RDS, EC2, Security Groups e configurações de rede', 'completed', 'high'),
('Desenvolver API REST', 'Implementar endpoints CRUD em Flask com validações', 'completed', 'high'),
('Criar função Lambda', 'Desenvolver Lambda para geração de relatórios estatísticos', 'in_progress', 'high'),
('Configurar API Gateway', 'Integrar rotas da API Gateway com EC2 e Lambda', 'pending', 'high'),
('Escrever documentação', 'Criar README, PDF técnico e diagramas de arquitetura', 'in_progress', 'medium'),
('Gravar vídeo de apresentação', 'Produzir vídeo demonstrativo de até 5 minutos', 'pending', 'medium'),
('Implementar CI/CD Pipeline', 'Configurar CodePipeline, CodeBuild e deploy automático', 'pending', 'low'),
('Testar todos os endpoints', 'Validar CRUD completo e tratamento de erros', 'pending', 'high'),
('Preparar apresentação final', 'Slides e roteiro para apresentação de 10 minutos', 'pending', 'medium');

-- ============================================================
-- Queries Úteis para Verificação
-- ============================================================

-- Contar tarefas por status
-- SELECT status, COUNT(*) as total FROM tasks GROUP BY status;

-- Contar tarefas por prioridade
-- SELECT priority, COUNT(*) as total FROM tasks GROUP BY priority;

-- Listar tarefas pendentes de alta prioridade
-- SELECT * FROM tasks WHERE status = 'pending' AND priority = 'high';

-- Taxa de conclusão
-- SELECT 
--     COUNT(*) as total,
--     SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
--     ROUND(SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) as completion_rate
-- FROM tasks;

-- ============================================================
-- Informações de Conexão (RDS)
-- ============================================================

-- Após criar o RDS, use:
-- Host: seu-endpoint-rds.region.rds.amazonaws.com
-- Port: 3306
-- User: admin
-- Password: [sua senha segura]
-- Database: tasks_db

-- Comando para conectar via EC2:
-- mysql -h seu-endpoint-rds.region.rds.amazonaws.com -u admin -p tasks_db

-- Comando para executar este script:
-- mysql -h seu-endpoint-rds.region.rds.amazonaws.com -u admin -p < schema.sql
