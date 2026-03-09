#!/usr/bin/env python3
"""
Script para inicializar la base de datos.
Se ejecuta automáticamente en el startup del contenedor Docker.
"""

import sys
import time
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def wait_for_database(database_url: str, max_retries: int = 30, retry_delay: int = 1):
    """
    Esperar a que la base de datos esté disponible.
    
    Args:
        database_url: URL de conexión a la BD
        max_retries: Número máximo de intentos
        retry_delay: Segundos entre intentos
    """
    logger.info(f"⏳ Esperando que la base de datos esté disponible...")
    logger.info(f"   URL: {database_url[:50]}...")
    
    engine = create_engine(database_url, echo=False)
    
    for attempt in range(1, max_retries + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info(f"✅ Base de datos disponible (intento {attempt})")
            return True
        except OperationalError as e:
            if attempt < max_retries:
                logger.warning(f"⏳ Intento {attempt}/{max_retries} fallido, reintentando en {retry_delay}s...")
                time.sleep(retry_delay)
            else:
                logger.error(f"❌ No se pudo conectar a la base de datos después de {max_retries} intentos")
                logger.error(f"   Error: {e}")
                return False
    
    return False


def init_database():
    """Inicializar la base de datos (crear tablas si no existen)."""
    try:
        logger.info("📊 Inicializando base de datos...")
        
        from backend.database import init_db
        init_db()
        
        logger.info("✅ Base de datos inicializada correctamente")
        return True
    except Exception as e:
        logger.error(f"❌ Error inicializando base de datos: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Función principal."""
    import os
    from backend import config
    
    logger.info("🚀 Iniciando proceso de configuración de base de datos")
    logger.info(f"   ENV: {config.ENV}")
    logger.info(f"   DATABASE_URL: {config.DATABASE_URL[:50]}...")
    
    # Esperar a que la BD esté disponible (solo en producción)
    if config.IS_WEB_ENV:
        if not wait_for_database(config.DATABASE_URL):
            logger.error("❌ No se pudo conectar a la base de datos")
            sys.exit(1)
    
    # Inicializar BD
    if not init_database():
        logger.error("❌ No se pudo inicializar la base de datos")
        sys.exit(1)
    
    logger.info("✅ Configuración completada exitosamente")
    sys.exit(0)


if __name__ == '__main__':
    main()
