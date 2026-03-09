# Migración SQLite → PostgreSQL

## 📋 Objetivo
Migrar la base de datos de SQLite a PostgreSQL para despliegue en Railway, **preservando todos los datos acumulados**.

## 🔄 Proceso de Migración

### Paso 1: Preparar el entorno local
```bash
cd /Users/spam11/Desktop/CRM-politics

# Instalar dependencias (si no las tienes)
pip install -r requirements.txt

# Verificar que tienes SQLite con datos
ls -lh agente_politico.db
```

### Paso 2: Crear base de datos PostgreSQL local (para testing)
```bash
# Opción A: Usando Docker (recomendado)
docker run --name postgres_crm -e POSTGRES_PASSWORD=password -e POSTGRES_DB=crm_politica -p 5432:5432 -d postgres:15

# Opción B: PostgreSQL instalado localmente
createdb crm_politica
```

### Paso 3: Ejecutar migración local
```bash
python migrate_sqlite_to_postgres.py \
  --source sqlite:///./agente_politico.db \
  --target postgresql://postgres:password@localhost:5432/crm_politica
```

**Salida esperada:**
```
✅ Conectado a SQLite
✅ Conectado a PostgreSQL
✅ Esquema creado en PostgreSQL
🚀 Iniciando migración de datos...

Migrando tabla: usuarios_autorizados
  → 5 filas encontradas
  ✅ 5 filas migradas
...
✅ Verificación exitosa

============================================================
📊 RESUMEN DE MIGRACIÓN
============================================================
Tablas migradas: 9
Filas migradas: 1,234
Errores: 0
Tiempo total: 12.45s
============================================================

✅ Migración completada exitosamente
```

### Paso 4: Verificar datos en PostgreSQL
```bash
# Conectar a PostgreSQL
psql postgresql://postgres:password@localhost:5432/crm_politica

# Verificar tablas
\dt

# Contar filas en tabla principal
SELECT COUNT(*) FROM personas;
SELECT COUNT(*) FROM conversaciones;
SELECT COUNT(*) FROM candidatos;
```

## 🚀 Despliegue en Railway

### Paso 1: Agregar PostgreSQL a Railway
1. Ve a tu proyecto en Railway: https://railway.app/dashboard
2. Click en **"+ New"** → **"Database"** → **"PostgreSQL"**
3. Railway auto-configura `DATABASE_URL` en variables de entorno

### Paso 2: Actualizar variables de entorno en Railway
```
ENV=cloud
DEBUG=False

# Servidor
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# Google Gemini (opcional)
GOOGLE_API_KEY=tu_api_key

# Meta/Facebook
META_APP_ID=tu_app_id
META_APP_SECRET=tu_app_secret
META_ACCESS_TOKEN=tu_token
META_VERIFY_TOKEN=agente_politico_token_secreto

# OAuth
OAUTH_REDIRECT_URI=https://tu-dominio-railway.app/auth/facebook/callback

# Admin
ADMIN_TOKEN=genera_un_token_seguro
SYNC_PASSWORD=CRMpoliticos2026!

# DATABASE_URL: Auto-configurada por Railway PostgreSQL plugin
```

### Paso 3: Migrar datos a Railway PostgreSQL
```bash
# Obtener DATABASE_URL de Railway
# Ve a tu proyecto → Variables → DATABASE_URL (copiar)

# Ejecutar migración
python migrate_sqlite_to_postgres.py \
  --source sqlite:///./agente_politico.db \
  --target "postgresql://user:pass@host:5432/railway"
```

### Paso 4: Desplegar en Railway
```bash
git add .
git commit -m "Migrate to PostgreSQL"
git push origin main
```

Railway detectará los cambios y redesplegará automáticamente.

## ✅ Verificación Post-Despliegue

### 1. Verificar que la API responde
```bash
curl https://tu-dominio-railway.app/
```

**Respuesta esperada:**
```json
{
  "message": "Agente Político API",
  "version": "1.0.1",
  "endpoints": {...}
}
```

