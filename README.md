# TasksCrudAWS

Academic task management API developed for **Cloud Developing 2025/2**, in the AWS Learner Lab context. The project uses a familiar domain to practice REST endpoints, relational persistence, containers, and integration between AWS services.

The backend is implemented in **Python, Flask and MySQL**, with Gunicorn and Docker. A separate Python Lambda handler generates reports by consuming the API over HTTP. This repository demonstrates these technologies; it does not contain Java, Go or Rust implementations.

**Project status:** educational implementation with limitations described below. No live deployment is confirmed. AWS addresses in the documentation are placeholders, not a public demo.

## Implemented functionality

- Create, list, retrieve, partially update via `PUT`, and delete tasks.
- Filter the task list by status and priority; order by creation date descending.
- Task fields: title, description, status, priority, and database-managed timestamps.
- Check required title on creation and allowed status/priority values on creation and update.
- Database connectivity check at `/health`.
- Report handler: total tasks, counts by status and priority, and completion percentage; handles upstream errors and timeouts.

| Method | Path | Successful response | Runtime |
|---|---|---|---|
| GET | `/health` | 200, database connected | Flask |
| GET | `/tasks` | 200, list and count | Flask |
| GET | `/tasks/{id}` | 200, task | Flask |
| POST | `/tasks` | 201, created task | Flask |
| PUT | `/tasks/{id}` | 200, updated task | Flask |
| DELETE | `/tasks/{id}` | 200, confirmation | Flask |
| GET | `/report` | 200, report | Requires AWS gateway/Lambda configuration |

Missing task IDs return 404. Supported validation failures return 400; database failures return 500. `/report` is **not a Flask route** and is not served by the local Compose stack.

## Architecture and technical choices

```text
Local:  HTTP client -> Flask / Gunicorn container -> MySQL 8 container

AWS architecture described in the academic deployment guide:
        API Gateway -> EC2 / Docker / Flask -> RDS MySQL
                    -> Lambda -> HTTP GET on Flask /tasks
```

- Flask handles HTTP and JSON; PyMySQL executes parameterized SQL for task values and filters. There is no ORM.
- MySQL stores tasks with enum fields and indexes on status, priority and creation date. The initialization SQL also inserts nine example tasks on a fresh database.
- Compose waits for the MySQL health check before starting the API and persists database files in a named volume.
- Gunicorn runs the containerized API with two workers.
- The report handler reuses `/tasks` rather than connecting directly to the database. This keeps SQL in the API, but transfers the full task list and depends on API availability.
- The AWS guide describes a private RDS database and security groups. Their current configuration is not verifiable from this repository. Deployment scripts are manual helpers, not a CI/CD pipeline or infrastructure as code.

## Run locally

Requirements: Git, Docker Engine with a running daemon, Docker Compose, and curl. Commands below run from the repository root in a POSIX shell.

```bash
git clone https://github.com/matheussricardoo/TasksCrudAWS.git
cd TasksCrudAWS

# Check the daemon and validate the Compose configuration.
docker info
docker compose -f deployment/docker-compose.yml config --quiet

# Build the API and start local MySQL and API containers.
docker compose -f deployment/docker-compose.yml up --build -d
docker compose -f deployment/docker-compose.yml ps
docker compose -f deployment/docker-compose.yml logs --tail=100 mysql api
```

Wait for MySQL initialization and a successful `/health` response before testing. The API is available at `http://localhost:8080`; MySQL is published on host port `3307` and reached by the API as `mysql:3306`.

**No AWS account, RDS instance, API key, or paid cloud service is required for this local stack.** It downloads container images and Python packages. Compose supplies local database settings directly; copying `.env.example` is unnecessary and does not override these settings. That template is for an external database deployment.

The committed database passwords are development defaults. The current Compose ports are published on all host interfaces; use a trusted local environment and do not expose this setup publicly.

```bash
# Stop and remove containers; preserve database data.
docker compose -f deployment/docker-compose.yml down
```

The schema and sample rows are initialized only when the MySQL volume is empty. `down --volumes` also deletes local database data; use it only when intentionally resetting the environment.

## Validate functionality

With the local stack running, verify database connectivity, task creation, retrieval, filtering, update and deletion. Use the ID returned by POST instead of assuming an existing task ID:

