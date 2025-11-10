#!/usr/bin/env bash
set -e

docker build -t myapp .
docker run --rm -p 5055:5055 --env-file .env.example myapp

