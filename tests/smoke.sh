#!/usr/bin/env bash
set -e 
curl -s http://localhost:5055/health | grep ok
echo "smoke test passed"

