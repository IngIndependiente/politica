#!/usr/bin/env python3
"""
Script de migración SQLite → PostgreSQL para CRM Política.
Preserva todos los datos acumulados durante la migración.

Uso:
    python migrate_sqlite_to_postgres.py --source sqlite:///agente_politico.db --target postgresql://user:pass@localhost/crm_politica
"""

import sys
import argparse
from datetime import datetime
from sqlalchemy import create_engine, inspect, MetaData, Table
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DatabaseMigrator:
    """Migrador de SQLite a PostgreSQL."""
    
    def __init__(self, source_url: str, target_url: str):
        """
        Inicializar migrador.
        
        Args:
            source_url: URL de SQLite (ej: sqlite:///agente_politico.db)
            target_url: URL de PostgreSQL (ej: postgresql://user:pass@localhost/crm_politica)
        """
        self.source_url = source_url
        self.target_url = target_url
        self.source_engine = None
        self.target_engine = None
        self.stats = {
            'tables': 0,
            'rows_migrated': 0,
            'errors': 0,
            'start_time': None,
            'end_time': None
        }
    
    def connect(self) -> bool:
        """Conectar a ambas bases de datos."""
        try:
            logger.info(f"Conectando a SQLite: {self.source_url}")
            self.source_engine = create_engine(self.source_url, echo=False)
            self.source_engine.connect().close()
            logger.info("✅ Conectado a SQLite")
            
            logger.info(f"Conectando a PostgreSQL: {self.target_url}")
            self.target_engine = create_engine(self.target_url, echo=False)
            self.target_engine.connect().close()
            logger.info("✅ Conectado a PostgreSQL")
            
            return True
        except SQLAlchemyError as e:
            logger.error(f"❌ Error de conexión: {e}")
            return False
    
    def create_target_schema(self):
        """Crear esquema en PostgreSQL usando los modelos."""
        try:
            logger.info("Creando esquema en PostgreSQL...")
            
            # Importar modelos
            from backend.database.models import Base
            
            # Crear todas las tablas
            Base.metadata.create_all(self.target_engine)
            logger.info("✅ Esquema creado en PostgreSQL")
            return True
        except Exception as e:
            logger.error(f"❌ Error creando esquema: {e}")
            return False
    
    def migrate_data(self) -> bool:
        """Migrar datos de SQLite a PostgreSQL."""
        try:
            self.stats['start_time'] = datetime.now()
            
            # Obtener metadata de SQLite
            source_metadata = MetaData()
            source_metadata.reflect(bind=self.source_engine)
            
            source_session = sessionmaker(bind=self.source_engine)()
            target_session = sessionmaker(bind=self.target_engine)()
            
            # Orden de tablas (respetando FK)
            table_order = [
                'usuarios_autorizados',
                'candidatos',
                'personas',
                'intereses',
                'persona_interes',
                'eventos',
                'conversaciones',
                'analisis',
                'meta_config'
            ]
            
            for table_name in table_order:
                if table_name not in source_metadata.tables:
                    logger.warning(f"⚠️ Tabla {table_name} no encontrada en SQLite")
                    continue
                
                logger.info(f"Migrando tabla: {table_name}")
                
                try:
                    # Obtener tabla de SQLite
                    source_table = source_metadata.tables[table_name]
                    
                    # Leer datos de SQLite
                    rows = source_session.execute(source_table.select()).fetchall()
                    logger.info(f"  → {len(rows)} filas encontradas")
                    
                    if len(rows) == 0:
                        logger.info(f"  → Tabla vacía, saltando")
                        self.stats['tables'] += 1
                        continue
                    
                    # Insertar en PostgreSQL
                    for row in rows:
                        # Convertir Row a dict
                        row_dict = dict(row._mapping) if hasattr(row, '_mapping') else dict(row)
                        
                        # Ejecutar INSERT directo
                        insert_stmt = source_table.insert().values(**row_dict)
                        target_session.execute(insert_stmt)
                        self.stats['rows_migrated'] += 1
                    
                    target_session.commit()
                    logger.info(f"  ✅ {len(rows)} filas migradas")
                    self.stats['tables'] += 1
                    
                except Exception as e:
                    logger.error(f"  ❌ Error migrando {table_name}: {e}")
                    target_session.rollback()
                    self.stats['errors'] += 1
            
            source_session.close()
            target_session.close()
            
            self.stats['end_time'] = datetime.now()
            return self.stats['errors'] == 0
            
        except Exception as e:
            logger.error(f"❌ Error en migración: {e}")
            return False
    
    def verify_migration(self) -> bool:
        """Verificar que la migración fue exitosa."""
        try:
            logger.info("\nVerificando migración...")
            
            source_metadata = MetaData()
            source_metadata.reflect(bind=self.source_engine)
            
            target_metadata = MetaData()
            target_metadata.reflect(bind=self.target_engine)
            
            source_session = sessionmaker(bind=self.source_engine)()
            target_session = sessionmaker(bind=self.target_engine)()
            
            all_match = True
            
            for table_name in source_metadata.tables:
                source_count = source_session.query(
                    source_metadata.tables[table_name]
                ).count()
                
                target_count = target_session.query(
                    target_metadata.tables[table_name]
                ).count()
                
                match = "✅" if source_count == target_count else "❌"
                logger.info(f"{match} {table_name}: SQLite={source_count}, PostgreSQL={target_count}")
                
                if source_count != target_count:
                    all_match = False
            
            source_session.close()
            target_session.close()
            
            return all_match
            
        except Exception as e:
            logger.error(f"❌ Error verificando: {e}")
            return False
    
    def print_summary(self):
        """Imprimir resumen de la migración."""
        duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds() if self.stats['end_time'] else 0
        
        print("\n" + "="*60)
        print("📊 RESUMEN DE MIGRACIÓN")
        print("="*60)
        print(f"Tablas migradas: {self.stats['tables']}")
        print(f"Filas migradas: {self.stats['rows_migrated']}")
        print(f"Errores: {self.stats['errors']}")
        print(f"Tiempo total: {duration:.2f}s")
        print("="*60 + "\n")


