#!/bin/bash
set -e

echo "Starting Frontend (Dash)..."
cd /app

# Ejecutar el frontend Dash
python -m frontend.app
