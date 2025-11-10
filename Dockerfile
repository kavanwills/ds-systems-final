FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src
COPY assets/ ./assets

ENV DATA_PATH=/app/assets/sample.csv

EXPOSE 5055

CMD ["python", "src/app.py"]
