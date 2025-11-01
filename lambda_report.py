"""
Lambda Function - Tasks Report Generator
Gera relatório estatístico das tarefas consumindo a API no EC2

Função:
- Consome endpoint GET /tasks da API
- Calcula estatísticas (total, por status, por prioridade)
- Retorna JSON com relatório completo

Integração: API Gateway → Lambda → EC2 API

Autor: Matheus Ricardo & Priscila Herculano
"""

import json
import urllib3
import os

# URL da API no EC2 (configurar via variável de ambiente)
# Exemplo: http://ec2-XX-XXX-XXX-XXX.compute-1.amazonaws.com:8080/tasks
API_URL = os.getenv('API_URL', 'http://localhost:8080/tasks')

# Cliente HTTP (urllib3 é nativo no Lambda Python 3.9+)
http = urllib3.PoolManager()


def lambda_handler(event, context):
    """
    Handler principal da função Lambda.
    
    Esta função:
    1. Faz request HTTP GET para a API de tarefas
    2. Processa os dados recebidos
    3. Calcula estatísticas
    4. Retorna relatório em JSON
    
    Args:
        event: Evento do API Gateway
        context: Contexto de execução do Lambda
    
    Returns:
        dict: Response formatado para API Gateway
    """
    
    try:
        print(f"Gerando relatório de tarefas...")
        print(f"API URL: {API_URL}")
        
        # Fazer request HTTP para a API
        response = http.request('GET', API_URL, timeout=10.0)
        
        if response.status != 200:
            raise Exception(f"API retornou status {response.status}")
        
        # Parsear resposta JSON
        api_response = json.loads(response.data.decode('utf-8'))
        
        # Verificar se há tarefas
        if 'data' in api_response:
            tasks = api_response['data']
        else:
            tasks = api_response  # Fallback se API retornar array direto
        
        # Calcular estatísticas
        total = len(tasks)
        
        # Contadores por status
        completed = sum(1 for t in tasks if t.get('status') == 'completed')
        pending = sum(1 for t in tasks if t.get('status') == 'pending')
        in_progress = sum(1 for t in tasks if t.get('status') == 'in_progress')
        
        # Contadores por prioridade
        high_priority = sum(1 for t in tasks if t.get('priority') == 'high')
        medium_priority = sum(1 for t in tasks if t.get('priority') == 'medium')
        low_priority = sum(1 for t in tasks if t.get('priority') == 'low')
        
        # Taxa de conclusão
        completion_rate = round((completed / total * 100) if total > 0 else 0, 2)
        
        # Montar relatório
        report = {
            'success': True,
            'report': {
                'total_tasks': total,
                'by_status': {
                    'completed': completed,
                    'in_progress': in_progress,
                    'pending': pending
                },
                'by_priority': {
                    'high': high_priority,
                    'medium': medium_priority,
                    'low': low_priority
                },
                'completion_rate': completion_rate,
                'completion_percentage': f"{completion_rate}%"
            },
            'timestamp': context.aws_request_id if context else 'local-test'
        }
        
        print(f"Relatório gerado: {total} tarefas processadas")
        
        # Retornar resposta formatada para API Gateway
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',  # CORS
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET,OPTIONS'
            },
            'body': json.dumps(report, ensure_ascii=False)
        }
        
    except urllib3.exceptions.TimeoutError:
        print("Erro: Timeout ao conectar com a API")
        return {
            'statusCode': 504,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': False,
                'error': 'Timeout connecting to API',
                'message': 'Verifique se a API está rodando e acessível'
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
                'error': str(e),
                'message': 'Erro ao processar relatório de tarefas'
            })
        }


# Para testes locais (executar: python lambda_report.py)
if __name__ == '__main__':
    print("Testando Lambda localmente...\n")
    
    # Simular evento do API Gateway
    test_event = {
        'httpMethod': 'GET',
        'path': '/report'
    }
    
    # Simular contexto do Lambda
    class TestContext:
        request_id = 'test-local-123'
    
    # Executar handler
    result = lambda_handler(test_event, TestContext())
    
    # Exibir resultado
    print("\nResultado:")
    print(f"Status Code: {result['statusCode']}")
    print(f"Body: {json.dumps(json.loads(result['body']), indent=2)}")
