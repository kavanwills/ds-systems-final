from flask import Flask, jsonify, request
import csv
import os
import logging
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Simple metrics tracking
metrics = {
    "requests_total": 0,
    "health_checks": 0,
    "records_requests": 0,
    "start_time": datetime.now().isoformat()
}

# Load data
DATA_PATH = os.getenv("DATA_PATH", "assets/sample.csv")
data = []

try:
    with open(DATA_PATH, "r") as f:
        reader = csv.DictReader(f)
        data = list(reader)
    logger.info(f"Loaded {len(data)} records from {DATA_PATH}")
except Exception as e:
    logger.error(f"Failed to load data: {e}")

@app.before_request
def before_request():
    metrics["requests_total"] += 1
    logger.info(f"Request: {request.method} {request.path}")

@app.route("/health")
def health():
    metrics["health_checks"] += 1
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})

@app.route("/metrics")
def get_metrics():
    """Observability endpoint for monitoring"""
    return jsonify({
        "metrics": metrics,
        "uptime_seconds": (datetime.now() - datetime.fromisoformat(metrics["start_time"])).total_seconds(),
        "data_records": len(data)
    })

@app.route("/records")
def records():
    metrics["records_requests"] += 1
    genre = request.args.get("genre")
    if genre:
        filtered = [r for r in data if r.get("genre") == genre]
        logger.info(f"Filtered {len(filtered)} records for genre={genre}")
        return jsonify(filtered)
    return jsonify(data)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5055))
    app.run(host="0.0.0.0", port=port)
