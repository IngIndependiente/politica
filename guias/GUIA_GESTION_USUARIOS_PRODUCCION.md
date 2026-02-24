# 🔐 GUÍA: Gestionar Usuarios en Producción

Una vez tu app esté desplegada en Heroku o Railway, tienes **3 formas** de agregar/gestionar usuarios autorizados.

---

## 🎯 OPCIÓN 1: Heroku/Railway CLI (Más Rápido)

### **Heroku:**

```powershell
# Acceder a terminal de tu app
heroku run bash -a crm-politico-prod

# Ejecutar script interactivo
python agregar_usuario_autorizado.py
```

**Comando directo (sin menú):**
```powershell
heroku run python agregar_usuario_autorizado.py "email@example.com" "Nombre" "candidato" -a crm-politico-prod
```

**Listar usuarios actuales:**
```powershell
heroku run python -c "
from backend.database import SessionLocal
from database.models import UsuarioAutorizado

db = SessionLocal()
usuarios = db.query(UsuarioAutorizado).all()
for u in usuarios:
    print(f'{u.id} - {u.email} - {u.nombre} - {'Activo' if u.activo == 1 else 'Inactivo'}')
db.close()
" -a crm-politico-prod
```

### **Railway:**

```powershell
# Instalar CLI si no lo tienes
npm i -g @railway/cli

# Login
railway login

# Conectar al proyecto
railway link

# Ejecutar script
railway run python agregar_usuario_autorizado.py
```

---

## 🌐 OPCIÓN 2: API REST (Recomendado para Uso Frecuente)

Agrega endpoints a tu backend para gestionar usuarios desde el navegador o Postman.

### **Paso 1: Agregar código a backend/main.py**

Copia el contenido de [admin_usuarios_endpoint.py](admin_usuarios_endpoint.py) al final de tu [backend/main.py](backend/main.py):

```python
# Agregar al final de backend/main.py

# Token de autenticación
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "cambiar-este-token-en-produccion")

def verificar_admin_token(authorization: str = Header(None)):
    """Middleware para verificar token de administrador."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Token requerido")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Formato inválido")
    
    token = authorization.replace("Bearer ", "")
    
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Token inválido")
    
    return True

# Endpoints de administración
@app.get("/admin/usuarios", tags=["Admin"])
async def listar_usuarios(
    db: Session = Depends(get_db),
    _: bool = Depends(verificar_admin_token)
):
    """Lista todos los usuarios autorizados."""
    from database.models import UsuarioAutorizado
    usuarios = db.query(UsuarioAutorizado).all()
    return [
        {
            "id": u.id,
            "email": u.email,
            "nombre": u.nombre,
            "rol": u.rol,
            "activo": u.activo,
            "fecha_registro": u.fecha_registro,
            "ultimo_acceso": u.ultimo_acceso
        }
        for u in usuarios
    ]

@app.post("/admin/usuarios", tags=["Admin"])
async def crear_usuario(
    email: str,
    nombre: str,
    rol: str = "candidato",
    db: Session = Depends(get_db),
    _: bool = Depends(verificar_admin_token)
):
    """Crea nuevo usuario autorizado."""
    from database.models import UsuarioAutorizado
    
    existe = db.query(UsuarioAutorizado).filter(
        UsuarioAutorizado.email == email
    ).first()
    
    if existe:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    
    nuevo = UsuarioAutorizado(
        email=email,
        nombre=nombre,
        rol=rol,
        activo=1
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    
    return {"mensaje": "Usuario creado", "id": nuevo.id, "email": nuevo.email}

@app.patch("/admin/usuarios/{usuario_id}", tags=["Admin"])
async def actualizar_usuario(
    usuario_id: int,
    activo: int = None,
    rol: str = None,
    db: Session = Depends(get_db),
    _: bool = Depends(verificar_admin_token)
):
    """Actualiza usuario (activar/desactivar, cambiar rol)."""
    from database.models import UsuarioAutorizado
    
    usuario = db.query(UsuarioAutorizado).filter(
        UsuarioAutorizado.id == usuario_id
    ).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if activo is not None:
        usuario.activo = activo
    if rol is not None:
        usuario.rol = rol
    
    db.commit()
    
    return {"mensaje": "Usuario actualizado", "email": usuario.email}
```

