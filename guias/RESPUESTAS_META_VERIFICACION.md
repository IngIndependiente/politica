# RESPUESTAS PARA VERIFICACIÓN DE META - APP CRM POLÍTICO

## 📋 PERMISOS NECESARIOS

### ✅ Permisos a SOLICITAR:

1. ✅ **business_management** - Gestión de activos empresariales (DEPENDENCIA REQUERIDA)
2. ✅ **pages_messaging** - Facebook Messenger
3. ✅ **pages_show_list** - Listar páginas del usuario
4. ✅ **instagram_basic** - Información básica de Instagram Business
5. ✅ **instagram_manage_messages** - Instagram Direct Messages
6. ✅ **pages_read_engagement** - Historial de conversaciones Facebook
7. ✅ **whatsapp_business_messaging** - WhatsApp mensajes
8. ✅ **whatsapp_business_management** - Gestión cuenta WhatsApp

### ❌ Permisos a ELIMINAR (innecesarios):

- **instagram_business_basic** - Nombre antiguo/alternativo de instagram_basic. Son el mismo permiso, solo necesitas uno. Meta recomienda usar `instagram_basic` en la API actual.
- **instagram_business_manage_messages** - Duplicado de instagram_manage_messages (mismo caso que el anterior)
- **pages_manage_metadata** - No modificas nombre, descripción o configuración de la página
- **instagram_manage_comments** - No gestionas comentarios públicos, solo mensajes directos
- **instagram_content_publish** - No publicas posts/stories en Instagram
- **public_profile** - No necesitas información de perfiles públicos de usuarios
- **instagram_manage_insights** - No usas estadísticas/métricas de alcance

---

## 📝 RESPUESTAS DETALLADAS PARA META

### 1. ¿Cómo usará la app **business_management**?

**Respuesta:**

> **IMPORTANTE:** Este permiso se solicita como DEPENDENCIA REQUERIDA para los permisos `pages_messaging`, `pages_show_list` e `instagram_manage_messages`. No se usa directamente para gestionar Business Manager.
>
> **Justificación técnica:**
> Nuestra aplicación es una plataforma multi-tenant que permite a MÚLTIPLES candidatos políticos y organizaciones usar nuestro CRM. Cuando un candidato se registra:
>
> 1. Usuario hace clic en "Conectar con Facebook" en nuestra app
> 2. Se inicia flujo de **Facebook Login for Business**
> 3. Usuario debe seleccionar qué páginas de Facebook e Instagram Business quiere conectar a la app
> 4. Usuario debe otorgar explícitamente permisos para que nuestra app gestione mensajes de esas páginas
> 5. `business_management` es necesario para que el usuario pueda ELEGIR qué activos empresariales (páginas/cuentas) conectar
>
> **Flujo en la app:**
> - Administrador de página navega por Facebook Login flow
> - Selecciona las páginas de Facebook e Instagram handles específicas
> - Proporciona permisos necesarios a la app
> - App informa al usuario: "Debe proporcionar explícitamente permisos para gestionar sus activos empresariales"
>
> **Código implementado:** Facebook Login for Business en frontend con scope: `business_management,pages_messaging,pages_show_list,instagram_manage_messages`
>
> **NO usamos este permiso para:** Crear/eliminar cuentas de Business Manager, gestionar configuración empresarial fuera de las páginas seleccionadas por el usuario, o acceder a activos no autorizados explícitamente.

---

### 2. ¿Cómo usará la app **pages_show_list**?

**Respuesta:**

> Utilizamos pages_show_list para permitir que el usuario **seleccione qué páginas de Facebook** desea conectar a nuestra plataforma durante el flujo de Facebook Login for Business.
>
> **Flujo de uso:**
> 1. Usuario inicia sesión en nuestra plataforma web
> 2. Hace clic en "Conectar Facebook/Instagram"
> 3. Facebook Login muestra TODAS sus páginas administradas
> 4. Usamos `pages_show_list` para obtener la lista completa de páginas donde el usuario es admin
> 5. Usuario selecciona la(s) página(s) política(s) que desea conectar
> 6. App guarda solo las páginas autorizadas por el usuario
>
> **Endpoint usado:** GET /me/accounts (para listar páginas donde el usuario tiene rol de admin)
>
> **Ejemplo práctico:**
> - Juan Pérez es candidato a alcalde de 3 comunas
> - Tiene 4 páginas de Facebook: "Juan Pérez Alcalde Comuna A", "Juan Pérez Candidato B", "Mi negocio personal", "Página familiar"
> - Con `pages_show_list` ve las 4 páginas
> - Selecciona solo las 2 páginas políticas que desea conectar al CRM
> - App solo procesa mensajes de esas 2 páginas autorizadas
>
> **Casos de uso multi-tenant:**
> - Diferentes candidatos en la misma plataforma
> - Cada uno conecta sus propias páginas
> - Sistema mantiene datos aislados por página/candidato

---

### 3. ¿Cómo usará la app **pages_messaging**?

**Respuesta:**

