#!/bin/bash
set -e

echo "🚀 Iniciando CRM Política en Railway..."
echo "Ambiente: ${ENV:-local}"
echo "Debug: ${DEBUG:-False}"
echo "Puerto: ${PORT:-8000}"

# Instalar dependencias si es necesario
echo "📦 Verificando dependencias..."
pip install --no-cache-dir -q -r requirements.txt 2>/dev/null || pip install -r requirements.txt

# Iniciar el backend
echo "✅ Iniciando backend..."
python -m uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}
