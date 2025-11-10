# Final Project for Systems - Flask + Docker API

## Executive Summary

**Problem:** Data scientists and developers need quick, reproducible ways to serve small datasets via REST APIs for testing data pipelines, prototyping applications, or sharing data with team members without complex database setup.

**Solution:** This project exposes a small CSV dataset over HTTP using a Flask application running inside a Docker container. It shows environment-based configuration, containerization, and a simple data-serving endpoint that can be deployed consistently across any environment.

## System Overview

### Course Concept(s)

This project integrates concepts from multiple course modules, with primary focus on **Weeks 10-11: Infrastructure - Cloud Services / APIs / Containers**:

**Primary Concepts:**
- RESTful API design with Flask framework and HTTP methods
- Containerization with Docker for reproducible, portable deployments
- Health check endpoints for monitoring and orchestration
- Cloud deployment and continuous integration

**Supporting Concepts:**
- **Week 1:** Linux command-line interface and bash operations
- **Week 2:** Version control with Git and GitHub
- **Weeks 3-4:** Shell scripting for testing and automation (smoke.sh)
- **Week 5:** Data storage and management (CSV data loading and filtering)
- Environment-based configuration management

### Architecture Diagram
![Architecture Diagram](assets/architecture.png)

### Data/Models/Services
- **Data Source:** `assets/sample.csv` 
- **Size:** 4 records, ~150 bytes
- **Format:** CSV with columns: id, name, genre
- **License:** Sample data created for this project (no external dependencies or licensing requirements)
- **Framework:** Flask 3.0+ (MIT License)
- **Runtime:** Python 3.11 in Docker container
- **Production Server:** Gunicorn WSGI server

### System Components
- Framework: Flask
- Data source: assets/sample.csv (loaded into memory on startup)
- Endpoints:
  - GET /health -> returns {"status":"ok"}
  - GET /records -> returns all rows
  - GET /records?genre=pop -> filtered rows (example query param)
  - GET /metrics -> returns observability metrics
- Port: 5055 (configurable via PORT env var)
- Config: DATA_PATH environment variable

## Project Structure
```
.
├── src/            # Flask app
│   └── app.py
├── assets/         # sample data
│   └── sample.csv
│   └── architecture.png
├── tests/          # smoke test
│   └── smoke.sh
├── .github/        # CI/CD workflows
│   └── workflows/
│       └── ci.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── LICENSE
└── README.md
```

## How to Run (Local)

### Docker
```bash
docker build -t myapp .

docker run --rm -p 5055:5055 --env-file .env.example myapp
```

In another terminal:
```bash
curl http://localhost:5055/health
curl http://localhost:5055/metrics
curl http://localhost:5055/records
curl "http://localhost:5055/records?genre=pop"
```

## Design Decisions

### Why This Concept?
**Flask for minimal REST API:** Flask was chosen for its simplicity and minimal boilerplate, making it ideal for lightweight data-serving applications. Alternative frameworks like FastAPI offer async capabilities and auto-generated docs, but Flask's simplicity was sufficient for this use case.

**In-memory CSV loading:** Data is loaded into memory on startup to avoid database setup complexity. This is acceptable for small datasets (< 100MB) and provides fast read access. For larger datasets or write operations, a database like PostgreSQL or MongoDB would be necessary.

**Docker containerization:** Ensures the application runs identically across development, testing, and production environments. Alternative approaches like virtual environments or direct deployment lack the isolation and reproducibility that containers provide.

**Gunicorn for production:** The development Flask server is replaced with Gunicorn in production for better performance, stability, and concurrent request handling.

### Tradeoffs
- **Performance:** In-memory data provides fast reads but limits scalability to datasets that fit in RAM. No write persistence between container restarts.
- **Cost:** Single container deployment is cost-effective for development but would need orchestration (Kubernetes, ECS) for production scaling.
- **Complexity:** Minimal dependencies and simple architecture make the codebase easy to understand and maintain, at the cost of advanced features.
- **Maintainability:** Environment-based configuration and clear separation of concerns (app logic, data, tests) make the project easy to modify and extend.

