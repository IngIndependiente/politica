#!/bin/bash
set -e

echo "Starting Frontend (Dash)..."
echo "PORT=$PORT"

# Railway asigna $PORT - usarlo como FRONTEND_PORT
export FRONTEND_PORT=${PORT:-8050}
export BACKEND_URL=${BACKEND_URL:-"https://web-production-5dbe.up.railway.app"}

echo "FRONTEND_PORT=$FRONTEND_PORT"
echo "BACKEND_URL=$BACKEND_URL"

cd /app
python -m frontend.app
