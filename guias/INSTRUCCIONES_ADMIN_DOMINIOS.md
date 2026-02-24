# 📧 INSTRUCCIONES PARA EL ADMINISTRADOR DEL SERVIDOR

**Para:** Administrador de hosting de retarget.cl  
**De:** Ricardo (Desarrollador CRM Político)  
**Asunto:** Configuración de 2 subdominios para App Review de Meta

---

## 🎯 OBJETIVO

Necesito configurar **1 subdominio** en retarget.cl para desplegar mi aplicación CRM:

- **`app.retarget.cl`** - Para producción con usuarios reales y datos reales (según requisitos de Meta para App Review)

El subdominio debe apuntar al hosting local donde se ejecutará la aplicación Python con HTTPS.

---

## 📋 TAREAS NECESARIAS

### ✅ TAREA 1: Garantizar Acceso a Política de Privacidad

**Ubicación destino:** 
```
https://retarget.cl/privacy-policy.html
```

**Requisito:** El archivo `privacy-policy.html` debe estar accesible en el dominio principal retarget.cl (ya existe en la raíz del proyecto).

---

### ✅ TAREA 2: Crear Subdominio `app.retarget.cl` (PERMANENTE)

Este subdominio apuntará al servidor local donde se ejecutará la aplicación CRM.

**En cPanel:**
1. Ir a "Subdominios" o "DNS Zone Editor"
2. Crear subdominio: `app.retarget.cl`
3. Configurar para apuntar al servidor actual (retarget.cl) o usar un registro A si el hosting lo permite
   ```
   Tipo: CNAME o A (según tu configuración)
   Nombre: app
   Destino: retarget.cl o [IP-del-servidor]
   TTL: 3600
   ```

**⚠️ NOTA:** Consulta con tu proveedor de hosting la mejor forma de configurar un subdominio que apunte al mismo servidor.

---

### ✅ TAREA 3: Ejecutar la Aplicación CRM

La aplicación debe ejecutarse como un servicio en el servidor del hosting que soporta Python.

#### Opción 1: Usar el Launcher (Recomendado)

Ejecuta el archivo launcher:
```bash
python launcher.py
```

Esto iniciará la aplicación. El launcher está configurado para:
- Cargar la configuración del sistema
- Inicializar la base de datos
- Conectar con APIs externas (Meta WhatsApp, etc.)
- Escuchar en el puerto configurado

#### Opción 2: Ejecutar Backend Directamente

Si necesitas más control:
```bash
cd backend/
python main.py
```

#### Configuración de Persistencia (Importante)

Para que la aplicación se mantenga ejecutándose incluso después de cerrar la sesión SSH:

**Opción A: Usar `nohup` (simple)**
```bash
nohup python launcher.py > app.log 2>&1 &
```

Esto:
- Ejecuta `launcher.py` en background
- Guarda logs en `app.log`
- Persiste aunque cierres la sesión

**Opción B: Crear un servicio systemd (avanzado)**
Si el hosting lo permite, contacta a tu proveedor para configurar un servicio systemd que inicie automáticamente con el servidor.

#### Verificación

Para confirmar que la app está corriendo:
```bash
curl http://localhost:8000  # O el puerto que uses
```

O accede a `https://app.retarget.cl` desde un navegador.

---

## 🔍 VERIFICACIÓN

Una vez configurados los subdominios, verifica con estos comandos:

### En Windows (PowerShell):
```powershell
nslookup review.retarget.cl
nslookup app.retarget.cl
```

### En Linux/Mac:
```bash
dig review.retarget.cl
dig app.retarget.cl
```

**Resultado esperado:** Deben resolver a los dominios de Heroku/Railway.

---

## ⏱️ TIEMPO DE PROPAGACIÓN DNS

- **Mínimo:** 15-30 minutos
- **Máximo:** 24-48 horas (raro)
- **Promedio:** 2-4 horas

**Consejo:** Configurar con TTL bajo (3600 segundos = 1 hora) para cambios más rápidos.

---

## 🔒 HTTPS / SSL

**¿Necesito configurar SSL?**

**SÍ, pero tu proveedor de hosting probablemente lo puede hacer.** El subdominio `app.retarget.cl` necesita HTTPS para que Meta apruebe la aplicación.

**Opciones:**

1. **AutoSSL (incluido en muchos hostings)**: cPanel/hosting proporciona SSL gratis automático para subdominios
2. **Let's Encrypt**: Certificado gratuito, renovación automática
3. **Contactar a tu proveedor**: Ellos pueden habilitar HTTPS en el subdominio en minutos