### **Paso 2: Generar Token de Administrador**

```powershell
# Generar token seguro
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Output ejemplo: KzY3mR_xN9pQ2tV8wL5jH4cBfG1aD7sO6uE0iM3vA9k

# Configurar en Heroku
heroku config:set ADMIN_TOKEN=KzY3mR_xN9pQ2tV8wL5jH4cBfG1aD7sO6uE0iM3vA9k -a crm-politico-prod
```

### **Paso 3: Usar la API**

#### Con **curl:**

```bash
# Listar usuarios
curl -X GET https://app.retarget.cl/admin/usuarios \
  -H "Authorization: Bearer KzY3mR_xN9pQ2tV8wL5jH4cBfG1aD7sO6uE0iM3vA9k"

# Crear usuario
curl -X POST "https://app.retarget.cl/admin/usuarios?email=nuevo@example.com&nombre=Juan%20Perez&rol=candidato" \
  -H "Authorization: Bearer KzY3mR_xN9pQ2tV8wL5jH4cBfG1aD7sO6uE0iM3vA9k"

# Desactivar usuario (ID 5)
curl -X PATCH "https://app.retarget.cl/admin/usuarios/5?activo=0" \
  -H "Authorization: Bearer KzY3mR_xN9pQ2tV8wL5jH4cBfG1aD7sO6uE0iM3vA9k"

# Reactivar usuario
curl -X PATCH "https://app.retarget.cl/admin/usuarios/5?activo=1" \
  -H "Authorization: Bearer KzY3mR_xN9pQ2tV8wL5jH4cBfG1aD7sO6uE0iM3vA9k"
```

#### Con **Postman:**

1. Nueva request → **GET** `https://app.retarget.cl/admin/usuarios`
2. Headers:
   - `Authorization: Bearer KzY3mR_xN9pQ2tV8wL5jH4cBfG1aD7sO6uE0iM3vA9k`
3. Send

#### Con **Python:**

```python
import requests

BASE_URL = "https://app.retarget.cl"
TOKEN = "KzY3mR_xN9pQ2tV8wL5jH4cBfG1aD7sO6uE0iM3vA9k"

headers = {"Authorization": f"Bearer {TOKEN}"}

# Listar usuarios
response = requests.get(f"{BASE_URL}/admin/usuarios", headers=headers)
print(response.json())

# Crear usuario
params = {
    "email": "candidato@example.com",
    "nombre": "Juan Pérez",
    "rol": "candidato"
}
response = requests.post(f"{BASE_URL}/admin/usuarios", headers=headers, params=params)
print(response.json())
```

#### **En el navegador (FastAPI docs):**

1. Ve a: `https://app.retarget.cl/docs`
2. Busca sección "Admin"
3. Click en "Authorize" 🔓
4. Ingresa: `Bearer KzY3mR_xN9pQ2tV8wL5jH4cBfG1aD7sO6uE0iM3vA9k`
5. Usa los endpoints desde la interfaz

---

## 🗄️ OPCIÓN 3: Acceso Directo a Base de Datos (Avanzado)

### **Heroku Postgres:**

Si usas PostgreSQL en lugar de SQLite:

```powershell
# Acceder a psql
heroku pg:psql -a crm-politico-prod

# Listar usuarios
SELECT * FROM usuarios_autorizados;

# Agregar usuario
INSERT INTO usuarios_autorizados (email, nombre, rol, activo, fecha_registro)
VALUES ('nuevo@example.com', 'Nuevo Usuario', 'candidato', 1, NOW());

# Desactivar usuario
UPDATE usuarios_autorizados SET activo = 0 WHERE email = 'usuario@example.com';

# Salir
\q
```

### **SQLite (menos común en producción):**

```powershell
# Descargar base de datos
heroku run cat data/agente_politico.db > local_backup.db -a crm-politico-prod

# Abrir con SQLite localmente
sqlite3 local_backup.db

# Agregar usuario
INSERT INTO usuarios_autorizados (email, nombre, rol, activo, fecha_registro)
VALUES ('nuevo@example.com', 'Nuevo', 'candidato', 1, datetime('now'));

# Subir de vuelta (no recomendado en producción activa)
```

