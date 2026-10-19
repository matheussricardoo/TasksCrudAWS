# Academic AWS deployment notes

The project was developed for Cloud Developing 2025/2 in the AWS Learner Lab context. These notes describe the intended integration, not proof of active resources. There is no confirmed public demo or infrastructure-as-code deployment in this repository.

For a reproducible local API/MySQL setup, use the [README](../README.md). It does not require AWS. No resources were created during the portfolio review. A cloud deployment can incur charges; no Free Tier eligibility or current price is assumed.

## Architecture

```text
API Gateway -- HTTP integration --> EC2 / Gunicorn container --> RDS MySQL
            -- Lambda proxy ------> report handler -- HTTP --> API /tasks
```

RDS should only accept database connections from the API's security group. Restrict administrative access and review how the gateway and Lambda reach the API. The presence of API Gateway alone does not prevent direct EC2 access. The repository does not verify any current security group, subnet, IAM role or logging configuration.

## Configuration checklist

1. Independently approve the resources and expected charges before creating them.
2. Configure the network, private database access and least-privilege roles. Do not expose MySQL publicly.
3. Load `deployment/sql/schema.sql` on the selected database. This SQL also inserts sample rows; do not repeatedly execute it against a populated environment unless the additional rows are intended.
4. Pass DB_HOST, DB_USER, DB_PASSWORD and DB_NAME to the API container through its environment. The local Compose file always points to its own MySQL container; it is not a cloud deployment file.
5. Package the report handler with its dependency and set API_URL to a reachable `/tasks` endpoint.
6. Configure gateway integrations and explicitly test status/body mapping, timeouts and CORS.

## API container commands

From the repository root, on a host where Docker is already configured:

```bash
docker build -t tasks-api:review -f deployment/Dockerfile .
# Create .env privately with the four DB_* variables before running this command.
docker run --name tasks-api --env-file .env -p 8080:8080 tasks-api:review
```

`.env.example` is an external-database template. The application does not automatically load it; `docker run --env-file` supplies values. DB_PORT and PORT are not configurable by the API; MySQL uses 3306 and Gunicorn binds 8080. Do not commit actual credentials or private keys.

## Lambda package

This packages files locally without contacting AWS:

```bash
python3 -m pip install -r src/requirements-lambda.txt --target build/lambda
cp src/lambda_report.py build/lambda/
(cd build/lambda && python3 -m zipfile -c ../../lambda-report.zip .)
```

Configure the handler as `lambda_report.lambda_handler`. Select and validate the Python runtime and role in the deployment environment. Include the dependency instead of assuming urllib3 is provided by the managed runtime. Set a function timeout longer than the handler's 10-second upstream request timeout.

## Validation and limitations

Check `/health`, run the CRUD workflow in the README, then invoke the report handler and gateway integration. Verify returned status codes; POST creation is 201, not 200. Database health does not prove security or full CRUD correctness.

Before a real public deployment, address authentication, authorization, throttling, TLS, credentials, runtime/dependency maintenance, backups, monitoring, costs and cleanup. These are future operational requirements, not implemented guarantees. Existing `tests/scripts/deploy.*` helpers are manual scripts and must be reviewed before use; they can stop containers and prune images. They are not a CI/CD pipeline.

Original team: Matheus Ricardo (development, AWS infrastructure, documentation) and Priscila Herculano (development, testing, AWS infrastructure).
