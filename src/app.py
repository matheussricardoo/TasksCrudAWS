"""
Tasks CRUD API - Projeto AWS Learner Lab
API RESTful simples com Flask para gerenciamento de tarefas

Endpoints:
- GET    /health           - Health check
- GET    /tasks            - Listar todas as tarefas (com filtros opcionais)
- GET    /tasks/<id>       - Buscar tarefa por ID
- POST   /tasks            - Criar nova tarefa
- PUT    /tasks/<id>       - Atualizar tarefa
- DELETE /tasks/<id>       - Deletar tarefa

Autor: Matheus Ricardo & Priscila Herculano
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Permite requisições de qualquer origem

# ============= CONFIGURAÇÃO DO BANCO DE DADOS =============

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'admin'),
    'password': os.getenv('DB_PASSWORD', 'senha123'),
    'database': os.getenv('DB_NAME', 'tasks_db'),
    'cursorclass': pymysql.cursors.DictCursor,
    'autocommit': False
}

def get_db_connection():
    """
    Cria e retorna uma conexão com o banco MySQL.
    Usa variáveis de ambiente para configuração.
    """
    try:
        return pymysql.connect(**DB_CONFIG)
    except pymysql.Error as e:
        print(f"Erro ao conectar ao banco: {e}")
        raise

# ============= ENDPOINTS =============

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check - Verifica se a API e o banco de dados estão funcionando.
    
    Retorna:
        200: API e banco conectados
        500: Erro na conexão
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e)
        }), 500


@app.route('/tasks', methods=['GET'])
def get_tasks():
    """
    Lista todas as tarefas com filtros opcionais.
    
    Query Params:
        - status: pending, in_progress, completed
        - priority: low, medium, high
    
    Exemplo: GET /tasks?status=pending&priority=high
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Construir query com filtros opcionais
        query = "SELECT * FROM tasks WHERE 1=1"
        params = []
        
        # Filtro por status
        status = request.args.get('status')
        if status:
            query += " AND status = %s"
            params.append(status)
        
        # Filtro por prioridade
        priority = request.args.get('priority')
        if priority:
            query += " AND priority = %s"
            params.append(priority)
        
        # Ordenar por data de criação (mais recentes primeiro)
        query += " ORDER BY created_at DESC"
        
        cursor.execute(query, params)
        tasks = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'count': len(tasks),
            'data': tasks
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """
    Busca uma tarefa específica por ID.
    
    Args:
        task_id: ID da tarefa
    
    Retorna:
        200: Tarefa encontrada
        404: Tarefa não encontrada
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        task = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if task:
            return jsonify({
                'success': True,
                'data': task
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Task not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/tasks', methods=['POST'])
def create_task():
    """
    Cria uma nova tarefa.
    
    Body JSON:
        {
            "title": "string (obrigatório)",
            "description": "string (opcional)",
            "status": "pending|in_progress|completed (opcional, padrão: pending)",
            "priority": "low|medium|high (opcional, padrão: medium)"
        }
    
    Retorna:
        201: Tarefa criada com sucesso
        400: Dados inválidos
    """
    try:
        data = request.get_json()
        
        # Validação: título é obrigatório
        if not data or not data.get('title'):
            return jsonify({
                'success': False,
                'error': 'Title is required'
            }), 400
        
        # Validar valores de status e priority
        valid_statuses = ['pending', 'in_progress', 'completed']
        valid_priorities = ['low', 'medium', 'high']
        
        status = data.get('status', 'pending')
        priority = data.get('priority', 'medium')
        
        if status not in valid_statuses:
            return jsonify({
                'success': False,
                'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
            }), 400
        
        if priority not in valid_priorities:
            return jsonify({
                'success': False,
                'error': f'Invalid priority. Must be one of: {", ".join(valid_priorities)}'
            }), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO tasks (title, description, status, priority)
            VALUES (%s, %s, %s, %s)
        """
        
        cursor.execute(query, (
            data.get('title'),
            data.get('description', ''),
            status,
            priority
        ))
        
        conn.commit()
        task_id = cursor.lastrowid
        
        # Buscar a tarefa recém-criada
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        new_task = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Task created successfully',
            'data': new_task
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Atualiza uma tarefa existente.
    
    Args:
        task_id: ID da tarefa
    
    Body JSON (todos os campos são opcionais):
        {
            "title": "string",
            "description": "string",
            "status": "pending|in_progress|completed",
            "priority": "low|medium|high"
        }
    
    Retorna:
        200: Tarefa atualizada
        404: Tarefa não encontrada
        400: Nenhum campo para atualizar
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar se a tarefa existe
        cursor.execute("SELECT id FROM tasks WHERE id = %s", (task_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({
                'success': False,
                'error': 'Task not found'
            }), 404
        
        # Construir query de atualização dinamicamente
        update_fields = []
        params = []
        
        if 'title' in data:
            update_fields.append("title = %s")
            params.append(data['title'])
        
        if 'description' in data:
            update_fields.append("description = %s")
            params.append(data['description'])
        
        if 'status' in data:
            valid_statuses = ['pending', 'in_progress', 'completed']
            if data['status'] not in valid_statuses:
                cursor.close()
                conn.close()
                return jsonify({
                    'success': False,
                    'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
                }), 400
            update_fields.append("status = %s")
            params.append(data['status'])
        
        if 'priority' in data:
            valid_priorities = ['low', 'medium', 'high']
            if data['priority'] not in valid_priorities:
                cursor.close()
                conn.close()
                return jsonify({
                    'success': False,
                    'error': f'Invalid priority. Must be one of: {", ".join(valid_priorities)}'
                }), 400
            update_fields.append("priority = %s")
            params.append(data['priority'])
        
        if not update_fields:
            cursor.close()
            conn.close()
            return jsonify({
                'success': False,
                'error': 'No fields to update'
            }), 400
        
        # Adicionar updated_at
        update_fields.append("updated_at = NOW()")
        params.append(task_id)
        
        query = f"UPDATE tasks SET {', '.join(update_fields)} WHERE id = %s"
        cursor.execute(query, params)
        conn.commit()
        
        # Buscar tarefa atualizada
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        updated_task = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Task updated successfully',
            'data': updated_task
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Remove uma tarefa do banco de dados.
    
    Args:
        task_id: ID da tarefa
    
    Retorna:
        200: Tarefa deletada
        404: Tarefa não encontrada
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar se a tarefa existe
        cursor.execute("SELECT id FROM tasks WHERE id = %s", (task_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({
                'success': False,
                'error': 'Task not found'
            }), 404
        
        # Deletar tarefa
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Task deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============= EXECUÇÃO =============

if __name__ == '__main__':
    # Modo desenvolvimento (apenas para testes locais)
    # Em produção, usar Gunicorn: gunicorn --bind 0.0.0.0:8080 app:app
    print("Iniciando API Tasks...")
    print(f"Conectando ao banco: {DB_CONFIG['host']}/{DB_CONFIG['database']}")
    print("API disponível em: http://0.0.0.0:8080")
    
    app.run(host='0.0.0.0', port=8080, debug=False)
