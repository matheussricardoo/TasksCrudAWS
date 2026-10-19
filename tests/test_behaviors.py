"""Isolated behavior checks: no database, HTTP server or AWS access."""
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import urllib3

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import app as api
import lambda_report as reports


class ApiValidationTests(unittest.TestCase):
    def test_invalid_creation_is_rejected_before_database_access(self):
        client = api.app.test_client()
        with patch.object(api, 'get_db_connection') as connect:
            for payload in ({}, {'title': 'Task', 'status': 'invalid'},
                            {'title': 'Task', 'priority': 'invalid'}):
                with self.subTest(payload=payload):
                    response = client.post('/tasks', json=payload)
                    self.assertEqual(response.status_code, 400)
                    self.assertFalse(response.json['success'])
            connect.assert_not_called()

    def test_health_reports_database_failure(self):
        with patch.object(api, 'get_db_connection', side_effect=RuntimeError('unavailable')):
            response = api.app.test_client().get('/health')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json['database'], 'disconnected')


class ReportTests(unittest.TestCase):
    def invoke(self, tasks):
        response = Mock(status=200, data=json.dumps({'data': tasks}).encode())
        with patch.object(reports.http, 'request', return_value=response):
            result = reports.lambda_handler({}, None)
        self.assertEqual(result['statusCode'], 200)
        return json.loads(result['body'])['report']

    def test_counts_and_completion_percentage(self):
        report = self.invoke([
            {'status': 'completed', 'priority': 'high'},
            {'status': 'pending', 'priority': 'medium'},
            {'status': 'in_progress', 'priority': 'low'},
        ])
        self.assertEqual(report['total_tasks'], 3)
        self.assertEqual(report['by_status'], {'completed': 1, 'pending': 1, 'in_progress': 1})
        self.assertEqual(report['by_priority'], {'high': 1, 'medium': 1, 'low': 1})
        self.assertEqual(report['completion_rate'], 33.33)

    def test_empty_list_has_zero_completion(self):
        report = self.invoke([])
        self.assertEqual(report['total_tasks'], 0)
        self.assertEqual(report['completion_rate'], 0)

    def test_upstream_failure_is_not_reported_as_success(self):
        with patch.object(reports.http, 'request', return_value=Mock(status=503)):
            result = reports.lambda_handler({}, None)
        self.assertEqual(result['statusCode'], 500)
        self.assertFalse(json.loads(result['body'])['success'])

    def test_upstream_timeout_returns_504(self):
        with patch.object(reports.http, 'request', side_effect=urllib3.exceptions.TimeoutError()):
            result = reports.lambda_handler({}, None)
        self.assertEqual(result['statusCode'], 504)
        self.assertFalse(json.loads(result['body'])['success'])




class DatabaseBoundaryTests(unittest.TestCase):
    def test_malformed_payloads_are_400_without_database_access(self):
        client = api.app.test_client()
        with patch.object(api, 'get_db_connection') as connect:
            for payload in ([], {'title': ' '}, {'title': 'x' * 201}, {'title': 123}, {'title': 'ok', 'description': []}):
                with self.subTest(payload=payload):
                    self.assertEqual(client.post('/tasks', json=payload).status_code, 400)
            self.assertEqual(client.post('/tasks', data='{', content_type='application/json').status_code, 400)
            self.assertEqual(client.put('/tasks/1', json={'title': ''}).status_code, 400)
            connect.assert_not_called()

    def test_database_failure_rolls_back_and_closes_connection(self):
        from unittest.mock import MagicMock
        connection = MagicMock()
        cursor = connection.cursor.return_value.__enter__.return_value
        cursor.execute.side_effect = RuntimeError('secret database details')
        with patch.object(api, 'get_db_connection', return_value=connection):
            result = api.app.test_client().get('/tasks')
        self.assertEqual(result.status_code, 500)
        self.assertNotIn('secret', result.get_data(as_text=True))
        connection.rollback.assert_called_once()
        connection.close.assert_called_once()

    def test_filters_are_parameterized_and_connection_is_closed(self):
        from unittest.mock import MagicMock
        connection = MagicMock()
        cursor = connection.cursor.return_value.__enter__.return_value
        cursor.fetchall.return_value = []
        with patch.object(api, 'get_db_connection', return_value=connection):
            result = api.app.test_client().get('/tasks?status=pending&priority=high')
        self.assertEqual(result.status_code, 200)
        query, params = cursor.execute.call_args.args
        self.assertIn('status = %s', query)
        self.assertEqual(params, ['pending', 'high'])
        connection.close.assert_called_once()




class WriteBoundaryTests(unittest.TestCase):
    def test_valid_creation_commits_and_closes(self):
        from unittest.mock import MagicMock
        connection = MagicMock()
        cursor = connection.cursor.return_value.__enter__.return_value
        cursor.lastrowid = 42
        cursor.fetchone.return_value = {'id': 42, 'title': 'New task', 'status': 'pending', 'priority': 'medium'}
        with patch.object(api, 'get_db_connection', return_value=connection):
            result = api.app.test_client().post('/tasks', json={'title': 'New task'})
        self.assertEqual(result.status_code, 201)
        self.assertEqual(result.json['data']['id'], 42)
        self.assertEqual(cursor.execute.call_args_list[0].args[1], ('New task', '', 'pending', 'medium'))
        connection.commit.assert_called_once()
        connection.close.assert_called_once()

    def test_deleting_missing_task_is_404_and_closes(self):
        from unittest.mock import MagicMock
        connection = MagicMock()
        connection.cursor.return_value.__enter__.return_value.rowcount = 0
        with patch.object(api, 'get_db_connection', return_value=connection):
            result = api.app.test_client().delete('/tasks/999')
        self.assertEqual(result.status_code, 404)
        connection.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
