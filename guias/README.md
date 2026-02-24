# Agente Político - Sistema de Análisis de Conversaciones

Sistema inteligente basado en LangGraph y Python para analizar conversaciones de redes sociales (Facebook e Instagram), extraer información estructurada de ciudadanos y gestionar una base de datos de contactos políticos.

## 🎯 Características

### Backend
- **Agente LangGraph**: Análisis inteligente de conversaciones usando GPT-4
- **Extracción automática de datos**:
  - Información personal (nombre, edad, género)
  - Categorías de interés (Deportes, Inversión, Seguridad, Salud, Educación)
  - Datos de contacto (teléfono, email)
  - Ocupación y ubicación
  - Fecha de contacto
- **Base de datos SQLite** local con SQLAlchemy
- **API REST** con FastAPI
- **Integración con Meta APIs** (Facebook e Instagram)

### Frontend
- **Dashboard responsive** con Dash (Python)
- **Filtros avanzados**:
  - Por género
  - Rango de edad
  - Categorías de interés
  - Ubicación
- **Visualizaciones**:
  - Gráficos de distribución por género
  - Gráficos de intereses más comunes
  - Estadísticas en tiempo real
- **Exportación a CSV** de resultados filtrados
- **Adaptable a smartphones**

## 📋 Requisitos Previos

- Python 3.9+
- Cuenta de Google Cloud Platform (GCP)
- Service Account con permisos para Vertex AI / Gemini API
- Meta Developer Account (para Facebook/Instagram APIs)

## 🚀 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd agente-politico
```

### 2. Crear y activar entorno virtual

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Google Cloud Platform

**Importante:** Antes de continuar, necesitas configurar GCP y obtener tus credenciales.

👉 **Sigue la guía completa en [GCP_SETUP.md](GCP_SETUP.md)**

Resumen rápido:
1. Crea un proyecto en GCP
2. Habilita Vertex AI API
3. Crea una Service Account con rol "Vertex AI User"
4. Descarga el archivo JSON de credenciales
5. Configura las variables de entorno

### 5. Configurar variables de entorno

Copiar el archivo de ejemplo y editar con tus credenciales:

```bash
cp .env.example .env
```

Editar `.env` con tus credenciales de GCP:

```env
# Google Cloud Platform (requerido para el agente)
GCP_PROJECT_ID=tu-proyecto-gcp
GCP_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=C:/ruta/completa/agente-politico-key.json
GEMINI_MODEL=gemini-2.0-flash-exp

# Meta APIs (opcional, para integración con redes sociales)
META_APP_ID=tu_app_id
META_APP_SECRET=tu_app_secret
META_ACCESS_TOKEN=tu_access_token
INSTAGRAM_ACCESS_TOKEN=tu_instagram_token

# Base de datos (por defecto SQLite local)
DATABASE_URL=sqlite:///./agente_politico.db

# Configuración de servidores
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
FRONTEND_HOST=127.0.0.1
FRONTEND_PORT=8050

DEBUG=True
```

**🆓 Para activar el FREE TIER:**
👉 **[Guía rápida de 5 minutos: FREE_TIER_GUIA.md](FREE_TIER_GUIA.md)**

**🏢 Para configuración enterprise con Vertex AI:**
👉 [Ver GCP_SETUP.md](GCP_SETUP.md)

### 6. Inicializar la base de datos

La base de datos se inicializa automáticamente al iniciar el backend por primera vez.

---

## 🎭 ¿Quieres probar SIN configurar APIs de Meta?

**¡Sí es posible!** Usa el **Modo Demo** con datos simulados:

```bash
# Genera 10-20 personas con conversaciones realistas
python generate_dummy_data.py

# O usa el menú interactivo
python test_meta_api.py
# Selecciona opción 5: Modo Demo
```

Esto te permite probar **todas las funcionalidades** sin necesitar configurar Facebook o Instagram.

👉 **[Guía completa: MODO_DEMO.md](MODO_DEMO.md)**

---

## 🎮 Uso

### Iniciar el Backend (API)

```bash
python backend/main.py
```

El backend estará disponible en: `http://127.0.0.1:8000`