```bash
curl -i http://localhost:8080/health
curl -i http://localhost:8080/tasks
curl -i -X POST http://localhost:8080/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Portfolio smoke test","priority":"high"}'

# Replace 123 with data.id from the POST response (expected HTTP 201).
curl -i http://localhost:8080/tasks/123
curl -i 'http://localhost:8080/tasks?status=pending&priority=high'
curl -i -X PUT http://localhost:8080/tasks/123 \
  -H 'Content-Type: application/json' -d '{"status":"completed"}'
curl -i -X DELETE http://localhost:8080/tasks/123
curl -i http://localhost:8080/tasks/123  # Expected: HTTP 404 after deletion

# Expected: HTTP 400 (required title missing).
curl -i -X POST http://localhost:8080/tasks \
  -H 'Content-Type: application/json' -d '{}'
```

### Isolated tests and local report invocation

Python 3.9+ and a virtual environment are needed for these commands. `urllib3` is installed separately because the Lambda dependency is not included in the API requirements.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r src/requirements.txt urllib3==2.2.3
python -m unittest discover -s tests -p 'test_*.py' -v

# Requires the local API and MySQL above; does not invoke AWS.
API_URL=http://localhost:8080/tasks python src/lambda_report.py
```

The handler returns an API Gateway response envelope whose `body` is a JSON string. Direct invocation prints this result; it does not create a local `/report` endpoint.

The isolated tests mock database/HTTP boundaries and cover validation, database failure reporting, report calculations, an empty task list, and upstream failures. They do not prove MySQL integration or AWS deployment. The older scripts in `tests/scripts/` are manual helpers; `test-api.sh` prints responses without asserting every result and should not be treated as evidence that all tests passed.

**Verification during this documentation review:** Compose configuration validated and isolated Python tests executed. Full container build, database initialization, HTTP CRUD integration and live report invocation remain unverified because the Docker daemon was unavailable. No AWS resources were created or contacted to validate a deployment.

## Limitations and next steps

- No authentication, authorization, per-user task isolation or application rate limiting.
- CORS is permissive; it is not an access-control mechanism.
- Input validation is partial: types, whitespace-only titles and title length need consistent handling; malformed JSON can become a 500 response.
- Error responses can expose internal exception details. Connection cleanup and transaction rollback need improvement on failure paths.
- No pagination; list and report operations load all tasks.
- Development credentials are present in Compose and application/container defaults. Secret management and configuration validation are future work.
- No automated deployment pipeline, infrastructure as code, or demonstrated production monitoring, backup recovery or load testing.
- Runtime and dependency updates, broader integration tests, and AWS packaging/configuration need review before any public deployment.

Cloud deployment is optional and may incur charges. The repository does not establish current free-tier eligibility, prices, or running resources. Do not interpret the academic guide as a guarantee of free hosting.

## Repository guide

| Path | Purpose |
|---|---|
| `src/app.py` | Flask API and database access |
| `src/lambda_report.py` | HTTP-based report handler |
| `src/requirements.txt` | API dependencies |
| `deployment/docker-compose.yml` | Local MySQL and API stack |
| `deployment/Dockerfile` | Gunicorn API image |
| `deployment/sql/schema.sql` | Schema, indexes and sample tasks |
| `tests/test_behaviors.py` | Isolated behavior tests |
| `tests/scripts/` | Existing manual API and deployment helpers |
| [API reference](docs/REFERENCIA_API.md) | Extended examples; see implementation notes at the top |
| [AWS deployment guide](docs/GUIA_IMPLANTACAO.md) | Academic cloud setup; not required locally |

## Team and contributions

Credits retained from the original project documentation; these are team responsibilities, not a claim of sole authorship or a verified breakdown of individual commits:

- **Matheus Ricardo:** development, AWS infrastructure, and documentation. [GitHub](https://github.com/matheussricardoo) · [LinkedIn](https://www.linkedin.com/in/matheussricardoo/)
- **Priscila Herculano:** development, testing, and AWS infrastructure. [GitHub](https://github.com/PriHerculano) · [LinkedIn](https://www.linkedin.com/in/priscilaherculano/)

## License

[MIT](LICENSE).