---

## 📊 COMPARACIÓN DE OPCIONES

| Opción | Velocidad | Facilidad | Seguridad | Mejor para |
|--------|-----------|-----------|-----------|-----------|
| **CLI** | ⭐⭐⭐⭐⭐ Rápida | ⭐⭐⭐⭐ Fácil | ⭐⭐⭐⭐⭐ Alta | Administradores técnicos |
| **API REST** | ⭐⭐⭐ Media | ⭐⭐⭐⭐⭐ Muy fácil | ⭐⭐⭐⭐ Alta (con token) | Uso frecuente / No técnicos |
| **Acceso DB** | ⭐⭐ Lenta | ⭐⭐ Compleja | ⭐⭐⭐ Media | Emergencias / Migraciones |

---

## 🎯 RECOMENDACIÓN

### **Durante desarrollo/primeros usuarios:**
✅ Usa **OPCIÓN 1 (CLI)** - Es rápida y directa

### **Para uso continuo:**
✅ Implementa **OPCIÓN 2 (API REST)** - Más cómoda y escalable

### **Workflow ideal:**

1. **Primera vez:** CLI para agregar tus primeros 2-3 usuarios
2. **Después:** API REST para gestión continua
3. **Emergencias:** CLI como backup

---

## ✅ CHECKLIST POST-DEPLOYMENT

### Inmediatamente después de desplegar:

```powershell
# 1. Agregar tu email como primer admin
heroku run python agregar_usuario_autorizado.py \
  "tu-email@example.com" "Tu Nombre" "admin" \
  -a crm-politico-prod

# 2. Verificar que funciona
heroku run python test_control_acceso.py "tu-email@example.com" \
  -a crm-politico-prod

# 3. Agregar candidatos iniciales
heroku run python agregar_usuario_autorizado.py \
  "candidato1@example.com" "Candidato 1" "candidato" \
  -a crm-politico-prod

# 4. (Opcional) Si implementaste API, generar token
python -c "import secrets; print(secrets.token_urlsafe(32))"
heroku config:set ADMIN_TOKEN=<token-generado> -a crm-politico-prod
```

---

## 🔒 SEGURIDAD

### **Protección del token API:**

```bash
# ❌ NUNCA hagas esto:
# - Subir token a GitHub
# - Compartir token por email/chat sin encriptar
# - Usar token débil como "admin123"

# ✅ SIEMPRE:
# - Usar secretos generados aleatoriamente (32+ caracteres)
# - Guardar en variables de entorno
# - Rotar tokens cada 3-6 meses
# - Usar HTTPS siempre
```

### **Regenerar token:**

```powershell
# Generar nuevo
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Actualizar en Heroku
heroku config:set ADMIN_TOKEN=<nuevo-token> -a crm-politico-prod
```

---

## 📞 TROUBLESHOOTING

### **Error: "Token inválido"**
```powershell
# Verificar token configurado
heroku config:get ADMIN_TOKEN -a crm-politico-prod

# Actualizar si es necesario
heroku config:set ADMIN_TOKEN=nuevo-token -a crm-politico-prod
```

### **Error: "Usuario ya existe"**
```powershell
# Listar usuarios
heroku run python -c "
from backend.database import SessionLocal
from database.models import UsuarioAutorizado
db = SessionLocal()
for u in db.query(UsuarioAutorizado).all():
    print(f'{u.email} - {u.nombre}')
" -a crm-politico-prod
```

### **Error: "No module named 'database'"**
```powershell
# Verificar que el código esté desplegado
heroku run ls -la -a crm-politico-prod

# Re-desplegar si es necesario
git push heroku main
```

---

## 🚀 RESUMEN RÁPIDO

**Para agregar usuario en producción:**

```powershell
# Opción 1: CLI (más rápida)
heroku run python agregar_usuario_autorizado.py "email" "nombre" "rol" -a <app-name>

# Opción 2: API (más cómoda)
curl -X POST "https://app.retarget.cl/admin/usuarios?email=x&nombre=y&rol=z" \
  -H "Authorization: Bearer <token>"
```

**¡Listo para producción! 🎉**
