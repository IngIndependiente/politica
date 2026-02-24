# 🚀 PASOS ESPECÍFICOS PARA RETARGET.CL

**Dominio:** retarget.cl ✅  
**Email en privacy policy:** ✅ Ya configurado  
**Fecha:** 5 de febrero de 2026

---

## ✅ LO QUE YA TIENES

- ✅ Dominio: retarget.cl
- ✅ Email real en privacy policy
- ✅ App funcionando en localhost
- ✅ Código listo para desplegar

---

## 🎯 LO QUE FALTA HACER (Orden prioritario)

### 1️⃣ **SUBIR PRIVACY POLICY A RETARGET.CL** ⚠️ URGENTE

Meta requiere: `https://retarget.cl/privacy-policy.html`

**Opciones para subir el archivo:**

#### Opción A: FTP/SFTP (5 minutos)
```bash
# Herramientas: FileZilla, WinSCP, CyberDuck

1. Conectar a retarget.cl por FTP/SFTP
   Host: retarget.cl (o IP de tu servidor)
   Usuario: [tu usuario]
   Contraseña: [tu contraseña]
   Puerto: 21 (FTP) o 22 (SFTP)

2. Navegar a carpeta pública:
   - public_html/
   - www/
   - htdocs/
   (depende de tu hosting)

3. Subir archivo: privacy-policy.html

4. Verificar en navegador:
   https://retarget.cl/privacy-policy.html
```

#### Opción B: Panel de Hosting (cPanel/Plesk)
```
1. Entrar a panel de tu hosting
2. File Manager o Administrador de archivos
3. Ir a carpeta raíz (public_html)
4. Botón "Upload" o "Subir"
5. Seleccionar privacy-policy.html
6. Esperar que se suba
7. Verificar: https://retarget.cl/privacy-policy.html
```

#### Opción C: Servir desde FastAPI
```python
# Agregar a backend/main.py

from fastapi.responses import FileResponse
import os

# Al inicio, después de crear app
@app.get("/privacy-policy.html", response_class=FileResponse)
async def privacy_policy():
    """Servir política de privacidad para Meta App Review."""
    policy_path = os.path.join(os.path.dirname(__file__), "..", "privacy-policy.html")
    return FileResponse(policy_path, media_type="text/html")

# También puedes servirlo como /privacy-policy (sin .html)
@app.get("/privacy-policy", response_class=FileResponse)
async def privacy_policy_alt():
    policy_path = os.path.join(os.path.dirname(__file__), "..", "privacy-policy.html")
    return FileResponse(policy_path, media_type="text/html")
```

Luego cuando despliegues el backend a retarget.cl, estará disponible automáticamente.

---

### 2️⃣ **GENERAR ÍCONO DE LA APP** (1-2 horas)

```bash
# Opción rápida: Script Python
pip install pillow
python generar_icono_app.py

# Genera:
# - app_icon_1024.png (subir a Meta Dashboard)
# - app_logo_200.png (logo alternativo)
# - app_icon_512.png (preview)
```

**O usa IA:**
- DALL-E 3: https://chat.openai.com/
- Leonardo AI: https://leonardo.ai/ (gratis)
- Bing Creator: https://www.bing.com/create

**Prompt sugerido:**
```
"Professional app icon for political CRM, 1024x1024px, 
flat design, blue and green colors, chat bubble with star symbol,
transparent background, modern style"
```

---

### 3️⃣ **CONFIGURAR HTTPS EN RETARGET.CL**

Meta requiere HTTPS (candado verde). Opciones:

#### Si tu hosting ya tiene SSL/TLS:
```
✅ Verifica: https://retarget.cl debería funcionar
✅ Si funciona, estás listo
```

#### Si NO tienes SSL:
```bash
# Opción 1: Let's Encrypt (gratis)
# Si tienes acceso SSH al servidor:
sudo certbot --nginx -d retarget.cl -d www.retarget.cl

# Opción 2: Panel de hosting
# La mayoría de hostings modernos (cPanel, Plesk) tienen botón "SSL/TLS"
# Click → "Let's Encrypt" → "Instalar"

# Opción 3: Cloudflare (gratis)
# 1. Crear cuenta en cloudflare.com
# 2. Agregar retarget.cl como sitio
# 3. Cambiar nameservers en tu registrador de dominio
# 4. Esperar 24h → HTTPS automático
```

---

### 4️⃣ **DESPLEGAR BACKEND A RETARGET.CL**

Tu backend debe correr en `https://retarget.cl` (puerto 443/HTTPS).