### 2. Verificar que los datos están en PostgreSQL
```bash
# Desde Railway Dashboard → PostgreSQL → Connect
# O usar psql si tienes acceso remoto

SELECT COUNT(*) as total_personas FROM personas;
SELECT COUNT(*) as total_conversaciones FROM conversaciones;
```

### 3. Probar endpoints
```bash
# Listar candidatos
curl https://tu-dominio-railway.app/api/candidatos

# Listar personas
curl https://tu-dominio-railway.app/api/personas
```

## 🔧 Troubleshooting

### Error: "DATABASE_URL no configurada"
**Causa:** Railway PostgreSQL plugin no está habilitado o DATABASE_URL no está en variables.

**Solución:**
1. Ve a Railway Dashboard → Tu proyecto → PostgreSQL
2. Verifica que el plugin esté conectado
3. Copia `DATABASE_URL` de Variables
4. Pégalo en tu `.env` local para testing

### Error: "psycopg2 not found"
**Causa:** psycopg2-binary no está instalado.

**Solución:**
```bash
pip install psycopg2-binary>=2.9.9
```

### Error: "relation 'personas' does not exist"
**Causa:** Esquema no se creó o migración falló.

**Solución:**
```bash
# Verificar tablas en PostgreSQL
psql $DATABASE_URL -c "\dt"

# Si no hay tablas, re-ejecutar migración
python migrate_sqlite_to_postgres.py --source sqlite:///./agente_politico.db --target $DATABASE_URL
```

### Error: "Duplicate key value violates unique constraint"
**Causa:** Datos duplicados o IDs conflictivos.

**Solución:**
```bash
# Limpiar PostgreSQL y re-migrar
psql $DATABASE_URL -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
python migrate_sqlite_to_postgres.py --source sqlite:///./agente_politico.db --target $DATABASE_URL
```

## 📊 Comparación SQLite vs PostgreSQL

| Aspecto | SQLite | PostgreSQL |
|---------|--------|-----------|
| **Archivo** | `agente_politico.db` | Servidor remoto |
| **Escalabilidad** | Limitada (~100MB) | Ilimitada |
| **Concurrencia** | Baja | Alta |
| **Backups** | Manual | Automático (Railway) |
| **Costo** | Gratis | Gratis en Railway (hasta límite) |
| **Producción** | ❌ No recomendado | ✅ Recomendado |

## 🔐 Seguridad

### Antes de desplegar:
1. ✅ Cambiar `ADMIN_TOKEN` a un valor seguro
2. ✅ Cambiar `SYNC_PASSWORD` a un valor seguro
3. ✅ Habilitar HTTPS en Railway
4. ✅ Configurar firewall de PostgreSQL
5. ✅ Hacer backup de SQLite antes de migrar

### Backup de SQLite
```bash
# Crear backup antes de migrar
cp agente_politico.db agente_politico.db.backup.$(date +%Y%m%d_%H%M%S)

# Listar backups
ls -lh agente_politico.db*
```

## 📝 Checklist de Migración

- [ ] Instalar psycopg2-binary
- [ ] Crear PostgreSQL local para testing
- [ ] Ejecutar migración local
- [ ] Verificar datos en PostgreSQL local
- [ ] Agregar PostgreSQL a Railway
- [ ] Configurar DATABASE_URL en Railway
- [ ] Migrar datos a Railway PostgreSQL
- [ ] Desplegar en Railway
- [ ] Verificar API responde
- [ ] Verificar datos en PostgreSQL remoto
- [ ] Probar endpoints principales
- [ ] Hacer backup de SQLite

## 🆘 Soporte

Si encuentras problemas:
1. Revisa los logs de Railway: Dashboard → Logs
2. Verifica DATABASE_URL: `echo $DATABASE_URL`
3. Prueba conexión: `psql $DATABASE_URL -c "SELECT 1"`
4. Re-ejecuta migración con `--verify-only` para diagnosticar