> Nuestra aplicación es una plataforma CRM multi-tenant para gestión de contactos ciudadanos en campañas políticas. Múltiples candidatos y organizaciones políticas pueden registrarse y usar nuestra app para procesar mensajes de SUS PROPIAS páginas de Facebook.
>
> **Flujo de uso (para cada candidato que usa nuestra plataforma):**
> 1. Candidato se registra en nuestra plataforma web
> 2. Conecta su página de Facebook mediante Facebook Login for Business
> 3. Ciudadano envía mensaje a la página de Facebook del candidato
> 4. Webhook recibe el mensaje en tiempo real (endpoint: /webhook)
> 5. Sistema de IA (Google Gemini) analiza el mensaje para extraer información demográfica estructurada: nombre completo, edad, género, ubicación, ocupación
> 6. Identifica automáticamente temas de interés político mencionados (Salud, Educación, Seguridad, Economía, Medio Ambiente, Transporte, Vivienda, Empleo, Corrupción)
> 7. Almacena la información en base de datos aislada por candidato
> 8. Genera perfiles demográficos y segmentación de votantes por intereses
> 9. **Respuesta automática** (opcional): Sistema puede enviar confirmación de recepción dentro de 30 segundos
>
> **Experiencia automatizada:**
> - Ciudadano: "Hola, soy Juan Pérez de 28 años, me preocupa la seguridad"
> - Bot responde en <30 seg: "Gracias Juan, hemos registrado tu preocupación sobre seguridad. ¿Hay algo específico que te afecte?"
> - Sistema extrae y almacena: Nombre, edad, interés (Seguridad)
>
> **Features implementadas:**
> - Quick Replies: Botones de respuesta rápida con temas predefinidos
> - Ice Breakers: Mensajes de inicio de conversación configurables
> - Persistent Menu: Menú con opciones como "Mis datos", "Propuestas", "Contactar equipo"
>
> **Custom Inbox Solution:**
> SÍ - Nuestra app incluye una interfaz de bandeja de entrada personalizada donde agentes humanos del equipo del candidato pueden:
> - Leer mensajes que la automatización no pudo procesar
> - Responder manualmente a preguntas complejas
> - Eliminar mensajes spam
> - Escalación: Si bot no entiende pregunta → envía a agente humano → agente responde en dashboard
>
> **Unsent Messages:**
> - Sistema detecta cuando usuario borra mensaje (webhook: message_unsent)
> - Elimina información extraída de ese mensaje de la base de datos
> - Mantiene privacidad del usuario
>
> **NO enviamos mensajes masivos ni spam**. Solo respuestas automáticas a conversaciones iniciadas por ciudadanos y procesamiento de información demográfica.

---

### 4. ¿Cómo usará la app **instagram_basic**?

**Respuesta:**

> Utilizamos instagram_manage_messages para procesar mensajes directos (DMs) de Instagram de manera idéntica a Facebook Messenger. Muchos ciudadanos, especialmente jóvenes, prefieren Instagram como canal de comunicación.
>
> **Flujo de uso:**
> 1. Ciudadano envía mensaje directo a la cuenta de Instagram Business del candidato
> 2. Webhook recibe el mensaje en tiempo real
> 3. Sistema de IA analiza el contenido para extraer: datos demográficos (nombre, edad, género, ubicación) y temas de interés político
> 4. Información se almacena en el mismo CRM unificado
> 5. Permite análisis demográfico cruzado entre plataformas
>
> **Casos de uso específicos:**
> - Joven de 22 años escribe: "Hola, me llamo Ana Rodríguez, vivo en Providencia y me preocupa la falta de empleos para profesionales jóvenes"
> - Sistema extrae: Nombre: Ana Rodríguez, Edad: 22, Ubicación: Providencia, Interés: Empleo
> - Candidato puede segmentar votantes jóvenes preocupados por empleo y diseñar propuestas específicas
>
> No publicamos contenido ni accedemos a comentarios públicos, solo procesamos mensajes privados enviados voluntariamente.

---

### 5. ¿Cómo usará la app **instagram_manage_messages**?

**Respuesta:**

