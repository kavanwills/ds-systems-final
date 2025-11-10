# Final Project for Systems - Flask + Docker API

## Summary
This project exposes a small CSV dataset over HTTP using a Flask application running inside a Docker container. It shows environment-based configuration, containerization, and a simple data-serving endpoint.

## Project Structure
	.
	├── src/            # Flask app
	│   └── app.py
	├── assets/         # sample data
	│   └── sample.csv
	├── tests/          # smoke test
	│   └── smoke.sh
	├── Dockerfile
	├── requirements.txt
	├── .env.example
	└── README.md

## System Overview
- Framework: Flask
- Data source: assets/sample.csv (loaded into memory on startup)
- Endpoints:
	- GET /health -> returns {"status":"ok"}
	- GET /records -> returns all rows
	- GET /records?genre=pop -> filtered rows (example query param)
- Port: 5055
- Config: DATA_PATH environment variable

## How to Run
	docker build -t myapp .
	docker run --rm -p 5055:5055 --env-file .env.example myapp

In another terminal:
	curl http://localhost:5055/health
	curl http://localhost:5055/records
	curl "http://localhost:5055/records?genre=pop"

## Tests
Start the container (see “How to Run”), then in another terminal:
	./tests/smoke.sh

## Sample Responses
	$ curl http://localhost:5055/health
	{"status":"ok"}

	$ curl http://localhost:5055/records
	[{"genre":"pop","id":"1","name":"Song A"}, {"genre":"rock","id":"2","name":"Song B"}, {"genre":"pop","id":"3","name":"Song C"}, {"genre":"jazz","id":"4","name":"Song D"}]

	$ curl "http://localhost:5055/records?genre=pop"
	[{"genre":"pop","id":"1","name":"Song A"}, {"genre":"pop","id":"3","name":"Song C"}]

## Design Decisions
- Used Flask for a minimal REST-style API.
- Loaded CSV into memory to avoid database setup.
- Used environment variables (.env.example) so paths are not hardcoded.
- Packaged as a single container for reproducible runs.

## Architecture
	client (curl / browser)
	        ↓
	Flask app (src/app.py)
	        ↓
	in-memory data from assets/sample.csv
