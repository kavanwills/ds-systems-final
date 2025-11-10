FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

ENV PORT=5055
ENV DATA_PATH=assets/sample.csv

# Expose port
EXPOSE $PORT

# Use gunicorn for production
CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 60 --access-logfile - --error-logfile - src.app:app