> Utilizamos instagram_manage_messages para procesar mensajes directos (DMs) de Instagram de múltiples candidatos políticos que usan nuestra plataforma. Funciona de manera idéntica a Facebook Messenger pero para Instagram Business/Creator.
>
> **Flujo de uso (experiencia automatizada):**
> 1. Candidato configura su cuenta en nuestra plataforma mediante Facebook Login for Business
> 2. Ciudadano envía mensaje directo a Instagram Business del candidato
> 3. Webhook recibe mensaje en tiempo real (endpoint: /webhook configurado con instagram_business_account_id)
> 4. **Respuesta automática en <30 segundos:**
>    - Bot: "¡Hola! Soy el asistente del candidato. ¿En qué puedo ayudarte?"
> 5. Sistema de IA analiza contenido para extraer: datos demográficos (nombre, edad, género, ubicación) y temas de interés político
> 6. Información se almacena en CRM aislado por candidato
> 7. Análisis demográfico cruzado entre Facebook, Instagram y WhatsApp
>
> **Automatización simple (ejemplo de flow):**
> ```
> Usuario: "Hola"
> Bot (<30 seg): "¡Hola! Soy el asistente de [Candidato]. ¿Qué te gustaría saber?"
>   [Quick Reply 1: 📋 Ver propuestas]
>   [Quick Reply 2: 🗣️ Expresar preocupación]
>   [Quick Reply 3: 📞 Hablar con equipo]
>
> Usuario selecciona: "Expresar preocupación"
> Bot: "¿Qué tema te preocupa más?"
>   [Quick Reply: Seguridad]
>   [Quick Reply: Educación]
>   [Quick Reply: Salud]
>   [Quick Reply: Economía]
>
> Usuario: "Seguridad. Soy María, 35 años, vivo en Santiago Centro"
> Bot: "Gracias María, hemos registrado tu preocupación sobre seguridad. Un miembro del equipo revisará tu mensaje."
> Sistema: Extrae → Nombre: María, Edad: 35, Ubicación: Santiago Centro, Interés: Seguridad
> ```
>
> **Features interactivas implementadas:**
>
> 1. **Quick Replies (Respuestas Rápidas):**
>    - Botones predefinidos que el usuario puede tocar
>    - Ejemplo: "Salud", "Educación", "Seguridad", "Economía"
>    - Configurables por cada candidato en dashboard
>
> 2. **Ice Breakers:**
>    - Mensajes de inicio automáticos cuando usuario abre chat por primera vez
>    - Ejemplo: "¿Qué te preocupa de tu comuna?", "¿Quieres conocer nuestras propuestas?"
>
> 3. **Persistent Menu:**
>    - Menú lateral con opciones permanentes
>    - Opciones: "Ver propuestas", "Mis datos registrados", "Contactar equipo humano"
>
> **Custom Inbox Solution: SÍ**
>
> Nuestra app incluye interfaz de bandeja de entrada donde agentes humanos pueden:
> - **Leer mensajes:** Ver todos los mensajes recibidos en tiempo real
> - **Responder manualmente:** Si bot no puede procesar pregunta compleja, agente responde
> - **Eliminar mensajes:** Borrar spam o mensajes inapropiados
> - **Escalación:** Mensajes que bot no entiende se marcan para revisión humana
>
> **Cómo probar escalación a agente humano:**
> 1. Enviar mensaje complejo: "¿Cuál es tu postura sobre la reforma tributaria del artículo 47-B?"
> 2. Bot detecta que no puede responder automáticamente
> 3. Envía respuesta: "Excelente pregunta. Un miembro de nuestro equipo te responderá pronto."
> 4. Mensaje aparece en dashboard marcado como "⚠️ Requiere atención humana"
> 5. Agente en dashboard lee mensaje y responde manualmente
> 6. Respuesta llega al ciudadano por Instagram Direct
>
> **Unsent Messages (Mensajes Borrados):**
> 
> Cómo manejamos cuando usuario borra un mensaje:
> 1. Webhook recibe evento `messages_unsent`
> 2. Sistema identifica qué mensaje fue borrado por su `message_id`
> 3. **Elimina información extraída** de ese mensaje de la base de datos
> 4. **Respeta privacidad:** Si usuario borró mensaje, no debe quedar rastro de datos extraídos
> 5. Log de auditoría registra: "Mensaje {id} borrado por usuario, datos eliminados"
>
> **Ejemplo de prueba:**
> - Usuario envía: "Hola, soy Juan Pérez, tengo 28 años"
> - Sistema guarda: Nombre: Juan Pérez, Edad: 28
> - Usuario BORRA el mensaje inmediatamente
> - Webhook recibe unsent event
> - Sistema elimina: Nombre y Edad de la base de datos
> - Dashboard ya no muestra esa información
>
> **Endpoints usados:**
> - `GET /{instagram-business-account-id}/conversations` - Listar conversaciones
> - `GET /{conversation-id}/messages` - Obtener mensajes
> - `POST /{instagram-business-account-id}/messages` - Enviar mensajes/respuestas
> - Webhooks: `messages`, `messaging_postbacks`, `message_reactions`, `messages_unsent`
>
> **Datos procesados:**
> - Contenido del mensaje (texto)
> - ID del remitente (Instagram User IGSID)
> - Timestamp del mensaje
> - Indicadores de lectura (read receipts)
>
> **No realizamos:** Publicación de contenido, acceso a comentarios públicos, envío de mensajes no solicitados. Solo procesamos mensajes directos privados enviados voluntariamente por ciudadanos.

---

### 6. ¿Cómo usará la app **pages_read_engagement**?

**Respuesta:**

> Utilizamos pages_read_engagement para sincronizar el historial completo de conversaciones de Facebook Messenger, incluyendo mensajes anteriores a la instalación de nuestra aplicación.
>
> **Justificación:**
> Cuando un candidato comienza a usar nuestra app, ya tiene un historial de conversaciones con ciudadanos en su página de Facebook. Este permiso nos permite:
>
> 1. **Importar conversaciones históricas** (función: `sincronizar_facebook` en sync_conversations.py)
> 2. **Análisis retroactivo** de intereses ciudadanos de meses/años anteriores
> 3. **Evitar duplicados** al verificar si una persona ya contactó previamente
> 4. **Construir contexto** para futuras conversaciones
>
> **Ejemplo práctico:**
> - Candidato instaló la app el 15 de enero de 2026
> - Tiene conversaciones con 500 ciudadanos desde julio de 2025
> - Ejecutamos sincronización manual para importar esas 500 conversaciones
> - Sistema analiza cada conversación histórica y construye la base de datos completa
> - Permite generar reportes estadísticos desde el inicio de la campaña, no solo desde la instalación
>
> **Frecuencia de uso:** Principalmente durante configuración inicial (sincronización masiva) y periódicamente para actualizar conversaciones existentes. No se usa en tiempo real para cada mensaje.

---

### 4. ¿Cómo usará la app **instagram_basic**?

**Respuesta:**

> Utilizamos instagram_basic para obtener información básica de las cuentas de **Instagram Business/Creator** de los candidatos políticos que usan nuestra plataforma, conectadas a sus páginas de Facebook.
>
> **NOTA IMPORTANTE:** A pesar del nombre "basic" (sin "business"), este permiso **SÍ es para cuentas de Instagram Business/Creator**. Es el permiso oficial de Meta para acceder a perfiles profesionales de Instagram.
>
> **Funcionalidades específicas:**
>
> 1. **Durante Facebook Login for Business:**
>    - Usuario conecta su página de Facebook
>    - Llamamos `GET /me/accounts?fields=instagram_business_account`
>    - Obtenemos ID de Instagram Business asociado a cada página
>    - Validamos que la cuenta es tipo Business/Creator (requisito obligatorio para Instagram Messaging)
>    - Mostramos al usuario: "✅ Instagram @candidato_ejemplo conectado exitosamente"
>
> 2. **Configuración de webhooks:**
>    - Usamos `instagram_business_account.id` para suscribir webhooks
>    - Endpoint: POST /{instagram-business-account-id}/subscribed_apps
>    - Permite recibir notificaciones de mensajes directos
>
> 3. **Validación multi-tenant:**
>    - Verificamos que cada candidato tiene cuenta Business/Creator válida
>    - Prevenimos conexión de cuentas personales (no soportadas por API)
>    - Asociamos correctamente mensajes a la cuenta Business correcta
>
> **Datos accedidos:**
> - ID de la cuenta de Instagram Business (`instagram_business_account.id`)
> - Nombre de usuario (@candidato_ejemplo)
> - ID de conexión con página de Facebook
> - Validación de tipo de cuenta (Business/Creator)
>
> **Endpoints usados:**
> - `GET /{page-id}?fields=instagram_business_account`
> - `GET /{instagram-business-account-id}?fields=id,username,name`
>
> **Requisito:** La cuenta de Instagram del candidato DEBE ser Business o Creator, no puede ser personal. Las cuentas personales no pueden recibir mensajes mediante la API.
>
> **No accedemos a:** publicaciones, stories, estadísticas de alcance, lista de seguidores, métricas de engagement, contenido del feed. Solo información básica de identificación y validación de cuenta profesional necesaria para configurar messaging.

