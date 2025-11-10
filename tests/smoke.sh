#!/bin/bash

echo "Running smoke tests..."

# Test health endpoint
echo "Testing /health..."
curl -f http://localhost:5055/health || exit 1
echo " ✓ Health check passed"

# Test records endpoint
echo "Testing /records..."
curl -f http://localhost:5055/records || exit 1
echo " ✓ Records endpoint passed"

# Test metrics endpoint
echo "Testing /metrics..."
curl -f http://localhost:5055/metrics || exit 1
echo " ✓ Metrics endpoint passed"

# Test filtered records
echo "Testing /records?genre=pop..."
curl -f "http://localhost:5055/records?genre=pop" || exit 1
echo " ✓ Filtered records passed"

echo ""
echo "All smoke tests passed! ✓"