#### Opción A: Servidor propio (VPS, DigitalOcean, AWS)
```bash
# 1. Conectar por SSH
ssh usuario@retarget.cl

# 2. Clonar código o subir por SFTP
git clone [tu_repo] /var/www/crm-politico
# O subir con FileZilla/WinSCP

# 3. Instalar dependencias
cd /var/www/crm-politico
pip install -r requirements.txt

# 4. Actualizar .env
nano .env
# Cambiar:
# OAUTH_REDIRECT_URI=https://retarget.cl/auth/facebook/callback

# 5. Configurar systemd para mantener backend corriendo
sudo nano /etc/systemd/system/crm-politico-backend.service

# Contenido del archivo:
[Unit]
Description=CRM Político Backend
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/crm-politico
ExecStart=/usr/bin/python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target

# 6. Iniciar servicio
sudo systemctl enable crm-politico-backend
sudo systemctl start crm-politico-backend

# 7. Configurar Nginx como reverse proxy
sudo nano /etc/nginx/sites-available/retarget.cl

# Contenido:
server {
    listen 80;
    server_name retarget.cl www.retarget.cl;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name retarget.cl www.retarget.cl;
    
    ssl_certificate /etc/letsencrypt/live/retarget.cl/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/retarget.cl/privkey.pem;
    
    location / {
        proxy_pass http://127.0.0.1:8050;  # Frontend Dash
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api/ {
        proxy_pass http://127.0.0.1:8000;  # Backend FastAPI
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /auth/ {
        proxy_pass http://127.0.0.1:8000;  # OAuth callbacks
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# 8. Activar sitio
sudo ln -s /etc/nginx/sites-available/retarget.cl /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### Opción B: Plataforma como servicio (más fácil)
```bash
# Heroku (gratis para empezar)
heroku create crm-politico-retarget
git push heroku main
heroku domains:add retarget.cl
# Luego en tu registrador de dominio (donde compraste retarget.cl):
# Agregar CNAME: retarget.cl → [tu-app].herokuapp.com

# Railway (https://railway.app)
# Similar a Heroku, con UI más moderna
# Connect GitHub → Deploy → Add custom domain → retarget.cl
```

---

### 5️⃣ **DESPLEGAR FRONTEND A RETARGET.CL**

El frontend Dash debe servirse en `https://retarget.cl`

```bash
# Actualizar frontend/config.py
BACKEND_URL = "https://retarget.cl"  # Cambiar de localhost

# Si usas systemd (servidor propio)
sudo nano /etc/systemd/system/crm-politico-frontend.service

[Unit]
Description=CRM Político Frontend
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/crm-politico
ExecStart=/usr/bin/python3 frontend/app.py
Restart=always

[Install]
WantedBy=multi-user.target

sudo systemctl enable crm-politico-frontend
sudo systemctl start crm-politico-frontend
```

---

### 6️⃣ **TOMAR SCREENSHOTS CON DATOS DUMMY**

```bash
# 1. Generar datos de prueba
python generate_dummy_data.py

# 2. Iniciar app en localhost (para screenshots)
python launcher.py

# 3. Tomar 6 screenshots:
#    Screenshot 1: Login + OAuth
#    Screenshot 2: Modal de selección de páginas
#    Screenshot 3: Dashboard con candidatos
#    Screenshot 4: Sincronización de mensajes
#    Screenshot 5: Tabla de conversaciones (FB + IG)
#    Screenshot 6: Análisis de IA

# Herramienta: Windows Snipping Tool (Win+Shift+S)
# Guardar en: screenshots/ o assets/screenshots/
```

---

### 7️⃣ **GRABAR VIDEO DE DEMOSTRACIÓN** (3-4 minutos)

```bash
# Seguir guión detallado:
# GUION_VIDEO_DEMO.txt (500+ líneas)

# Herramientas:
# - OBS Studio (gratis): https://obsproject.com/
# - Loom (fácil): https://loom.com/

# Configuración:
# - Resolución: 1920x1080
# - Frame rate: 30 fps
# - Formato: MP4
# - Duración: 3-4 minutos
# - Narración en español o inglés
```

---

### 8️⃣ **CONFIGURAR META DASHBOARD**

```
URL: https://developers.facebook.com/apps/1249817260324336

┌─────────────────────────────────────────────────┐
│ SETTINGS > BASIC                                │
├─────────────────────────────────────────────────┤
│ App Name: CRM Político Multi-Tenant            │
│ Category: Business                              │
│ Contact Email: [email de tu cliente] ✅         │
│ Privacy Policy URL: https://retarget.cl/privacy-policy.html │
│ App Icon: [subir app_icon_1024.png]            │
│ App Domains: retarget.cl                        │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ PRODUCTS > FACEBOOK LOGIN > SETTINGS            │
├─────────────────────────────────────────────────┤
│ Valid OAuth Redirect URIs:                      │
│   https://retarget.cl/auth/facebook/callback    │
│                                                  │
│ Client OAuth Login: ON ✓                        │
│ Web OAuth Login: ON ✓                           │
└─────────────────────────────────────────────────┘
```

---

### 9️⃣ **ENVIAR A APP REVIEW**

```
1. Ir a: APP REVIEW > PERMISSIONS AND FEATURES

2. Para CADA permiso, click "Request":
   • business_management
   • pages_show_list
   • pages_messaging
   • pages_read_engagement
   • instagram_basic
   • instagram_manage_messages

3. Completar formulario (usar RESPUESTAS_META_APP_REVIEW.txt)

4. Subir screenshots (6 imágenes)

5. Subir video (MP4, <100 MB)

6. Click "Submit for Review"

7. ⏳ Esperar 3-7 días hábiles
```