---

### 5. ¿Cómo usará la app **whatsapp_business_messaging**?

**Respuesta:**

> Utilizamos whatsapp_business_messaging para recibir y responder mensajes de WhatsApp Business, permitiendo a ciudadanos contactar al candidato a través de la plataforma de mensajería más popular en Latinoamérica.
>
> **Flujo de uso:**
> 1. Ciudadano envía mensaje de WhatsApp al número de WhatsApp Business del candidato
> 2. Webhook recibe notificación en tiempo real (endpoint: /webhook/whatsapp)
> 3. Sistema de IA analiza el mensaje para extraer información demográfica y temas de interés
> 4. Información se almacena en el CRM junto con datos de Facebook e Instagram
> 5. Sistema puede enviar respuesta de confirmación automática (opcional)
> 6. Marca mensaje como "leído" para notificar al ciudadano
>
> **Ejemplo de conversación:**
> ```
> Ciudadano: "Hola, soy Pedro González, 45 años, comerciante de La Florida. 
>             Me preocupa la inseguridad en mi comuna, necesitamos más patrullas"
>
> Sistema procesa:
> - Nombre: Pedro González
> - Edad: 45
> - Ocupación: Comerciante
> - Ubicación: La Florida
> - Interés: Seguridad
> - Plataforma: WhatsApp
> ```
>
> **Ventajas de WhatsApp:**
> - Mayor adopción en población de 40+ años
> - Comunicación más directa y personal
> - Notificaciones push más efectivas
> - Autenticación por número telefónico
>
> **Código implementado:** integrations/whatsapp_api.py y backend/main.py (endpoints /webhook/whatsapp)
>
> **No realizamos:** envío de mensajes masivos, cadenas, promociones comerciales, ni spam. Solo procesamos mensajes individuales iniciados por ciudadanos.

---

### 6. ¿Cómo usará la app **whatsapp_business_management**?

**Respuesta:**

> Utilizamos whatsapp_business_management para gestionar la configuración de la cuenta de WhatsApp Business y verificar que está correctamente conectada a nuestra aplicación.
>
> **Funcionalidades específicas:**
>
> 1. **Verificar configuración de cuenta:**
>    - Obtener Phone Number ID necesario para enviar/recibir mensajes
>    - Validar que la cuenta de WhatsApp Business está activa
>    - Confirmar que webhooks están correctamente configurados
>
> 2. **Gestionar perfil de negocio:**
>    - Verificar nombre del candidato mostrado en WhatsApp
>    - Validar número de teléfono asociado
>    - Confirmar descripción del perfil político
>
> 3. **Configuración técnica:**
>    - Actualizar URL de webhook cuando cambie servidor
>    - Configurar eventos a recibir (mensajes entrantes, cambios de estado)
>    - Verificar tokens de acceso
>
> **Flujo de onboarding:**
> ```
> 1. Candidato conecta su WhatsApp Business a nuestra app
> 2. Sistema usa whatsapp_business_management para:
>    - Obtener WHATSAPP_PHONE_NUMBER_ID
>    - Obtener WHATSAPP_BUSINESS_ACCOUNT_ID
>    - Validar que puede recibir webhooks
> 3. Configura webhook URL: https://tu-servidor.com/webhook/whatsapp
> 4. Valida con test de verificación (hub.verify_token)
> 5. Sistema queda listo para recibir mensajes
> ```
>
> **Variables de entorno configuradas:**
> - WHATSAPP_PHONE_NUMBER_ID: ID único del número de WhatsApp
> - WHATSAPP_BUSINESS_ACCOUNT_ID: ID de la cuenta de negocio
> - WHATSAPP_VERIFY_TOKEN: Token de seguridad para webhooks
>
> **No realizamos:** gestión de múltiples cuentas comerciales, creación de nuevas cuentas de negocio, modificación de configuración empresarial fuera del alcance de la aplicación política.

---

## � SCREEN RECORDING - GUION DETALLADO PARA APP REVIEW

Meta requiere un video mostrando cómo OTROS usuarios pueden configurar y usar tu app. Este video debe demostrar:

### **PARTE 1: SETUP (Configuración) - 2 minutos**

#### 1. Login a la plataforma (15 segundos)
- **Mostrar:** Página de inicio de tu plataforma web
- **URL:** https://tu-dominio.com/login
- **Acción:** Hacer clic en "Registrarse" o "Iniciar Sesión"
- **Narración:** "Para comenzar, el candidato accede a nuestra plataforma CRM"