Una vez que `app.retarget.cl` esté configurado en DNS, solicita SSL al hosting.

---

## 📝 RESUMEN DE CONFIGURACIÓN DNS

| Subdominio | Tipo | Destino | TTL | Propósito |
|------------|------|---------|-----|-----------|
| `app` | CNAME/A | retarget.cl o [IP-servidor] | 3600 | Producción con datos reales |

*(Consultar con hosting la configuración exacta)*

---

## ❓ DUDAS FRECUENTES

### ¿Por qué solo 1 subdominio?

Meta ahora requiere que probemos con **datos reales** en la App Review, no con datos de prueba. Por eso usamos un solo `app.retarget.cl` con la base de datos real.

### ¿Es seguro usar datos reales para Meta?

**Sí**, siempre que:
- La aplicación tenga autenticación y control de acceso
- La política de privacidad esté disponible
- Solo usuarios autorizados puedan acceder
- Los datos estén encriptados en tránsito (HTTPS)

### ¿Qué pasa si la aplicación se cae?

Por eso es importante usar `nohup` o un servicio systemd para mantenerla corriendo. El hosting puede reiniciar el servidor en cualquier momento, así que el servicio debe iniciarse automáticamente.

### ¿Afecta esto al WordPress actual?

**No.** El WordPress en `retarget.cl` funciona independientemente. El subdominio `app.retarget.cl` es una aplicación separada.

### ¿Qué puertos puedo usar?

**Consulta con tu proveedor sobre qué puertos permite.** Típicamente:
- Puerto 80 (HTTP)
- Puerto 443 (HTTPS)
- Puertos > 1024 para no-root

---

## 📞 CONTACTO

Si tienes dudas técnicas sobre la configuración:

- **Email:** [tu-email@ejemplo.com]
- **Teléfono:** [tu-teléfono]

**Por favor notifícame cuando:**
- ✅ Hayas subido `privacy-policy.html`
- ✅ Hayas creado los subdominios
- ✅ Los DNS estén propagados y funcionando

---

## 🚀 SIGUIENTE PASO

**Lo que necesito de ti:**

1. Confirmar que puedes crear el subdominio `app.retarget.cl`
2. Confirmar que puedes habilitar HTTPS en el subdominio
3. Confirmar que Python está disponible en el servidor (para ejecutar launcher.py)
4. Tiempo estimado para completar

**Lo que haré yo:**

1. Preparar la aplicación y la base de datos de producción
2. Enviarte el comando exacto para ejecutar la app: `python launcher.py`
3. Verificar que todo esté funcionando en `https://app.retarget.cl`
4. Hacer submit a Meta para App Review

---

## 📊 DIAGRAMA DE ARQUITECTURA

```
┌───────────────────────────────────────────────────────────┐
│                    retarget.cl                            │
│         (WordPress + Privacy Policy)                      │
│    https://retarget.cl/privacy-policy.html               │
└───────────────────────────────────────────────────────────┘
                           │
                           │ CNAME/A Record
                           ▼
                   ┌───────────────────┐
                   │  app.retarget.cl  │
                   │   (Subdominio)    │
                   └─────────┬─────────┘
                             │
                             │ (apunta al mismo servidor)
                             ▼
        ┌────────────────────────────────────────┐
        │         Hosting con Python             │
        │    (Ejecuta launcher.py o main.py)    │
        │                                        │
        │  ┌──────────────────────────────────┐ │
        │  │   CRM APP (Flask/FastAPI)        │ │
        │  │  - Autenticación                 │ │
        │  │  - Base de datos con datos reales│ │
        │  │  - APIs de Meta/WhatsApp         │ │
        │  │  - Control de acceso             │ │
        │  └──────────────────────────────────┘ │
        └────────────────────────────────────────┘
```

---

## ✅ CHECKLIST FINAL

- [ ] Verificar que privacy-policy.html sea accesible en https://retarget.cl/privacy-policy.html
- [ ] Subdominio `app.retarget.cl` creado (CNAME o A record)
- [ ] DNS propagado (verificado con nslookup/dig)
- [ ] HTTPS habilitado en `app.retarget.cl`
- [ ] Aplicación ejecutándose: `python launcher.py` o en background con `nohup`
- [ ] `https://app.retarget.cl` accesible y funcional
- [ ] Notificar a Ricardo con el resultado

---

**¡Muchas gracias por tu ayuda! 🙏**

Con esto podré completar el proceso de App Review de Meta y lanzar la plataforma.
