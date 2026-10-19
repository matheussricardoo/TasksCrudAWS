-- Tasks schema and academic sample data. Authors: Matheus Ricardo and Priscila Herculano.

CREATE DATABASE IF NOT EXISTS tasks_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE tasks_db;


CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    title VARCHAR(200) NOT NULL,
    
    description TEXT,
    
    status ENUM('pending', 'in_progress', 'completed') 
        DEFAULT 'pending' 
        NOT NULL,
    
    priority ENUM('low', 'medium', 'high') 
        DEFAULT 'medium' 
        NOT NULL,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_status (status),
    INDEX idx_priority (priority),
    INDEX idx_created_at (created_at)
    
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Task management table';


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