#### 2. Facebook Login for Business (45 segundos)
- **Mostrar:** Botón "Conectar con Facebook"
- **Acción:** Clic en botón
- **Dialog de Facebook aparece:**
  - Seleccionar "Continuar como [Tu Nombre]"
  - **IMPORTANTE:** Mostrar selección de páginas
    - Checkbox lista de páginas donde eres admin
    - Seleccionar la(s) página(s) política(s) a conectar
  - **IMPORTANTE:** Mostrar selección de Instagram
    - "Seleccionar cuenta de Instagram Business: @candidato_ejemplo"
  - Revisar permisos solicitados:
    - ✅ Gestionar mensajes de página
    - ✅ Ver lista de páginas
    - ✅ Mensajes de Instagram
    - ✅ Gestionar activos empresariales
- **Hacer clic en "Confirmar"**
- **Narración:** "El usuario debe otorgar explícitamente permisos para que nuestra app gestione sus activos empresariales: páginas de Facebook e Instagram Business"

#### 3. Configurar experiencia automatizada (60 segundos)
- **Mostrar:** Dashboard de configuración
- **Paso 1:** Configurar mensaje de bienvenida (Ice Breaker)
  - Campo: "Mensaje de inicio: ¡Hola! Soy el asistente del candidato..."
  - Guardar

- **Paso 2:** Configurar Quick Replies
  - Agregar botón: "Seguridad"
  - Agregar botón: "Educación"
  - Agregar botón: "Salud"
  - Agregar botón: "Economía"
  - Guardar

- **Paso 3:** Configurar respuestas automáticas
  - "Si usuario menciona 'seguridad' → Responder: 'Nuestro plan de seguridad incluye...'"
  - "Si usuario menciona 'educación' → Responder: 'Invertiremos en educación pública...'"
  - Guardar

- **Paso 4:** Activar bot
  - Toggle: "Estado del bot: ❌ Inactivo → ✅ Activo"
  - Confirmación: "✅ Bot configurado exitosamente"

- **Narración:** "El usuario configura mensajes de bienvenida, respuestas rápidas y automatizaciones que procesarán mensajes de ciudadanos"

---

### **PARTE 2: TESTING (Pruebas) - 2 minutos**

#### 4. Iniciar conversación con la experiencia automatizada (20 segundos)
- **Cambiar a teléfono móvil o emulador:**
- **Abrir Instagram**
- **Buscar:** @candidato_ejemplo (la cuenta configurada)
- **Enviar mensaje:** "Hola"
- **Cronómetro visible:** Mostrar que respuesta llega en <30 segundos

#### 5. Experiencia automatizada responde (40 segundos)
- **Bot responde (< 30 seg):**
  ```
  ¡Hola! Soy el asistente del candidato. ¿Qué te gustaría saber?
  
  [Quick Reply: 📋 Ver propuestas]
  [Quick Reply: 🗣️ Expresar preocupación]
  [Quick Reply: 📞 Hablar con equipo]
  ```

- **Usuario hace clic:** "Expresar preocupación"

- **Bot responde:**
  ```
  ¿Qué tema te preocupa más?
  
  [Quick Reply: Seguridad]
  [Quick Reply: Educación]
  [Quick Reply: Salud]
  [Quick Reply: Economía]
  ```

- **Usuario hace clic:** "Seguridad"

- **Usuario escribe:** "Soy Juan Pérez, 28 años, vivo en Santiago y me preocupa la delincuencia"

- **Bot responde (< 30 seg):**
  ```
  Gracias Juan, hemos registrado tu preocupación sobre seguridad. Un miembro de nuestro equipo revisará tu mensaje.
  ```

#### 6. Verificar datos en Custom Inbox (30 segundos)
- **Cambiar a laptop/desktop:**
- **Mostrar dashboard de la app**
- **Sección "Mensajes recibidos":**
  - Lista de conversaciones en tiempo real
  - **Aparece nueva entrada:**
    ```
    Juan Pérez | 28 años | Santiago | Seguridad
    Plataforma: Instagram
    Hace 1 minuto
    ```
- **Hacer clic en la conversación**
- **Modal muestra:**
  - Historial completo de mensajes
  - Datos extraídos automáticamente
  - Botón: "Responder manualmente"

#### 7. Agente humano responde (enviar mensaje) (20 segundos)
- **En el modal de conversación:**
- **Escribir respuesta manual:** "Hola Juan, gracias por compartir tu preocupación. Nuestro plan de seguridad incluye..."
- **Hacer clic:** "Enviar"
- **Cambiar a teléfono:**
- **Mostrar Instagram:** Juan recibe el mensaje del agente humano

#### 8. Eliminar mensaje (delete message) (10 segundos)
- **En dashboard:**
- **Buscar mensaje de spam o prueba**
- **Hacer clic:** ícono de papelera 🗑️
- **Confirmar:** "¿Eliminar este mensaje?"
- **Mensaje desaparece de la lista**

#### 9. Probar unsent message (mensaje borrado por usuario) (30 segundos)
- **Cambiar a teléfono:**
- **En Instagram, enviar nuevo mensaje:** "Hola, soy María González, tengo 35 años"
- **Esperar 5 segundos** (para que sistema procese)
- **BORRAR el mensaje** (mantener presionado → "Anular envío")
- **Cambiar a dashboard:**
- **Mostrar que:** Los datos de María NO aparecen en la base de datos
- **O si aparecieron:** Mostrar que desaparecen automáticamente cuando webhook recibe unsent event
- **Narración:** "Cuando un usuario borra su mensaje, nuestro sistema elimina automáticamente cualquier información extraída, respetando su privacidad"

---

### **PARTE 3: TESTING FACEBOOK MESSENGER (1 minuto)**

#### 10. Repetir flujo con Facebook Messenger
- **Abrir Facebook Messenger en móvil**
- **Buscar página:** "Candidato Ejemplo"
- **Enviar mensaje:** "Hola"
- **Bot responde en < 30 seg** con Quick Replies
- **Usuario interactúa** con automatización
- **Dashboard muestra** mensaje recibido en tiempo real
- **Mismo flujo:** Custom inbox, respuesta manual, delete

---

