"""Academic task API. Original authors: Matheus Ricardo and Priscila Herculano."""
from contextlib import contextmanager
from datetime import datetime
from functools import wraps
import os

from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'admin'),
    'password': os.getenv('DB_PASSWORD', 'senha123'),
    'database': os.getenv('DB_NAME', 'tasks_db'),
    'cursorclass': pymysql.cursors.DictCursor,
    'autocommit': False,
    'connect_timeout': 5,
}
STATUSES = ('pending', 'in_progress', 'completed')
PRIORITIES = ('low', 'medium', 'high')
FIELDS = ('title', 'description', 'status', 'priority')


def get_db_connection():
    return pymysql.connect(**DB_CONFIG)


@contextmanager
def database_cursor():
    """Close connections on every path and roll back failed transactions."""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            yield connection, cursor
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def database_errors(handler):
    @wraps(handler)
    def wrapped(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except Exception:
            app.logger.exception('Task request failed')
            return jsonify(success=False, error='Internal server error'), 500
    return wrapped


def validate_payload(data, creating=False):
    """Validate the supported fields before opening a database connection."""
    if not isinstance(data, dict) or not data:
        return 'A non-empty JSON object is required'
    if creating and 'title' not in data:
        return 'Title is required'
    if 'title' in data and (not isinstance(data['title'], str)
                            or not data['title'].strip() or len(data['title']) > 200):
        return 'Title must be a non-blank string of at most 200 characters'
    if 'description' in data and not isinstance(data['description'], str):
        return 'Description must be a string'
    if 'status' in data and data['status'] not in STATUSES:
        return 'Invalid status. Must be one of: ' + ', '.join(STATUSES)
    if 'priority' in data and data['priority'] not in PRIORITIES:
        return 'Invalid priority. Must be one of: ' + ', '.join(PRIORITIES)
    if not any(field in data for field in FIELDS):
        return 'No fields to update'
    return None


@app.get('/health')
def health_check():
    try:
        with database_cursor() as (_, cursor):
            cursor.execute('SELECT 1')
        return jsonify(status='healthy', database='connected', timestamp=datetime.now().isoformat())
    except Exception:
        app.logger.exception('Database health check failed')
        return jsonify(status='unhealthy', database='disconnected'), 500


@app.get('/tasks')
@database_errors
def get_tasks():
    query = 'SELECT * FROM tasks WHERE 1=1'
    parameters = []
    # Column names come from this fixed allowlist; values are parameterized.
    for field in ('status', 'priority'):
        value = request.args.get(field)
        if value:
            query += f' AND {field} = %s'
            parameters.append(value)
    query += ' ORDER BY created_at DESC'
    with database_cursor() as (_, cursor):
        cursor.execute(query, parameters)
        tasks = cursor.fetchall()
    return jsonify(success=True, count=len(tasks), data=tasks)


@app.get('/tasks/<int:task_id>')
@database_errors
def get_task(task_id):
    with database_cursor() as (_, cursor):
        cursor.execute('SELECT * FROM tasks WHERE id = %s', (task_id,))
        task = cursor.fetchone()
    if task is None:
        return jsonify(success=False, error='Task not found'), 404
    return jsonify(success=True, data=task)


@app.post('/tasks')
@database_errors
def create_task():
    data = request.get_json(silent=True)
    error = validate_payload(data, creating=True)
    if error:
        return jsonify(success=False, error=error), 400
    with database_cursor() as (connection, cursor):
        cursor.execute('INSERT INTO tasks (title, description, status, priority) VALUES (%s, %s, %s, %s)',
                       (data['title'], data.get('description', ''), data.get('status', 'pending'),
                        data.get('priority', 'medium')))
        task_id = cursor.lastrowid
        cursor.execute('SELECT * FROM tasks WHERE id = %s', (task_id,))
        task = cursor.fetchone()
        connection.commit()
    return jsonify(success=True, message='Task created successfully', data=task), 201


@app.put('/tasks/<int:task_id>')
@database_errors
def update_task(task_id):
    data = request.get_json(silent=True)
    error = validate_payload(data)
    if error:
        return jsonify(success=False, error=error), 400
    with database_cursor() as (connection, cursor):
        cursor.execute('SELECT id FROM tasks WHERE id = %s', (task_id,))
        if cursor.fetchone() is None:
            return jsonify(success=False, error='Task not found'), 404
        fields = [field for field in FIELDS if field in data]
        assignments = ', '.join(f'{field} = %s' for field in fields)
        cursor.execute(f'UPDATE tasks SET {assignments}, updated_at = NOW() WHERE id = %s',
                       [data[field] for field in fields] + [task_id])
        cursor.execute('SELECT * FROM tasks WHERE id = %s', (task_id,))
        task = cursor.fetchone()
        connection.commit()
    return jsonify(success=True, message='Task updated successfully', data=task)


@app.delete('/tasks/<int:task_id>')
@database_errors
def delete_task(task_id):
    with database_cursor() as (connection, cursor):
        cursor.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
        deleted = cursor.rowcount
        connection.commit()
    if not deleted:
        return jsonify(success=False, error='Task not found'), 404
    return jsonify(success=True, message='Task deleted successfully')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
