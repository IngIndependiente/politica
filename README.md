# Agente Político - CRM Politics

Sistema de análisis de conversaciones y gestión de contactos ciudadanos.

## Estructura

```
├── backend/          # API FastAPI, config, base de datos, agente IA, integraciones
│   ├── main.py       # API FastAPI
│   ├── config.py     # Configuración centralizada
│   ├── control.py    # Control del backend (start/stop/sync)
│   ├── agent/        # Agente LangGraph (extracción de datos con Gemini)
│   ├── database/     # Modelos, servicios, storage (SQLAlchemy + DataFrames)
│   └── integrations/ # Meta API, WhatsApp API
├── frontend/         # Dashboard Dash (interfaz web)
│   ├── app.py        # Aplicación Dash
│   └── config.py     # Re-exporta backend.config
├── guias/            # Documentación, guías de uso y políticas
├── data/             # Archivos Parquet (modo local)
├── exports/          # Exportaciones CSV
├── launcher.py       # Launcher con ventana nativa (pywebview)
└── *.py              # Utilidades (generadores, migraciones, tests)
```

## Inicio Rápido

```bash
# Backend
python -m backend.main

# Frontend (otra terminal) 
python -m frontend.app

# O todo junto con ventana nativa
python launcher.py
```

## Documentación

Ver [guias/README.md](guias/README.md) para documentación completa del proyecto.