API docs (Swagger): `http://127.0.0.1:8000/docs`

### Iniciar el Frontend (Dashboard)

En otra terminal:

```bash
python frontend/app.py
```

El dashboard estará disponible en: `http://127.0.0.1:8050`

## 📚 Estructura del Proyecto

```
agente-politico/
├── agent/
│   └── langgraph_agent.py      # Agente LangGraph para análisis
├── backend/
│   └── main.py                  # API FastAPI
├── database/
│   ├── __init__.py              # Conexión a DB
│   ├── models.py                # Modelos SQLAlchemy
│   └── services.py              # Servicios de datos
├── frontend/
│   └── app.py                   # Dashboard Dash
├── integrations/
│   └── meta_api.py              # Cliente Meta API
├── exports/                      # Archivos CSV exportados
├── config.py                    # Configuración global
├── requirements.txt             # Dependencias
├── .env.example                 # Ejemplo de variables de entorno
└── README.md                    # Este archivo
```

## 🔧 Configuración de Meta APIs (Facebook e Instagram)

Para usar las integraciones con redes sociales, consulta:

👉 **[Guía completa de configuración de Meta APIs: META_API_SETUP.md](META_API_SETUP.md)**

**Resumen rápido:**
1. Crea una app en [Meta for Developers](https://developers.facebook.com/)
2. Conecta tu página de Facebook
3. Obtén los Access Tokens
4. Configúralos en tu archivo `.env`

**Script de prueba:**
```bash
python test_meta_api.py
```

---

## 🔧 Uso de la API

### Procesar un mensaje

```bash
POST /api/mensajes/procesar
Content-Type: application/json

{
  "mensaje": "Hola, me llamo Juan Pérez, tengo 28 años y me preocupa la seguridad en mi barrio",
  "plataforma": "facebook",
  "facebook_id": "123456789"
}
```

### Buscar personas

```bash
POST /api/personas/buscar
Content-Type: application/json

{
  "genero": "Masculino",
  "edad_min": 18,
  "edad_max": 30,
  "intereses": ["Salud", "Educación"]
}
```

### Exportar a CSV

```bash
POST /api/personas/exportar
Content-Type: application/json

{
  "genero": "Masculino",
  "edad_min": 18,
  "edad_max": 30,
  "intereses": ["Salud"]
}
```

Los archivos CSV se guardan en la carpeta `exports/`.

## 📊 Uso del Dashboard

1. **Filtrar personas**: Usa los selectores en la barra lateral para definir criterios de búsqueda
2. **Ver resultados**: La tabla muestra todas las personas que coinciden con los filtros
3. **Exportar CSV**: Haz clic en "Exportar CSV" para descargar los resultados filtrados
4. **Ver estadísticas**: Los gráficos se actualizan automáticamente cada 30 segundos

## 🔐 Configuración de Meta APIs

Para obtener tus credenciales de Meta:

1. Ve a [Meta for Developers](https://developers.facebook.com/)
2. Crea una nueva app
3. Añade los productos "Facebook Login" y "Instagram Basic Display"
4. Obtén tu Access Token desde el Graph API Explorer
5. Configura los permisos necesarios:
   - `pages_messaging`
   - `pages_read_engagement`
   - `instagram_basic`
   - `instagram_manage_messages`

**📖 Para instrucciones detalladas, consulta [META_API_SETUP.md](META_API_SETUP.md)**

**🧪 Probar tu configuración:**
```bash
python test_meta_api.py
```

---

## 🧪 Testing del Agente

Para probar el agente sin APIs reales, puedes usar el endpoint de procesamiento directamente:

```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/api/mensajes/procesar",
    json={
        "mensaje": "Me llamo María García, tengo 35 años y me interesa la salud pública",
        "plataforma": "test"
    }
)

print(response.json())
```

## 📱 Responsive Design

El dashboard está optimizado para:
- Desktop (>1200px)
- Tablets (768px - 1200px)
- Smartphones (<768px)

La barra lateral se adapta automáticamente en pantallas pequeñas.

## 🤝 Categorías de Interés

El sistema categoriza automáticamente los intereses en:
- **Deportes**
- **Inversión**
- **Seguridad**
- **Salud**
- **Educación**

Estas categorías pueden modificarse en `config.py`.

## � Deployment a Producción

### Deployment Rápido a Heroku

Para desplegar a producción en Heroku con dominio personalizado:

**Opción 1: Script automatizado (PowerShell en Windows)**
```powershell
.\deploy_heroku.ps1
```

**Opción 2: Script automatizado (Bash en Linux/Mac)**
```bash
chmod +x deploy_heroku.sh
./deploy_heroku.sh
```

Los scripts automatizan:
- ✅ Verificación de Heroku CLI
- ✅ Login y autenticación
- ✅ Creación de app (si no existe)
- ✅ Configuración de Git
- ✅ Commit de cambios pendientes
- ✅ Push a Heroku
- ✅ Instrucciones para dominio personalizado

### Guía Manual Completa

Para configuración paso a paso incluyendo variables de entorno, dominio personalizado, y DNS:

**Ver:** [GUIA_DEPLOYMENT_HEROKU.md](GUIA_DEPLOYMENT_HEROKU.md)

La guía incluye:
- 📦 Instalación de Heroku CLI
- ⚙️ Configuración de 21 variables de entorno
- 🌐 Setup de dominio personalizado (app.retarget.cl)
- 🔧 Configuración DNS (Cloudflare, GoDaddy, NIC Chile)
- 🔐 Actualización de OAuth URIs en Meta Dashboard
- 🛠️ Troubleshooting de errores comunes
- 📊 Monitoreo y logs
- 💰 Costos y planes

### Archivos de Deployment

- **Procfile**: Configuración del servidor web
- **runtime.txt**: Versión de Python (3.11.9)
- **requirements.txt**: Dependencias de Python

### Dominio Personalizado

Después del deployment inicial:

1. Agregar dominio a Heroku:
```bash
heroku domains:add app.retarget.cl -a crm-politico-app
```

2. Configurar CNAME en tu proveedor DNS:
```
Nombre: app
Tipo: CNAME
Valor: <DNS Target de Heroku>
```

3. Actualizar Meta Dashboard:
- App Domains: `app.retarget.cl`
- Valid OAuth Redirect URIs: `https://app.retarget.cl/auth/facebook/callback`

### PostgreSQL (Recomendado)

Heroku tiene filesystem efímero. Para persistencia de datos:

```bash
heroku addons:create heroku-postgresql:essential-0 -a crm-politico-app
```

Heroku configurará automáticamente `DATABASE_URL`.

## 📝 Notas Importantes

- La base de datos SQLite es local y se crea en el directorio raíz del proyecto
- **Producción**: Se recomienda usar PostgreSQL en Heroku (filesystem efímero)
- Los archivos CSV exportados se guardan en `exports/`
- El agente requiere una API key válida de Google Gemini
- Las integraciones con Meta requieren configuración adicional de permisos
- **Admin API**: Sistema de whitelist con endpoints REST para gestionar usuarios autorizados

## 🐛 Solución de Problemas

### Error: "Google credentials not found" o "Authentication failed"
- Verifica que el archivo `.env` existe
- Verifica que `GOOGLE_APPLICATION_CREDENTIALS` apunta al archivo JSON correcto
- Verifica que tu Service Account tiene permisos para Vertex AI
- Asegúrate de haber habilitado la API de Vertex AI en tu proyecto GCP

### Error: "Connection refused" al acceder al dashboard
- Asegúrate de que el backend está ejecutándose
- Verifica que los puertos 8000 y 8050 no están en uso

### La exportación CSV no funciona
- Verifica que la carpeta `exports/` tiene permisos de escritura
- Revisa los logs del backend para más detalles

## 📄 Licencia

Este proyecto es de código abierto para uso educativo y político.

## 👥 Contacto

Para preguntas o soporte, por favor abre un issue en el repositorio.

---

**¡Listo para usar!** 🎉

Inicia el backend y el frontend, y comienza a analizar conversaciones y gestionar tu base de datos de contactos políticos.
