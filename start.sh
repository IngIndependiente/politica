#!/bin/bash
set -e

echo "🚀 Iniciando CRM Política..."
echo "Ambiente: ${ENV:-local}"
echo "Puerto: ${PORT:-8000}"

# Inicializar base de datos (crear tablas si no existen, esperar PostgreSQL)
echo "� Inicializando base de datos..."
python init_db.py
echo "✅ Base de datos lista"

# Iniciar el backend
echo "🌐 Iniciando servidor..."
python -m uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}