### Technical Decisions
- Used Flask for a minimal REST-style API.
- Loaded CSV into memory to avoid database setup.
- Used environment variables (.env.example) so paths are not hardcoded.
- Packaged as a single container for reproducible runs.
- Added metrics endpoint for observability.
- Implemented structured logging for production monitoring.

### Security/Privacy
- No secrets are committed; configuration uses environment variables (.env.example).
- Input validation on query parameters to prevent injection attacks.
- Sample data contains no personally identifiable information.
- Container security: Base Python image is from official Docker Hub; dependencies are pinned in requirements.txt.

### Ops
- Container logs to stdout, so it can be monitored easily when deployed.
- Stateless design allows horizontal scaling behind a load balancer.
- **Observability:** `/metrics` endpoint provides request counts, uptime, and system stats.
- **CI/CD:** GitHub Actions automatically builds, tests, and validates every push.
- **Known limitations:** 
  - No data persistence (in-memory only)
  - No authentication/authorization
  - Limited to single-node deployment without orchestration
  - No rate limiting

## Results & Evaluation

### Sample Responses
```bash
$ curl http://localhost:5055/health
{"status":"ok","timestamp":"2025-11-10T14:30:00"}

$ curl http://localhost:5055/metrics
{"metrics":{"requests_total":42,"health_checks":10,"records_requests":15},"uptime_seconds":3600,"data_records":4}

$ curl http://localhost:5055/records
[{"genre":"pop","id":"1","name":"Song A"}, {"genre":"rock","id":"2","name":"Song B"}, {"genre":"pop","id":"3","name":"Song C"}, {"genre":"jazz","id":"4","name":"Song D"}]

$ curl "http://localhost:5055/records?genre=pop"
[{"genre":"pop","id":"1","name":"Song A"}, {"genre":"pop","id":"3","name":"Song C"}]
```

### Validation
The service responds to health checks and returns filtered data from the CSV.

- GET /health → 200 OK with {"status":"ok"}
- GET /records → returns all 4 demo rows
- GET /records?genre=pop → returns only rows with genre=pop
- GET /metrics → returns observability data

This demonstrates the container is healthy and the API can filter data.

### Tests
Start the container (see "How to Run"), then in another terminal:
```bash
./tests/smoke.sh
```

### CI/CD Pipeline
GitHub Actions automatically runs on every push:
- Builds Docker image
- Starts container
- Runs smoke tests on all endpoints
- Validates health, records, and metrics endpoints

View build status: [![CI](https://github.com/kavanwills/ds-systems-final/actions/workflows/ci.yml/badge.svg)](https://github.com/kavanwills/ds-systems-final/actions)

### Performance Notes
- **Startup time:** < 2 seconds from `docker run` to accepting requests
- **Response time:** < 10ms for health check, < 50ms for data endpoints
- **Resource footprint:** ~50MB container image, ~30MB RAM at runtime
- **Concurrency:** Gunicorn with 2 workers for production deployment

## What's Next

### Planned Improvements
- **Database integration:** Add PostgreSQL or MongoDB backend for persistent storage instead of in-memory CSV
- **Authentication:** Implement JWT token-based authentication for secure API access
- **Enhanced querying:** Add pagination, sorting, and multi-field filtering capabilities
- **API documentation:** Create Swagger/OpenAPI specification with interactive docs
- **Advanced observability:** Integrate Prometheus metrics and Grafana dashboards
- **Rate limiting:** Implement rate limiting using Flask-Limiter to prevent API abuse
- **Automated deployment:** Add CD pipeline to auto-deploy on successful CI builds
- **Data validation:** Add Pydantic schemas for request/response validation
- **CORS support:** Enable cross-origin requests for frontend integration

## Links
- **GitHub Repository:** https://github.com/kavanwills/ds-systems-final
- **Live Demo:** [YOUR-RENDER-URL-HERE] *(Add after deployment)*
- **CI/CD Pipeline:** https://github.com/kavanwills/ds-systems-final/actions

---

## License
This project is licensed under the MIT License - see the LICENSE file for details.
