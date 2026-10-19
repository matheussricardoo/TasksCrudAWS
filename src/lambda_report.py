"""Report handler consuming the task API over HTTP.

Original authors: Matheus Ricardo and Priscila Herculano.
Set API_URL to the complete /tasks URL. No AWS calls are made by this module.
"""
import json
import logging
import os
import urllib3

API_URL = os.getenv('API_URL', 'http://localhost:8080/tasks')
http = urllib3.PoolManager()
logger = logging.getLogger(__name__)


def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(body, ensure_ascii=False),
    }


def lambda_handler(event, context):
    """Return a JSON-string body compatible with API Gateway proxy integration."""
    try:
        result = http.request('GET', API_URL, timeout=10.0, retries=False)
        if result.status != 200:
            raise ValueError('Upstream API returned a non-200 status')
        payload = json.loads(result.data.decode('utf-8'))
        tasks = payload.get('data') if isinstance(payload, dict) else payload
        if not isinstance(tasks, list) or any(not isinstance(task, dict) for task in tasks):
            raise ValueError('Expected an array of task objects')
        total = len(tasks)
        completed = sum(task.get('status') == 'completed' for task in tasks)
        rate = round(completed / total * 100, 2) if total else 0
        return response(200, {
            'success': True,
            'report': {
                'total_tasks': total,
                'by_status': {key: sum(task.get('status') == key for task in tasks)
                              for key in ('completed', 'in_progress', 'pending')},
                'by_priority': {key: sum(task.get('priority') == key for task in tasks)
                                for key in ('high', 'medium', 'low')},
                'completion_rate': rate,
                'completion_percentage': f'{rate}%',
            },
            # This legacy field is a request identifier, not a date/time timestamp.
            'timestamp': getattr(context, 'aws_request_id', 'local-test'),
        })
    except urllib3.exceptions.TimeoutError:
        return response(504, {'success': False, 'error': 'Timeout connecting to API'})
    except Exception:
        logger.exception('Report generation failed')
        return response(500, {'success': False, 'error': 'Unable to generate report'})


if __name__ == '__main__':
    print(json.dumps(lambda_handler({}, None), indent=2))