### **PARTE 4: WHATSAPP BUSINESS (1 minuto)** *(Opcional si ya configuraste WhatsApp)*

#### 11. Testing con WhatsApp
- **Abrir WhatsApp en móvil**
- **Enviar mensaje** al número de WhatsApp Business del candidato
- **Bot responde en < 30 seg**
- **Dashboard procesa** mensaje de WhatsApp
- **Mostrar datos extraídos** incluyendo número telefónico

---

## 📋 PLATFORM SETTINGS (Configuración de Plataforma)

En App Review submission, configura:

**Platform:** Website

**Site URL:** https://tu-dominio.com

**Login URL:** https://tu-dominio.com/login

---

## 📝 STEP-BY-STEP INSTRUCTIONS (Instrucciones Paso a Paso)

Copia esto en el formulario de Meta:

```
INSTRUCCIONES PARA PROBAR LA APP:

1. SETUP (Configuración):
   a. Ve a https://tu-dominio.com/login
   b. Haz clic en "Registrarse" o usa credenciales de prueba (si no usas Facebook Login)
   c. Haz clic en el botón "Conectar Facebook/Instagram"
   d. En el diálogo de Facebook Login for Business:
      - Selecciona la(s) página(s) de Facebook que deseas conectar
      - Selecciona la cuenta de Instagram Business asociada
      - Otorga todos los permisos solicitados
      - Haz clic en "Confirmar"
   e. En el dashboard, ve a "Configuración de Bot"
   f. Configura:
      - Mensaje de bienvenida: "¡Hola! Soy el asistente del candidato..."
      - Quick Replies: Seguridad, Educación, Salud, Economía
      - Respuestas automáticas para cada tema
   g. Activa el bot con el toggle "Estado: Activo"
   h. Guarda cambios

2. TESTING (Pruebas):
   a. Desde un teléfono móvil, abre Instagram
   b. Busca y accede a la cuenta de Instagram Business que configuraste
   c. Envía un mensaje directo: "Hola"
   d. Verifica que el bot responde en menos de 30 segundos con Quick Replies
   e. Interactúa con los botones de respuesta rápida
   f. Envía un mensaje más complejo incluyendo tu nombre, edad y preocupación
   g. Verifica que el bot procesa y responde apropiadamente

3. CUSTOM INBOX (Bandeja de Entrada):
   a. En el dashboard de la plataforma, ve a "Mensajes"
   b. Verifica que aparece la conversación que iniciaste
   c. Haz clic en la conversación para ver detalles
   d. Verifica que se extrajeron datos demográficos automáticamente
   e. Escribe una respuesta manual en el campo de texto
   f. Haz clic en "Enviar"
   g. Verifica en Instagram que recibes la respuesta del agente humano

4. DELETE MESSAGE (Eliminar Mensaje):
   a. En el dashboard, selecciona cualquier mensaje
   b. Haz clic en el ícono de eliminar (papelera)
   c. Confirma la eliminación
   d. Verifica que el mensaje desaparece

5. UNSENT MESSAGE (Mensaje Borrado):
   a. En Instagram, envía otro mensaje con información personal
   b. Inmediatamente borra el mensaje (Anular envío)
   c. Verifica en el dashboard que los datos NO aparecen o desaparecen automáticamente

6. FACEBOOK MESSENGER (Opcional):
   Repite los pasos 2-5 usando Facebook Messenger en lugar de Instagram

NOTAS IMPORTANTES:
- El bot DEBE responder en menos de 30 segundos
- Los mensajes borrados por usuarios DEBEN eliminarse de la base de datos
- La página/cuenta de Instagram DEBE ser de tipo Business o Creator
- Los agentes humanos pueden responder manualmente desde el dashboard
```

---

## 🔐 CREDENTIALS (Credenciales de Prueba)

**Opción 1: USO Facebook Login for Business**

Selecciona: "I use Facebook Login for Business to log into my website"

No necesitas proporcionar credenciales. Los revisores de Meta usarán sus propias cuentas de Facebook.

**Opción 2: NO USO Facebook Login for Business** *(solo si tu app requiere registro previo)*

Selecciona: "I don't use Facebook Login for Business to log into my website"

Proporciona credenciales de una cuenta de prueba:
```
Username: test_candidato@ejemplo.com
Password: [Tu contraseña de prueba segura]
```

⚠️ **NO incluyas:** Credenciales personales de Facebook, Instagram, o test users de Meta.

---

## �🎬 GUION PARA VIDEO DE DEMOSTRACIÓN (2-3 minutos)

### **Escena 1: Introducción (15 segundos)**
- **Visual:** Logo y nombre del candidato
- **Texto en pantalla:** "Sistema CRM - Gestión Inteligente de Contactos Ciudadanos"
- **Narración:** "Presentamos nuestro sistema de gestión de contactos para campañas políticas, que unifica comunicación ciudadana de Facebook, Instagram y WhatsApp."

---

### **Escena 2: Facebook Messenger (30 segundos)**
- **Visual:** Pantalla dividida (split screen)
  - **Izquierda:** Facebook Messenger mostrando página del candidato
  - **Derecha:** Dashboard de la aplicación en tiempo real

- **Acción:**
  1. Usuario envía mensaje en Messenger: *"Hola, me llamo Juan Pérez, tengo 28 años y vivo en Santiago. Me preocupa la falta de seguridad en mi barrio."*
  2. En el dashboard (derecha) aparece en tiempo real:
     - Notificación de nuevo contacto
     - Nombre: Juan Pérez
     - Edad: 28 años
     - Ubicación: Santiago
     - Interés detectado: **Seguridad** (etiqueta con color)

- **Narración:** "Cuando un ciudadano envía un mensaje por Facebook, nuestra IA extrae automáticamente su información demográfica y temas de interés."

---

