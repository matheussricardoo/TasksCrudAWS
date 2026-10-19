"""HTTP smoke check against an explicitly started API; creates and deletes one task."""
import json
import os
from urllib.error import HTTPError
from urllib.request import Request, urlopen

BASE = os.getenv('API_URL', 'http://localhost:8080').rstrip('/')


def call(method, path, expected, body=None):
    data = json.dumps(body).encode() if body is not None else None
    request = Request(BASE + path, data=data, method=method,
                      headers={'Content-Type': 'application/json'})
    try:
        response = urlopen(request, timeout=10)
    except HTTPError as error:
        response = error
    with response:
        status = response.status
        payload = json.loads(response.read())
    if status != expected:
        raise AssertionError(f'{method} {path}: expected {expected}, received {status}')
    return payload


def main():
    task_id = None
    try:
        assert call('GET', '/health', 200)['database'] == 'connected'
        call('POST', '/tasks', 400, {})
        task = call('POST', '/tasks', 201, {'title': 'HTTP smoke check', 'priority': 'high'})['data']
        task_id = task['id']
        assert call('GET', f'/tasks/{task_id}', 200)['data']['title'] == 'HTTP smoke check'
        filtered = call('GET', '/tasks?status=pending&priority=high', 200)['data']
        assert any(item['id'] == task_id for item in filtered)
        assert call('PUT', f'/tasks/{task_id}', 200, {'status': 'completed'})['data']['status'] == 'completed'
        call('DELETE', f'/tasks/{task_id}', 200)
        call('GET', f'/tasks/{task_id}', 404)
        task_id = None
        print('HTTP CRUD smoke check passed')
    finally:
        if task_id is not None:
            # Only delete the exact ID returned by this run's successful POST.
            call('DELETE', f'/tasks/{task_id}', 200)


if __name__ == '__main__':
    main()
