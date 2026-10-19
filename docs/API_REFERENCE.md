# Task API reference

This document describes the Flask implementation and separate report handler. Base URL for local requests: `http://localhost:8080`. No public AWS endpoint is confirmed.

## Task model

| Field | Contract |
|---|---|
| id | Database-generated integer |
| title | Non-blank string, at most 200 characters |
| description | Optional string; defaults to an empty string on creation |
| status | pending (default), in_progress, completed |
| priority | low, medium (default), high |
| created_at, updated_at | MySQL timestamps serialized by Flask; not guaranteed to be ISO 8601 |

## Routes

| Method | Route | Success | Failure cases |
|---|---|---|---|
| GET | /health | 200: healthy and database connected | 500: database disconnected |
| GET | /tasks | 200: success, count, data array | 500: database failure |
| GET | /tasks/{id} | 200: success, data object | 404: missing task |
| POST | /tasks | 201: success, message, data | 400: invalid JSON or field values |
| PUT | /tasks/{id} | 200: success, message, data | 400: invalid data; 404: missing task |
| DELETE | /tasks/{id} | 200: success, message | 404: missing task |

PUT supports partial updates. Only title, description, status and priority can be updated. Unknown fields are ignored; an update containing no supported fields is rejected. Query filters on GET /tasks are optional `status` and `priority` values combined with AND. Results are sorted by creation time descending; no pagination is implemented.

```bash
curl -i 'http://localhost:8080/tasks?status=pending&priority=high'
curl -i -X POST http://localhost:8080/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Review API","description":"Local example","priority":"high"}'
```

Use `data.id` from the creation response for retrieval, update and deletion. Responses such as `{ "success": false, "error": "Task not found" }` describe task failures. Database exceptions are logged on the server and return a generic 500 response. Framework-level errors such as unknown routes can use Flask's default HTML response.

## Report handler

`src/lambda_report.py` is not a Flask route. It fetches the complete API_URL (default `http://localhost:8080/tasks`) and counts tasks by status/priority and completion percentage. An empty list produces zero completion. Invalid upstream responses produce statusCode 500; HTTP timeouts produce 504.

The handler returns an API Gateway proxy envelope:

```json
{
  "statusCode": 200,
  "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
  "body": "{\"success\": true, \"report\": {\"total_tasks\": 0, \"by_status\": {\"completed\": 0, \"in_progress\": 0, \"pending\": 0}, \"by_priority\": {\"high\": 0, \"medium\": 0, \"low\": 0}, \"completion_rate\": 0, \"completion_percentage\": \"0%\"}, \"timestamp\": \"local-test\"}"
}
```

The `body` is a JSON string. With API Gateway proxy integration, HTTP clients receive its decoded content as the response body. The legacy `timestamp` field contains a request identifier, not a time measurement.

## Access and limits

The API has no authentication, authorization or rate limiting. CORS is permissive. This academic implementation is not intended for public deployment with sensitive data. See the [README](../README.md) for local execution and validation.