### **Escena 3: Instagram Direct (30 segundos)**
- **Visual:** Pantalla dividida
  - **Izquierda:** Instagram Direct en smartphone
  - **Derecha:** Dashboard actualizándose

- **Acción:**
  1. Usuario envía DM en Instagram: *"Soy María González, 35 años, profesora. Necesitamos más inversión en educación pública."*
  2. Dashboard muestra nuevo registro:
     - Nombre: María González
     - Edad: 35 años
     - Ocupación: Profesora
     - Interés detectado: **Educación**

- **Narración:** "Instagram Direct funciona de la misma manera, capturando preocupaciones de ciudadanos que prefieren esta plataforma."

---

### **Escena 4: WhatsApp Business (30 segundos)**
- **Visual:** Pantalla dividida
  - **Izquierda:** WhatsApp Business en smartphone
  - **Derecha:** Dashboard agregando contacto

- **Acción:**
  1. Usuario envía mensaje de WhatsApp: *"Hola, soy Carlos Ruiz, 52 años, dueño de un almacén en Maipú. Me afecta mucho la economía, necesito apoyo a las PYMEs."*
  2. Dashboard registra:
     - Nombre: Carlos Ruiz
     - Edad: 52 años
     - Ocupación: Comerciante
     - Ubicación: Maipú
     - Interés detectado: **Economía**
     - Teléfono: +56912345678

- **Narración:** "WhatsApp permite llegar a segmentos de población que prefieren comunicación más directa y personal."

---

### **Escena 5: Dashboard y Análisis (45 segundos)**
- **Visual:** Pantalla completa del dashboard mostrando:
  1. **Tabla de contactos** con todos los ciudadanos registrados
  2. **Filtros aplicados:**
     - Seleccionar "Género: Femenino"
     - Seleccionar "Edad: 30-40"
     - Seleccionar "Interés: Educación"
     - Tabla se actualiza mostrando solo María González y otras mujeres similares

  3. **Gráficos estadísticos:**
     - Gráfico circular: Distribución por género (51% Femenino, 49% Masculino)
     - Gráfico de barras: Intereses más comunes
       - Seguridad: 35%
       - Educación: 28%
       - Salud: 22%
       - Economía: 15%

  4. **Exportar datos:**
     - Clic en botón "Exportar CSV"
     - Archivo descargado: `personas_export_20260204.csv`

- **Narración:** "El dashboard permite filtrar contactos por demografía e intereses, generar estadísticas en tiempo real y exportar datos para análisis avanzados o campañas segmentadas."

---

### **Escena 6: Vista Detallada de Conversación (20 segundos)**
- **Visual:** Dashboard → Clic en botón "Ver" de Juan Pérez
- **Acción:**
  1. Modal aparece con historial completo:
     ```
     Juan Pérez | 28 años | Masculino | Santiago
     Plataforma: Facebook Messenger
     
     HISTORIAL:
     [15/01/2026 14:30] Juan: "Hola, me preocupa la seguridad..."
     [15/01/2026 14:35] Candidato: "Gracias por tu mensaje, Juan..."
     [20/01/2026 10:15] Juan: "¿Cuál es tu propuesta para seguridad?"
     ```
  2. Información extraída automáticamente destacada:
     - ✅ Nombre completo
     - ✅ Edad
     - ✅ Ubicación
     - ✅ Interés: Seguridad

- **Narración:** "Cada contacto mantiene un historial completo de conversaciones con información extraída automáticamente por IA."

---

### **Escena 7: Cierre (10 segundos)**
- **Visual:** Logo del candidato + texto en pantalla
- **Texto:**
  ```
  CRM POLÍTICO
  Gestión inteligente de contactos ciudadanos con IA
  
  ✓ Facebook Messenger
  ✓ Instagram Direct
  ✓ WhatsApp Business
  ✓ Análisis con Google Gemini AI
  ```
- **Narración:** "Comunicación unificada, análisis inteligente, decisiones informadas."

---

## 📋 CHECKLIST ANTES DE ENVIAR A META

### Preparación técnica:
- [ ] Implementar código de WhatsApp ✅ (COMPLETADO)
- [ ] Configurar variables de entorno para WhatsApp ✅ (COMPLETADO)
- [ ] Verificar que el código de webhook esté actualizado ✅ (COMPLETADO)
- [ ] Probar webhooks localmente con ngrok
- [ ] Configurar servidor público HTTPS para webhooks
- [ ] Validar que .env tiene todos los valores necesarios

### Permisos:
- [ ] Eliminar 7 permisos innecesarios identificados
- [ ] Solicitar 8 permisos necesarios:
  - business_management (DEPENDENCIA)
  - pages_show_list  
  - pages_messaging
  - pages_read_engagement
  - instagram_basic
  - instagram_manage_messages
  - whatsapp_business_messaging
  - whatsapp_business_management

### Documentación:
- [ ] Grabar screen recording de 5-7 minutos siguiendo guion PARTE 1-4
- [ ] Copiar respuestas detalladas de este documento a formulario de Meta
- [ ] Copiar Step-by-Step Instructions al formulario
- [ ] Subir screen recording a YouTube (unlisted) o directamente en App Review
- [ ] Configurar Platform Settings: Website + URL de login
- [ ] Decidir método de autenticación: Facebook Login for Business O credenciales de prueba
- [ ] Verificar que privacy-policy.html esté accesible públicamente
- [ ] Completar Business Verification de Meta (si no está hecha)

### Configuración de Meta:
- [ ] Configurar URL de webhook en Facebook App Dashboard:
  - URL: `https://tu-dominio.com/webhook`
  - Verify Token: valor de `META_VERIFY_TOKEN`
- [ ] Configurar URL de webhook para WhatsApp:
  - URL: `https://tu-dominio.com/webhook/whatsapp`
  - Verify Token: valor de `WHATSAPP_VERIFY_TOKEN`
