# Variables de Entorno para Railway

## 🔴 CRÍTICAS (sin estas el deploy falla)

Estas variables DEBEN estar configuradas para que el backend funcione:

```
GOOGLE_API_KEY=AIzaSyAOgeoO_qFHjRs6Eo3Jkl3Vn_DssPu60A4
ENV=cloud
DEBUG=False
```

## 📋 Pasos para configurar en Railway

1. **Ve a tu proyecto en Railway:**
   - https://railway.app/dashboard
   - Selecciona el proyecto "worthy-upliftment"
   - Click en "Variables" (en el panel izquierdo)

2. **Agrega las variables CRÍTICAS:**
   - Click en "New Variable"
   - Nombre: `GOOGLE_API_KEY`
   - Valor: `AIzaSyAOgeoO_qFHjRs6Eo3Jkl3Vn_DssPu60A4`
   - Click "Add"

   - Nombre: `ENV`
   - Valor: `cloud`
   - Click "Add"

   - Nombre: `DEBUG`
   - Valor: `False`
   - Click "Add"

3. **Redeploy:**
   - Ve a "Deployments"
   - Click en el último deploy (el que falló)
   - Click en "Redeploy"
   - Espera a que termine

## ✅ Variables Recomendadas (opcional pero útil)

Si quieres que funcionen todas las integraciones:

```
META_APP_ID=1249817260324336
META_APP_SECRET=b58b0b0f7a725044064d8433ed2e030d
META_ACCESS_TOKEN=EAARws8HV9fABQnobP8epqLAxPDAUqMmZC0k40LRuYKuppHXyPzXi872le2fOE6ixOK48VUfbjmyFKTKTlddHRDShoA8FRjQK57ZCyuEqZA0NU3iZBKD9DjbM5YCGg7lvaKGOdUVZCPMDErBIXV24ZB7EmIIusK4Oan1mkEtYIadbKdcV233SFSZAR5wBhfx0rpmHKgfgTs44gZDZD
META_VERIFY_TOKEN=agente_politico_token_secreto
WHATSAPP_PHONE_NUMBER_ID=1020214704502248
WHATSAPP_BUSINESS_ACCOUNT_ID=883009121149060
WHATSAPP_VERIFY_TOKEN=whatsapp_verify_token_secreto
ADMIN_TOKEN=yOZPAYY6ZzflXcAbFFq1D34Kw5AXzpN2xf7f6cHVo8k
SYNC_PASSWORD=CRMpoliticos2026!
OAUTH_REDIRECT_URI=https://web-production-d7b6.up.railway.app/auth/facebook/callback
```

## 🔍 Verificación post-deploy

Después de configurar las variables y redeploy:

1. Espera a que el deploy termine (5-10 minutos)
2. Ve a "Logs" para verificar que no hay errores
3. Accede a la URL pública: `https://web-production-d7b6.up.railway.app`
4. Deberías ver la API de FastAPI funcionando

## ❌ Si sigue fallando

Revisa los logs en Railway:
- Ve a "Logs" en tu proyecto
- Busca mensajes de error
- Comparte los logs aquí para debuggear

## 📝 Notas

- `GOOGLE_API_KEY` es la API key de Google AI Studio (gratis)
- Las credenciales de Meta/WhatsApp son opcionales si no usas esas integraciones
- `ENV=cloud` activa el modo producción
- `DEBUG=False` desactiva el debug mode (necesario en producción)
