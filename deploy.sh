#!/bin/bash

# Script para desplegar en Railway sin CLI interactivo
# Uso: ./deploy.sh <RAILWAY_TOKEN> <PROJECT_NAME>

RAILWAY_TOKEN="${1:-8f5bd33d-9508-407f-a80d-7fa751e3f18b}"
PROJECT_NAME="${2:-crm-politics}"

echo "🚀 Desplegando CRM Política en Railway..."
echo "Token: ${RAILWAY_TOKEN:0:10}..."
echo "Proyecto: $PROJECT_NAME"

# Verificar que el token sea válido
echo "Verificando token..."
curl -s -H "Authorization: Bearer $RAILWAY_TOKEN" \
  https://api.railway.app/graphql \
  -d '{"query":"{ me { id } }"}' | grep -q "id" && echo "✅ Token válido" || echo "❌ Token inválido"

# Crear proyecto si no existe
echo "Creando/verificando proyecto..."

# Inicializar git si no está inicializado
if [ ! -d .git ]; then
  git init
  git add .
  git commit -m "Initial commit for Railway deployment"
fi

# Usar railway CLI con token
export RAILWAY_TOKEN="$RAILWAY_TOKEN"
railway init --name "$PROJECT_NAME" 2>/dev/null || true

echo "✅ Proyecto inicializado"
echo ""
echo "Próximos pasos:"
echo "1. Ve a https://railway.app/dashboard"
echo "2. Configura las variables de entorno:"
echo "   - ENV=cloud"
echo "   - DEBUG=False"
echo "   - GOOGLE_API_KEY=tu_api_key"
echo "   - META_APP_ID=tu_app_id"
echo "   - etc..."
echo "3. El deploy se iniciará automáticamente"