- [ ] Obtener y configurar `WHATSAPP_PHONE_NUMBER_ID`
- [ ] Obtener y configurar `WHATSAPP_BUSINESS_ACCOUNT_ID`

---

## 🚨 ADVERTENCIAS IMPORTANTES

### 1. **Aplicaciones Políticas - Restricciones de Meta**
Meta tiene políticas **MUY ESTRICTAS** para aplicaciones relacionadas con política:

- ✅ **Mencionar explícitamente** que es para CRM político en todas las descripciones
- ✅ **No ocultar** el propósito de la aplicación
- ✅ **Cumplir** con leyes locales de protección de datos (GDPR, LOPD, etc.)
- ✅ **Transparencia total** con los usuarios sobre qué datos se recopilan
- ✅ **No vender ni compartir** datos con terceros
- ❌ **Nunca** usar para desinformación, manipulación o interferencia electoral

### 2. **Protección de Datos**
Debes demostrar que cumples con:
- Almacenamiento seguro de datos (base de datos local cifrada recomendada)
- Políticas de privacidad claras (ya tienes `privacy-policy.html`)
- Consentimiento informado de usuarios
- Derecho al olvido (GDPR) - implementar endpoint para eliminar datos

### 3. **Límites de Rate Limiting**
WhatsApp Business API tiene límites estrictos:
- **Tier 1:** 1,000 conversaciones únicas en 24 horas
- Para aumentar tier, necesitas buen historial de cumplimiento
- **No enviar spam** o Meta bloqueará tu cuenta permanentemente

### 4. **Verificación de Negocio (Business Verification)**
Meta requiere Business Verification para permisos avanzados:
- Documento legal del candidato/partido político
- Dirección física verificada
- Número de teléfono de contacto
- Sitio web oficial del candidato

---

## 📞 PRÓXIMOS PASOS

### 1. **Configurar servidor público HTTPS**
Para que Meta pueda enviar webhooks, necesitas:
- Dominio con certificado SSL válido
- O usar servicio como ngrok para desarrollo: `ngrok http 8000`
- Configurar firewall para permitir IPs de Meta

### 2. **Completar configuración de WhatsApp**
En Meta App Dashboard → WhatsApp → Configuration:
1. Agregar número de teléfono a WhatsApp Business
2. Copiar Phone Number ID → pegar en `.env` como `WHATSAPP_PHONE_NUMBER_ID`
3. Copiar Business Account ID → pegar en `.env` como `WHATSAPP_BUSINESS_ACCOUNT_ID`
4. Configurar webhook URL en "Webhook fields" → seleccionar "messages"

### 3. **Probar integración**
```bash
# 1. Iniciar backend
python backend/main.py

# 2. Verificar webhooks
curl http://localhost:8000/webhook/whatsapp?hub.mode=subscribe&hub.verify_token=whatsapp_verify_token_secreto&hub.challenge=TEST

# 3. Enviar mensaje de prueba desde WhatsApp a tu número
# 4. Verificar en logs que se recibió:
#    ✅ WHATSAPP_WEBHOOK_VERIFIED
#    ✅ Mensaje WhatsApp procesado para +56912345678
```

---

## ✅ RESUMEN EJECUTIVO

**Permisos finales a solicitar:** 8 (7 funcionales + 1 dependencia)

**CAMBIOS IMPORTANTES vs versión anterior:**
- ✅ Agregado: `business_management` (REQUERIDO como dependencia)
- ✅ Agregado: `pages_show_list` (necesario para multi-tenant)
- ❌ Removido: 7 permisos innecesarios

**Tipo de aplicación:** Multi-tenant (OTROS candidatos pueden usar la app)

**Plataformas soportadas:**
- ✅ Facebook Messenger (pages_messaging + pages_read_engagement + pages_show_list)
- ✅ Instagram Direct (instagram_manage_messages + instagram_basic)
- ✅ WhatsApp Business (whatsapp_business_messaging + whatsapp_business_management)

**Features clave para App Review:**
- ✅ Facebook Login for Business (selección de páginas/cuentas)
- ✅ Respuestas automáticas en <30 segundos
- ✅ Quick Replies (botones de respuesta rápida)
- ✅ Ice Breakers (mensajes de bienvenida)
- ✅ Persistent Menu (menú lateral)
- ✅ Custom Inbox Solution (bandeja para agentes humanos)
- ✅ Manejo de unsent messages (respeto a privacidad)
- ✅ Delete messages (agentes pueden eliminar)

**Archivos clave implementados:**
- `integrations/whatsapp_api.py` - Cliente de WhatsApp ✅
- `backend/main.py` - Webhooks agregados ✅
- `config.py` - Variables de configuración ✅
- `.env` - Configuración de credenciales ✅
- `database/dataframe_services.py` - Soporte para búsqueda por teléfono ✅

**Screen recording requerido:** 5-7 minutos mostrando:
1. Setup completo con Facebook Login for Business
2. Configuración de bot (ice breakers, quick replies, automatización)
3. Testing de experiencia automatizada (<30 seg respuesta)
4. Custom inbox (leer, responder, eliminar mensajes)
5. Unsent messages (privacidad)

**¿Listo para enviar?** NO - Falta:
1. ⚠️ **CRÍTICO:** Implementar Facebook Login for Business en frontend
2. ⚠️ **CRÍTICO:** Implementar Quick Replies, Ice Breakers, Persistent Menu
3. ⚠️ **CRÍTICO:** Implementar manejo de unsent messages
4. Configurar servidor público HTTPS
5. Obtener Phone Number ID y Business Account ID de WhatsApp
6. Grabar screen recording de 5-7 minutos
7. Completar Business Verification

---

¿Necesitas ayuda con alguno de los pasos siguientes?
