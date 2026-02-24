# Setup de Railway para CRM Política

## Estado actual
✅ Código pusheado a GitHub: https://github.com/IngIndependiente/politica
✅ Dockerfile creado para Railway
✅ railway.json configurado
✅ Variables de entorno listas

## Pasos para desplegar en Railway

### 1. Ve a Railway Dashboard
https://railway.app/dashboard

### 2. Crea un nuevo proyecto
- Click en "New Project"
- Selecciona "Deploy from GitHub"
- Conecta tu cuenta de GitHub si no está conectada
- Selecciona el repositorio: `IngIndependiente/politica`

### 3. Railway detectará automáticamente:
- ✅ Dockerfile
- ✅ railway.json
- ✅ requirements.txt

### 4. Configura las variables de entorno en Railway:

```
# Modo
ENV=cloud
DEBUG=False

# Servidor
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# Google Gemini API
GOOGLE_API_KEY=tu_api_key_aqui

# Meta/Facebook API
META_APP_ID=tu_app_id
META_APP_SECRET=tu_app_secret
META_ACCESS_TOKEN=tu_access_token
META_VERIFY_TOKEN=agente_politico_token_secreto

# WhatsApp Business API
WHATSAPP_PHONE_NUMBER_ID=tu_phone_id
WHATSAPP_BUSINESS_ACCOUNT_ID=tu_business_id
WHATSAPP_VERIFY_TOKEN=whatsapp_verify_token_secreto

# OAuth Redirect URI
OAUTH_REDIRECT_URI=https://tu-dominio-railway.app/auth/facebook/callback

# Base de datos
DATABASE_URL=sqlite:///./agente_politico.db

# Admin
ADMIN_TOKEN=genera_un_token_seguro
SYNC_PASSWORD=CRMpoliticos2026!
```

### 5. Click en "Deploy"
Railway hará el resto automáticamente.

## Después del deploy

1. Railway te dará una URL pública (ej: `https://crm-politics-backend.railway.app`)
2. Accede a esa URL para verificar que el backend funciona
3. Verifica los logs en Railway si hay errores

## Para el Frontend (Dash)

Si quieres desplegar el frontend en un servicio separado:

1. Crea otro proyecto en Railway desde el mismo repo
2. Configura variables:
   ```
   ENV=cloud
   DEBUG=False
   FRONTEND_HOST=0.0.0.0
   FRONTEND_PORT=8050
   BACKEND_URL=https://crm-politics-backend.railway.app
   GOOGLE_API_KEY=tu_api_key
   ```
3. En "Build" → selecciona `Procfile.frontend`
4. Deploy

## Troubleshooting

**El deploy falla:**
- Revisa los logs en Railway
- Verifica que todas las variables de entorno estén configuradas
- Confirma que el Dockerfile es válido

**Backend no responde:**
- Verifica que `ENV=cloud` está configurado
- Revisa que `DEBUG=False`
- Mira los logs: Railway → Logs

**Base de datos no persiste:**
- Usa PostgreSQL en lugar de SQLite
- Railway proporciona PostgreSQL integrado
- Configura `DATABASE_URL=postgresql://...`

## Cambios realizados en el código

1. **backend/config.py** — Agregada variable `BACKEND_URL` para Railway
2. **frontend/app.py** — Cambiar `debug=True` a `debug=config.DEBUG`
3. **Dockerfile** — Creado para Railway
4. **railway.json** — Configuración de Railway
5. **Procfile.backend** y **Procfile.frontend** — Para servicios separados
