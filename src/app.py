import os
import csv
from flask import Flask, request, jsonify

app = Flask(__name__)

DATA_PATH = os.getenv("DATA_PATH", "assets/sample.csv")

records = []
with open(DATA_PATH, newline="") as f:
	reader = csv.DictReader(f)
	for row in reader:
		records.append(row)

@app.route("/health")
def get_health():
	return jsonify({"status": "ok"}), 200

@app.route("/records")
def get_records():
	genre = request.args.get("genre")
	filtered = records
	if genre:
		filtered = [r for r in records if r.get("genre", "").lower() == genre.lower()]
	return jsonify(filtered), 200

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5055)