---

## 📋 CHECKLIST RÁPIDO PARA RETARGET.CL

```
☐ Subir privacy-policy.html a https://retarget.cl/privacy-policy.html
☐ Verificar que HTTPS funciona (candado verde)
☐ Generar ícono 1024x1024 (python generar_icono_app.py)
☐ Desplegar backend a retarget.cl
☐ Desplegar frontend a retarget.cl
☐ Actualizar .env con OAUTH_REDIRECT_URI de producción
☐ Probar OAuth en producción (https://retarget.cl)
☐ Generar datos dummy (python generate_dummy_data.py)
☐ Tomar 6 screenshots
☐ Grabar video de 3-4 minutos
☐ Configurar Meta Dashboard:
   ☐ App Domains: retarget.cl
   ☐ Privacy Policy URL: https://retarget.cl/privacy-policy.html
   ☐ OAuth Redirect: https://retarget.cl/auth/facebook/callback
☐ Subir ícono a Meta Dashboard
   ☐ Solicitar 8 permisos con screenshots + video
☐ Enviar a review
☐ ⏳ Esperar 3-7 días
☐ ✅ ¡Aprobado! 🎉
```

---

## ⏱️ TIMELINE ESTIMADO PARA RETARGET.CL

| Tarea | Tiempo | Estado |
|-------|--------|--------|
| Subir privacy policy | 5 min | ⬜ Pendiente |
| Generar ícono | 1-2 h | ⬜ Pendiente |
| Desplegar backend | 2-4 h | ⬜ Pendiente |
| Desplegar frontend | 1-2 h | ⬜ Pendiente |
| Testing en producción | 1 h | ⬜ Pendiente |
| Screenshots | 1-2 h | ⬜ Pendiente |
| Video | 2-3 h | ⬜ Pendiente |
| Configurar Meta | 1 h | ⬜ Pendiente |
| Completar formulario | 2 h | ⬜ Pendiente |
| **TOTAL PREPARACIÓN** | **1-2 días** | |
| **REVIEW DE META** | **3-7 días** | |
| **TOTAL** | **4-9 días** | |

---

## 🚨 PROBLEMAS COMUNES Y SOLUCIONES

### Problema 1: "privacy-policy.html da 404"
```bash
# Verificar que el archivo está en la carpeta correcta
# Si usas Nginx, debe estar en:
/var/www/html/privacy-policy.html

# O configurar location en Nginx:
location /privacy-policy.html {
    alias /ruta/completa/privacy-policy.html;
}
```

### Problema 2: "Meta dice que privacy policy no es accesible"
```bash
# 1. Verificar en navegador privado/incógnito
https://retarget.cl/privacy-policy.html

# 2. Verificar headers HTTP
curl -I https://retarget.cl/privacy-policy.html

# Debe retornar:
# HTTP/2 200 
# Content-Type: text/html

# Si retorna 404, verifica ruta del archivo
# Si retorna redirect, Meta lo rechaza
```

### Problema 3: "OAuth redirect no funciona"
```bash
# 1. Verificar que backend está corriendo
curl https://retarget.cl/docs

# 2. Verificar endpoint callback
curl https://retarget.cl/auth/facebook/callback

# 3. Verificar en Meta Dashboard que la URL coincide EXACTAMENTE
# (sin / al final)
```

---

## 📞 RECURSOS PARA RETARGET.CL

**Hosting Chile (si necesitas):**
- DigitalOcean Chile (datacenter en Brasil): https://digitalocean.com
- Vultr Chile: https://vultr.com
- AWS Chile (Santiago): https://aws.amazon.com

**SSL/TLS Gratis:**
- Let's Encrypt: https://letsencrypt.org/
- Cloudflare: https://cloudflare.com

**Meta Dashboard:**
- Tu app: https://developers.facebook.com/apps/1249817260324336
- Docs: https://developers.facebook.com/docs/app-review

---

## 🎯 PRÓXIMO PASO INMEDIATO

```
╔════════════════════════════════════════════════╗
║  🚀 ACCIÓN AHORA:                             ║
║                                                ║
║  1. Subir privacy-policy.html a retarget.cl   ║
║     → FTP, cPanel, o FastAPI                  ║
║                                                ║
║  2. Verificar:                                 ║
║     https://retarget.cl/privacy-policy.html   ║
║     (debe abrir sin login)                     ║
║                                                ║
║  3. Generar ícono:                             ║
║     python generar_icono_app.py               ║
║                                                ║
║  ⏱️ Con retarget.cl ya tienes ventaja:        ║
║     Estás a solo 4-9 días de aprobación 🎉    ║
╚════════════════════════════════════════════════╝
```

---

**¿Dudas técnicas sobre despliegue en retarget.cl?**
- Pregúntame sobre configuración específica de tu servidor
- Puedo ayudarte con Nginx, systemd, o cualquier parte técnica

**¡ESTÁS MUY CERCA! 🚀**
