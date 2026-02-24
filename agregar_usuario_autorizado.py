"""
Script para agregar usuarios a la lista blanca de acceso.
Solo los usuarios agregados aquí podrán acceder a la app en producción.

Uso:
    python agregar_usuario_autorizado.py
"""

import os
import sys
from datetime import datetime

# Agregar el directorio raíz al path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# Importar directamente desde database para acceso a SQLAlchemy
try:
    from backend.database.storage import SessionLocal, init_db
except ImportError:
    # Fallback: importar directamente desde database.__init__
    from backend.database import SessionLocal, init_db

from backend.database.models import UsuarioAutorizado

def agregar_usuario(email: str, nombre: str, rol: str = "candidato"):
    """
    Agrega un usuario a la lista blanca.
    
    Args:
        email: Email del usuario (debe coincidir con su cuenta de Facebook)
        nombre: Nombre completo del usuario
        rol: Rol del usuario ('candidato', 'admin', 'equipo')
    """
    db = SessionLocal()
    
    try:
        # Verificar si ya existe
        existe = db.query(UsuarioAutorizado).filter(
            UsuarioAutorizado.email == email
        ).first()
        
        if existe:
            print(f"❌ El usuario {email} ya está registrado")
            if existe.activo == 0:
                print(f"   (Usuario está INACTIVO. ¿Deseas reactivarlo?)")
            return False
        
        # Crear nuevo usuario
        nuevo_usuario = UsuarioAutorizado(
            email=email,
            nombre=nombre,
            rol=rol,
            activo=1,
            fecha_registro=datetime.utcnow()
        )
        
        db.add(nuevo_usuario)
        db.commit()
        
        print(f"✅ Usuario agregado exitosamente:")
        print(f"   Nombre: {nombre}")
        print(f"   Email: {email}")
        print(f"   Rol: {rol}")
        print(f"   Estado: Activo")
        
        return True
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error al agregar usuario: {e}")
        return False
        
    finally:
        db.close()


def listar_usuarios():
    """Lista todos los usuarios autorizados."""
    db = SessionLocal()
    
    try:
        usuarios = db.query(UsuarioAutorizado).all()
        
        if not usuarios:
            print("\n📋 No hay usuarios autorizados registrados.\n")
            return
        
        print(f"\n📋 USUARIOS AUTORIZADOS ({len(usuarios)} total):")
        print("=" * 80)
        print(f"{'ID':<5} {'Nombre':<25} {'Email':<35} {'Rol':<12} {'Estado':<8}")
        print("-" * 80)
        
        for usuario in usuarios:
            estado = "✅ Activo" if usuario.activo == 1 else "❌ Inactivo"
            print(f"{usuario.id:<5} {usuario.nombre:<25} {usuario.email:<35} {usuario.rol:<12} {estado:<8}")
        
        print("=" * 80)
        print()
        
    except Exception as e:
        print(f"❌ Error al listar usuarios: {e}")
        
    finally:
        db.close()


def desactivar_usuario(email: str):
    """Desactiva un usuario (no elimina, solo lo desactiva)."""
    db = SessionLocal()
    
    try:
        usuario = db.query(UsuarioAutorizado).filter(
            UsuarioAutorizado.email == email
        ).first()
        
        if not usuario:
            print(f"❌ Usuario {email} no encontrado")
            return False
        
        usuario.activo = 0
        db.commit()
        
        print(f"✅ Usuario {email} desactivado exitosamente")
        return True
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error al desactivar usuario: {e}")
        return False
        
    finally:
        db.close()


def reactivar_usuario(email: str):
    """Reactiva un usuario desactivado."""
    db = SessionLocal()
    
    try:
        usuario = db.query(UsuarioAutorizado).filter(
            UsuarioAutorizado.email == email
        ).first()
        
        if not usuario:
            print(f"❌ Usuario {email} no encontrado")
            return False
        
        usuario.activo = 1
        db.commit()
        
        print(f"✅ Usuario {email} reactivado exitosamente")
        return True
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error al reactivar usuario: {e}")
        return False
        
    finally:
        db.close()


def menu_interactivo():
    """Menú interactivo para gestionar usuarios."""
    print("\n" + "=" * 60)
    print("🔐 GESTIÓN DE USUARIOS AUTORIZADOS - CRM POLÍTICO")
    print("=" * 60)
    
    while True:
        print("\n¿Qué deseas hacer?")
        print("1. Agregar nuevo usuario")
        print("2. Listar usuarios")
        print("3. Desactivar usuario")
        print("4. Reactivar usuario")
        print("5. Salir")
        
        opcion = input("\nOpción (1-5): ").strip()
        
        if opcion == "1":
            print("\n--- AGREGAR NUEVO USUARIO ---")
            nombre = input("Nombre completo: ").strip()
            email = input("Email (debe coincidir con Facebook): ").strip().lower()
            
            print("\nRoles disponibles:")
            print("  - candidato: Usuario candidato (acceso normal)")
            print("  - admin: Administrador (acceso completo)")
            print("  - equipo: Miembro del equipo")
            
            rol = input("Rol (candidato/admin/equipo) [candidato]: ").strip().lower()
            if not rol:
                rol = "candidato"
            
            if rol not in ["candidato", "admin", "equipo"]:
                print("❌ Rol inválido. Debe ser: candidato, admin o equipo")
                continue
            
            # Confirmar
            print(f"\n📝 Resumen:")
            print(f"   Nombre: {nombre}")
            print(f"   Email: {email}")
            print(f"   Rol: {rol}")
            
            confirmar = input("\n¿Confirmar? (s/n): ").strip().lower()
            if confirmar == "s":
                agregar_usuario(email, nombre, rol)
        
        elif opcion == "2":
            listar_usuarios()
        
        elif opcion == "3":
            print("\n--- DESACTIVAR USUARIO ---")
            email = input("Email del usuario a desactivar: ").strip().lower()
            confirmar = input(f"¿Seguro que deseas desactivar {email}? (s/n): ").strip().lower()
            if confirmar == "s":
                desactivar_usuario(email)
        
        elif opcion == "4":
            print("\n--- REACTIVAR USUARIO ---")
            email = input("Email del usuario a reactivar: ").strip().lower()
            reactivar_usuario(email)
        
        elif opcion == "5":
            print("\n👋 ¡Hasta luego!")
            break
        
        else:
            print("❌ Opción inválida")


if __name__ == "__main__":
    # Inicializar base de datos (crea tablas si no existen)
    print("🔧 Inicializando base de datos...")
    init_db()
    
    # Si se pasan argumentos, agregar usuario directamente
    if len(sys.argv) == 4:
        # Uso: python agregar_usuario_autorizado.py "email" "nombre" "rol"
        email = sys.argv[1]
        nombre = sys.argv[2]
        rol = sys.argv[3]
        
        agregar_usuario(email, nombre, rol)
    
    elif len(sys.argv) == 3:
        # Uso: python agregar_usuario_autorizado.py "email" "nombre"
        email = sys.argv[1]
        nombre = sys.argv[2]
        
        agregar_usuario(email, nombre, "candidato")
    
    else:
        # Modo interactivo
        menu_interactivo()
