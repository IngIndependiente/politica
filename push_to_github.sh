#!/bin/bash

# Script para pushear a GitHub usando token
# Uso: ./push_to_github.sh <GITHUB_TOKEN>

GITHUB_TOKEN="${1}"
REPO="IngIndependiente/politica"

if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Error: Debes proporcionar un token de GitHub"
    echo "Uso: ./push_to_github.sh <GITHUB_TOKEN>"
    echo ""
    echo "Para obtener un token:"
    echo "1. Ve a https://github.com/settings/tokens"
    echo "2. Click en 'Generate new token (classic)'"
    echo "3. Selecciona 'repo' scope"
    echo "4. Copia el token y úsalo aquí"
    exit 1
fi

echo "🚀 Pusheando a GitHub..."
echo "Repositorio: $REPO"

# Configurar URL con token
git remote set-url origin "https://${GITHUB_TOKEN}@github.com/${REPO}.git"

# Push
git push -u origin main

if [ $? -eq 0 ]; then
    echo "✅ Push completado exitosamente"
    echo "Verifica en: https://github.com/$REPO"
else
    echo "❌ Error en el push"
    exit 1
fi