def main():
    """Función principal."""
    parser = argparse.ArgumentParser(
        description='Migrar base de datos de SQLite a PostgreSQL'
    )
    parser.add_argument(
        '--source',
        default='sqlite:///./agente_politico.db',
        help='URL de SQLite (default: sqlite:///./agente_politico.db)'
    )
    parser.add_argument(
        '--target',
        required=True,
        help='URL de PostgreSQL (ej: postgresql://user:pass@localhost/crm_politica)'
    )
    parser.add_argument(
        '--verify-only',
        action='store_true',
        help='Solo verificar, no migrar'
    )
    
    args = parser.parse_args()
    
    migrator = DatabaseMigrator(args.source, args.target)
    
    # Conectar
    if not migrator.connect():
        logger.error("No se pudo conectar a las bases de datos")
        sys.exit(1)
    
    if args.verify_only:
        logger.info("Modo verificación: comparando datos...")
        if migrator.verify_migration():
            logger.info("✅ Verificación exitosa")
            sys.exit(0)
        else:
            logger.error("❌ Verificación falló")
            sys.exit(1)
    
    # Crear esquema
    if not migrator.create_target_schema():
        logger.error("No se pudo crear el esquema")
        sys.exit(1)
    
    # Migrar datos
    logger.info("\n🚀 Iniciando migración de datos...\n")
    if not migrator.migrate_data():
        logger.error("❌ Migración falló")
        sys.exit(1)
    
    # Verificar
    if not migrator.verify_migration():
        logger.error("❌ Verificación falló después de migración")
        sys.exit(1)
    
    migrator.print_summary()
    logger.info("✅ Migración completada exitosamente")
    sys.exit(0)


if __name__ == '__main__':
    main()
