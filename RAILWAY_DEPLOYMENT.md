# Despliegue en Railway

## Estructura de despliegue

El CRM tiene dos servicios que deben correr en Railway:

1. **Backend (FastAPI)** — API en puerto 8000
2. **Frontend (Dash)** — Dashboard en puerto 8050

## Opción 1: Dos servicios separados en Railway (RECOMENDADO)

### Paso 1: Crear servicio Backend

1. En Railway, crear nuevo proyecto desde GitHub
2. Seleccionar rama `main` (o la que uses)
3. Configurar variables de entorno:
   ```
   ENV=cloud
   DEBUG=False
   BACKEND_HOST=0.0.0.0
   BACKEND_PORT=8000
   GOOGLE_API_KEY=tu_api_key
   META_APP_ID=tu_app_id
   META_APP_SECRET=tu_secret
   META_ACCESS_TOKEN=tu_token
   WHATSAPP_PHONE_NUMBER_ID=tu_id
   WHATSAPP_BUSINESS_ACCOUNT_ID=tu_id
   DATABASE_URL=postgresql://...  # Si usas PostgreSQL
   ```
4. Procfile: `Procfile.backend`
5. Deploy

**Nota:** Railway te dará una URL pública, ej: `https://crm-politics-backend.railway.app`

### Paso 2: Crear servicio Frontend

1. En Railway, crear otro nuevo proyecto desde el mismo repo
2. Configurar variables de entorno:
   ```
   ENV=cloud
   DEBUG=False
   FRONTEND_HOST=0.0.0.0
   FRONTEND_PORT=8050
   BACKEND_URL=https://crm-politics-backend.railway.app  # URL del backend del paso anterior
   GOOGLE_API_KEY=tu_api_key
   ```
3. Procfile: `Procfile.frontend`
4. Deploy

## Opción 2: Un solo servicio con ambos (alternativa)

Si prefieres todo en uno, crear un script `run.sh`:

```bash
#!/bin/bash
# Iniciar backend en background
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Iniciar frontend
python -m frontend.app --host 0.0.0.0 --port 8050

# Cleanup
kill $BACKEND_PID
```

Y en Procfile:
```
web: bash run.sh
```

**Desventaja:** Si uno falla, ambos se caen.

## Variables de entorno críticas para Railway

| Variable | Valor | Notas |
|----------|-------|-------|
| `ENV` | `cloud` | Activa modo producción |
| `DEBUG` | `False` | Desactiva debug mode |
| `BACKEND_URL` | `https://crm-politics-backend.railway.app` | URL pública del backend (solo frontend) |
| `DATABASE_URL` | PostgreSQL o SQLite | Para persistencia de datos |
| `GOOGLE_API_KEY` | Tu API key | Gemini API |
| `META_APP_ID`, `META_APP_SECRET` | Credenciales Meta | Para Facebook/Instagram |

## Troubleshooting

### Frontend no se conecta al backend

**Problema:** Error `Connection refused` o `CORS error`

**Solución:**
1. Verificar que `BACKEND_URL` en frontend apunta a la URL correcta del backend
2. Verificar que backend tiene CORS habilitado (está en `main.py`)
3. Revisar logs en Railway: `railway logs`

### Dash no arranca

**Problema:** `Address already in use` o `Port 8050 not available`

**Solución:**
1. Railway asigna puerto automáticamente via `$PORT`
2. Verificar que `FRONTEND_PORT` usa `$PORT` en producción

### Base de datos no persiste

**Problema:** Datos desaparecen entre deploys

**Solución:**
1. Cambiar `ENV=cloud` en variables
2. Usar PostgreSQL en lugar de SQLite: `DATABASE_URL=postgresql://...`
3. Railway proporciona PostgreSQL integrado

## Verificación post-deploy

1. Acceder a `https://crm-politics-frontend.railway.app`
2. Verificar que carga el dashboard
3. Revisar logs: `railway logs`
4. Probar búsqueda de personas (debe conectar al backend)

## Rollback rápido

En Railway, puedes revertir a un deploy anterior desde el dashboard en 1 click.
