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


if __name__ == '__main__':
    unittest.main()
