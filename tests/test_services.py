#!/usr/bin/env python3
"""
Tests unitarios para cada servicio del CRM Política.
Usa SQLite en memoria para aislamiento.
"""
import sys
import os
import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from backend.database.models import Base, Persona, Interes, Conversacion, Analisis, Evento, Candidato, UsuarioAutorizado
from backend.database.services import PersonaService, ConversacionService, AnalisisService


# ==================== FIXTURES ====================

@pytest.fixture
def engine():
    """Crear engine SQLite en memoria."""
    eng = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(eng)
    return eng


@pytest.fixture
def session(engine):
    """Crear sesión de test."""
    Session = sessionmaker(bind=engine)
    sess = Session()
    
    # Crear intereses predeterminados
    for cat in ["Deportes", "Inversión", "Seguridad", "Salud", "Educación"]:
        sess.add(Interes(categoria=cat))
    sess.commit()
    
    yield sess
    sess.close()


# ==================== TEST PERSONA SERVICE ====================

class TestPersonaService:
    """Tests unitarios para PersonaService."""

    def test_crear_persona_con_facebook_id(self, session):
        """Crear persona nueva con facebook_id."""
        datos = {
            "nombre_completo": "Juan Pérez",
            "edad": 35,
            "genero": "Masculino",
            "telefono": "+56912345678",
            "email": "juan@email.com",
            "ocupacion": "Ingeniero",
            "ubicacion": "Santiago"
        }
        persona = PersonaService.crear_o_actualizar_persona(
            session, datos, facebook_id="fb_001"
        )
        assert persona.id is not None
        assert persona.nombre_completo == "Juan Pérez"
        assert persona.edad == 35
        assert persona.facebook_id == "fb_001"
        assert persona.ubicacion == "Santiago"
        print(f"  ✅ Persona creada: id={persona.id}, nombre={persona.nombre_completo}")

    def test_crear_persona_con_instagram_id(self, session):
        """Crear persona nueva con instagram_id."""
        datos = {"nombre_completo": "María García", "edad": 28}
        persona = PersonaService.crear_o_actualizar_persona(
            session, datos, instagram_id="ig_001"
        )
        assert persona.instagram_id == "ig_001"
        assert persona.nombre_completo == "María García"
        print(f"  ✅ Persona Instagram: id={persona.id}")

    def test_actualizar_persona_existente(self, session):
        """Actualizar datos de persona existente por facebook_id."""
        datos1 = {"nombre_completo": "Pedro López", "edad": 40}
        persona1 = PersonaService.crear_o_actualizar_persona(
            session, datos1, facebook_id="fb_002"
        )
        
        datos2 = {"nombre_completo": "Pedro López Actualizado", "ocupacion": "Doctor"}
        persona2 = PersonaService.crear_o_actualizar_persona(
            session, datos2, facebook_id="fb_002"
        )
        
        assert persona1.id == persona2.id
        assert persona2.nombre_completo == "Pedro López Actualizado"
        assert persona2.ocupacion == "Doctor"
        print(f"  ✅ Persona actualizada: {persona2.nombre_completo}")

    def test_asignar_intereses(self, session):
        """Asignar intereses a una persona."""
        datos = {
            "nombre_completo": "Ana Ruiz",
            "intereses": ["Deportes", "Salud"]
        }
        persona = PersonaService.crear_o_actualizar_persona(
            session, datos, facebook_id="fb_003"
        )
        
        intereses = [i.categoria for i in persona.intereses]
        assert "Deportes" in intereses
        assert "Salud" in intereses
        assert len(intereses) == 2
        print(f"  ✅ Intereses asignados: {intereses}")

    def test_obtener_persona_por_id(self, session):
        """Obtener persona por ID."""
        datos = {"nombre_completo": "Carlos Test"}
        persona = PersonaService.crear_o_actualizar_persona(
            session, datos, facebook_id="fb_004"
        )
        
        encontrada = PersonaService.obtener_persona_por_id(session, persona.id)
        assert encontrada is not None
        assert encontrada.nombre_completo == "Carlos Test"
        print(f"  ✅ Persona encontrada por id={persona.id}")

    def test_obtener_persona_inexistente(self, session):
        """Obtener persona que no existe devuelve None."""
        result = PersonaService.obtener_persona_por_id(session, 99999)
        assert result is None
        print(f"  ✅ Persona inexistente retorna None")

    def test_listar_todas(self, session):
        """Listar todas las personas."""
        for i in range(5):
            PersonaService.crear_o_actualizar_persona(
                session, {"nombre_completo": f"Persona {i}"}, facebook_id=f"fb_list_{i}"
            )
        
        personas = PersonaService.listar_todas(session)
        assert len(personas) == 5
        print(f"  ✅ Listado: {len(personas)} personas")

    def test_buscar_por_genero(self, session):
        """Buscar personas por género."""
        PersonaService.crear_o_actualizar_persona(
            session, {"nombre_completo": "Hombre 1", "genero": "Masculino"}, facebook_id="fb_g1"
        )
        PersonaService.crear_o_actualizar_persona(
            session, {"nombre_completo": "Mujer 1", "genero": "Femenino"}, facebook_id="fb_g2"
        )
        
        hombres = PersonaService.buscar_personas(session, genero="Masculino")
        assert len(hombres) == 1
        assert hombres[0].nombre_completo == "Hombre 1"
        print(f"  ✅ Búsqueda por género: {len(hombres)} resultado(s)")

    def test_buscar_por_edad(self, session):
        """Buscar personas por rango de edad."""
        PersonaService.crear_o_actualizar_persona(
            session, {"nombre_completo": "Joven", "edad": 25}, facebook_id="fb_age1"
        )
        PersonaService.crear_o_actualizar_persona(
            session, {"nombre_completo": "Mayor", "edad": 60}, facebook_id="fb_age2"
        )
        
        jovenes = PersonaService.buscar_personas(session, edad_min=20, edad_max=30)
        assert len(jovenes) == 1
        assert jovenes[0].nombre_completo == "Joven"
        print(f"  ✅ Búsqueda por edad: {len(jovenes)} resultado(s)")


# ==================== TEST CONVERSACION SERVICE ====================

class TestConversacionService:
    """Tests unitarios para ConversacionService."""

    def _crear_persona(self, session):
        """Helper: crear persona para tests."""
        datos = {"nombre_completo": "Test Conv"}
        return PersonaService.crear_o_actualizar_persona(
            session, datos, facebook_id=f"fb_conv_{datetime.now().timestamp()}"
        )

    def test_guardar_conversacion(self, session):
        """Guardar una conversación nueva."""
        persona = self._crear_persona(session)
        conv = ConversacionService.guardar_conversacion(
            session,
            persona_id=persona.id,
            mensaje="Hola, me interesa el proyecto",
            plataforma="facebook",
            conversacion_id="conv_001"
        )
        assert conv.id is not None
        assert conv.mensaje == "Hola, me interesa el proyecto"
        assert conv.plataforma == "facebook"
        assert conv.es_enviado == 0
        print(f"  ✅ Conversación guardada: id={conv.id}")

    def test_guardar_conversacion_enviada(self, session):
        """Guardar conversación enviada (es_enviado=True)."""
        persona = self._crear_persona(session)
        conv = ConversacionService.guardar_conversacion(
            session,
            persona_id=persona.id,
            mensaje="Gracias por tu interés",
            plataforma="instagram",
            es_enviado=True
        )
        assert conv.es_enviado == 1
        print(f"  ✅ Conversación enviada: es_enviado={conv.es_enviado}")

    def test_evitar_duplicados(self, session):
        """No duplicar conversaciones con mismo conversacion_id."""
        persona = self._crear_persona(session)
        conv1 = ConversacionService.guardar_conversacion(
            session, persona.id, "Mensaje original", "facebook", conversacion_id="dup_001"
        )
        conv2 = ConversacionService.guardar_conversacion(
            session, persona.id, "Mensaje duplicado", "facebook", conversacion_id="dup_001"
        )
        assert conv1.id == conv2.id
        assert conv2.mensaje == "Mensaje original"
        print(f"  ✅ Duplicado evitado: ambas retornan id={conv1.id}")

    def test_obtener_historial(self, session):
        """Obtener historial de conversaciones ordenado."""
        persona = self._crear_persona(session)
        for i in range(5):
            ConversacionService.guardar_conversacion(
                session, persona.id, f"Mensaje {i}", "facebook",
                fecha_mensaje=datetime.utcnow() - timedelta(hours=5 - i)
            )
        
        historial = ConversacionService.obtener_historial(session, persona.id)
        assert len(historial) == 5
        # Verificar orden descendente
        assert "Mensaje 4" in historial[0].mensaje
        print(f"  ✅ Historial: {len(historial)} mensajes, orden correcto")

    def test_historial_con_limit(self, session):
        """Limitar cantidad de mensajes en historial."""
        persona = self._crear_persona(session)
        for i in range(10):
            ConversacionService.guardar_conversacion(
                session, persona.id, f"Msg {i}", "facebook"
            )
        
        historial = ConversacionService.obtener_historial(session, persona.id, limit=3)
        assert len(historial) == 3
        print(f"  ✅ Historial limitado: {len(historial)} de 10")


# ==================== TEST ANALISIS SERVICE ====================

class TestAnalisisService:
    """Tests unitarios para AnalisisService."""

    def _crear_persona(self, session):
        """Helper: crear persona para tests."""
        datos = {"nombre_completo": "Test Analisis"}
        return PersonaService.crear_o_actualizar_persona(
            session, datos, facebook_id=f"fb_anal_{datetime.now().timestamp()}"
        )

    def test_crear_analisis(self, session):
        """Crear un análisis nuevo."""
        persona = self._crear_persona(session)
        analisis = AnalisisService.crear_analisis(
            session,
            persona_id=persona.id,
            resumen="Persona interesada en seguridad pública",
            contenido_completo="Conversación completa...",
            categorias=["Seguridad", "Educación"]
        )
        assert analisis.id is not None
        assert analisis.resumen == "Persona interesada en seguridad pública"
        assert "Seguridad" in analisis.categorias
        print(f"  ✅ Análisis creado: id={analisis.id}")

    def test_evitar_duplicado_por_start_conversation(self, session):
        """No duplicar análisis para la misma sesión (mismo start_conversation)."""
        persona = self._crear_persona(session)
        start = datetime.utcnow()
        
        a1 = AnalisisService.crear_analisis(
            session, persona.id, "Resumen 1", "Contenido 1",
            start_conversation=start
        )
        a2 = AnalisisService.crear_analisis(
            session, persona.id, "Resumen 2", "Contenido 2",
            start_conversation=start + timedelta(seconds=30)
        )
        assert a1.id == a2.id
        print(f"  ✅ Duplicado evitado: ambas retornan id={a1.id}")

    def test_buscar_analisis_por_persona(self, session):
        """Buscar análisis de una persona específica."""
        persona = self._crear_persona(session)
        for i in range(3):
            AnalisisService.crear_analisis(
                session, persona.id, f"Resumen {i}", f"Contenido {i}",
                start_conversation=datetime.utcnow() - timedelta(hours=i+1)
            )
        
        resultados = AnalisisService.buscar_analisis(session, persona_id=persona.id)
        assert len(resultados) == 3
        print(f"  ✅ Búsqueda: {len(resultados)} análisis encontrados")

    def test_buscar_analisis_por_fecha(self, session):
        """Buscar análisis por rango de fechas."""
        persona = self._crear_persona(session)
        
        # Análisis de ayer
        AnalisisService.crear_analisis(
            session, persona.id, "Ayer", "...",
            start_conversation=datetime.utcnow() - timedelta(days=1, hours=1)
        )
        # Análisis de hoy
        AnalisisService.crear_analisis(
            session, persona.id, "Hoy", "...",
            start_conversation=datetime.utcnow() - timedelta(hours=1)
        )
        
        # Buscar solo de hoy
        desde = datetime.utcnow() - timedelta(hours=12)
        resultados = AnalisisService.buscar_analisis(session, fecha_inicio=desde)
        assert len(resultados) >= 1
        assert any("Hoy" in r.resumen for r in resultados)
        print(f"  ✅ Búsqueda por fecha: {len(resultados)} resultado(s)")


# ==================== TEST MODELOS DIRECTOS ====================

class TestModelos:
    """Tests unitarios para modelos SQLAlchemy directos."""

    def test_crear_candidato(self, session):
        """Crear candidato."""
        candidato = Candidato(
            nombre="Candidato Test",
            email="candidato@test.com",
            partido="Partido Test",
            cargo="Alcalde"
        )
        session.add(candidato)
        session.commit()
        
        assert candidato.id is not None
        assert candidato.estado == "activo"
        print(f"  ✅ Candidato: id={candidato.id}, nombre={candidato.nombre}")

    def test_crear_evento(self, session):
        """Crear evento."""
        evento = Evento(
            nombre="Evento Test",
            descripcion="Descripción del evento"
        )
        session.add(evento)
        session.commit()
        
        assert evento.id is not None
        assert evento.nombre == "Evento Test"
        print(f"  ✅ Evento: id={evento.id}, nombre={evento.nombre}")

    def test_crear_usuario_autorizado(self, session):
        """Crear usuario autorizado."""
        usuario = UsuarioAutorizado(
            email="admin@test.com",
            nombre="Admin Test",
            rol="admin"
        )
        session.add(usuario)
        session.commit()
        
        assert usuario.id is not None
        assert usuario.rol == "admin"
        assert usuario.activo == 1
        print(f"  ✅ Usuario: id={usuario.id}, rol={usuario.rol}")

    def test_relacion_candidato_persona(self, session):
        """Verificar relación candidato ↔ persona."""
        candidato = Candidato(nombre="Cand", email="cand@test.com")
        session.add(candidato)
        session.commit()
        
        persona = Persona(
            nombre_completo="Persona de Cand",
            candidato_id=candidato.id
        )
        session.add(persona)
        session.commit()
        
        assert persona.candidato.nombre == "Cand"
        assert len(candidato.personas) == 1
        print(f"  ✅ Relación candidato-persona OK")

    def test_relacion_persona_conversacion(self, session):
        """Verificar relación persona ↔ conversación (cascade delete)."""
        persona = Persona(nombre_completo="Cascade Test")
        session.add(persona)
        session.commit()
        
        conv = Conversacion(
            persona_id=persona.id,
            mensaje="Test cascade",
            plataforma="facebook"
        )
        session.add(conv)
        session.commit()
        
        assert len(persona.conversaciones) == 1
        
        # Borrar persona debería borrar conversaciones (cascade)
        session.delete(persona)
        session.commit()
        
        remaining = session.query(Conversacion).filter_by(persona_id=persona.id).count()
        assert remaining == 0
        print(f"  ✅ Cascade delete OK (persona → conversaciones)")

    def test_relacion_analisis_evento(self, session):
        """Verificar relación análisis ↔ evento."""
        persona = Persona(nombre_completo="Rel Test")
        session.add(persona)
        session.commit()
        
        evento = Evento(nombre="Evento Rel")
        session.add(evento)
        session.commit()
        
        analisis = Analisis(
            persona_id=persona.id,
            resumen="Test relación",
            evento_id=evento.id
        )
        session.add(analisis)
        session.commit()
        
        assert analisis.evento.nombre == "Evento Rel"
        assert len(evento.analisis) == 1
        print(f"  ✅ Relación análisis-evento OK")


# ==================== TEST INTEGRACIÓN COMPLETO ====================

class TestIntegracion:
    """Test de integración: flujo completo del CRM."""

    def test_flujo_completo(self, session):
        """
        Flujo completo:
        1. Crear candidato
        2. Crear persona vinculada al candidato
        3. Guardar conversaciones
        4. Crear análisis
        5. Crear evento y asociar análisis
        6. Verificar relaciones y datos
        """
        print("\n" + "="*60)
        print("🧪 TEST DE INTEGRACIÓN - FLUJO COMPLETO")
        print("="*60)
        
        # --- PASO 1: Crear candidato ---
        candidato = Candidato(
            nombre="María Rodríguez",
            email="maria@partido.cl",
            partido="Partido Ciudadano",
            cargo="Alcaldesa de Providencia"
        )
        session.add(candidato)
        session.commit()
        assert candidato.id is not None
        print(f"\n✅ Paso 1: Candidato creado - {candidato.nombre} (id={candidato.id})")
        
        # --- PASO 2: Crear persona vinculada ---
        datos_persona = {
            "nombre_completo": "Roberto Sánchez",
            "edad": 45,
            "genero": "Masculino",
            "telefono": "+56987654321",
            "email": "roberto@email.com",
            "ocupacion": "Profesor",
            "ubicacion": "Providencia",
            "intereses": ["Educación", "Seguridad"]
        }
        persona = PersonaService.crear_o_actualizar_persona(
            session, datos_persona, facebook_id="fb_integ_001"
        )
        persona.candidato_id = candidato.id
        session.commit()
        session.refresh(persona)
        
        assert persona.id is not None
        assert persona.candidato_id == candidato.id
        assert len(persona.intereses) == 2
        print(f"✅ Paso 2: Persona creada - {persona.nombre_completo} (id={persona.id})")
        print(f"   Intereses: {[i.categoria for i in persona.intereses]}")
        print(f"   Candidato: {persona.candidato.nombre}")
        
        # --- PASO 3: Guardar conversaciones ---
        mensajes = [
            ("Hola, me gustaría saber sobre el plan de seguridad", False),
            ("Claro Roberto, nuestro plan incluye más iluminación y cámaras", True),
            ("¿Y qué hay sobre educación? Soy profesor", False),
            ("Tenemos un programa de mejora salarial para docentes", True),
            ("Excelente, me interesa colaborar", False)
        ]
        
        conversaciones = []
        for i, (msg, enviado) in enumerate(mensajes):
            conv = ConversacionService.guardar_conversacion(
                session,
                persona_id=persona.id,
                mensaje=msg,
                plataforma="facebook",
                es_enviado=enviado,
                conversacion_id=f"conv_integ_{i}",
                fecha_mensaje=datetime.utcnow() - timedelta(minutes=len(mensajes) - i)
            )
            conversaciones.append(conv)
        
        assert len(conversaciones) == 5
        print(f"✅ Paso 3: {len(conversaciones)} conversaciones guardadas")
        
        # --- PASO 4: Crear análisis ---
        contenido = "\n".join([m[0] for m in mensajes])
        analisis = AnalisisService.crear_analisis(
            session,
            persona_id=persona.id,
            resumen="Ciudadano interesado en seguridad y educación. Profesor dispuesto a colaborar.",
            contenido_completo=contenido,
            categorias=["Seguridad", "Educación"],
            start_conversation=conversaciones[0].fecha_mensaje
        )
        
        assert analisis.id is not None
        assert "seguridad" in analisis.resumen.lower()
        print(f"✅ Paso 4: Análisis creado - id={analisis.id}")
        print(f"   Resumen: {analisis.resumen[:60]}...")
        
        # --- PASO 5: Crear evento y asociar ---
        evento = Evento(
            nombre="Campaña Providencia 2026",
            descripcion="Campaña electoral para alcaldía"
        )
        session.add(evento)
        session.commit()
        
        analisis.evento_id = evento.id
        session.commit()
        session.refresh(analisis)
        
        assert analisis.evento.nombre == "Campaña Providencia 2026"
        print(f"✅ Paso 5: Evento '{evento.nombre}' asociado al análisis")
        
        # --- PASO 6: Verificación final ---
        print(f"\n{'='*60}")
        print(f"📊 VERIFICACIÓN FINAL")
        print(f"{'='*60}")
        
        # Verificar candidato tiene personas
        session.refresh(candidato)
        assert len(candidato.personas) == 1
        print(f"✅ Candidato '{candidato.nombre}' tiene {len(candidato.personas)} persona(s)")
        
        # Verificar historial de conversaciones
        historial = ConversacionService.obtener_historial(session, persona.id)
        assert len(historial) == 5
        print(f"✅ Persona '{persona.nombre_completo}' tiene {len(historial)} conversaciones")
        
        # Verificar análisis de la persona
        analisis_list = AnalisisService.buscar_analisis(session, persona_id=persona.id)
        assert len(analisis_list) >= 1
        print(f"✅ Persona tiene {len(analisis_list)} análisis")
        
        # Verificar evento tiene análisis
        session.refresh(evento)
        assert len(evento.analisis) == 1
        print(f"✅ Evento '{evento.nombre}' tiene {len(evento.analisis)} análisis")
        
        # Verificar no duplicados
        conv_dup = ConversacionService.guardar_conversacion(
            session, persona.id, "Duplicado", "facebook", conversacion_id="conv_integ_0"
        )
        assert conv_dup.id == conversaciones[0].id
        print(f"✅ Protección anti-duplicados funciona")
        
        # Resumen total
        total_personas = session.query(Persona).count()
        total_conv = session.query(Conversacion).count()
        total_analisis = session.query(Analisis).count()
        total_eventos = session.query(Evento).count()
        
        print(f"\n{'='*60}")
        print(f"📈 RESUMEN DE DATOS")
        print(f"{'='*60}")
        print(f"  Candidatos:     {session.query(Candidato).count()}")
        print(f"  Personas:       {total_personas}")
        print(f"  Conversaciones: {total_conv}")
        print(f"  Análisis:       {total_analisis}")
        print(f"  Eventos:        {total_eventos}")
        print(f"  Intereses:      {session.query(Interes).count()}")
        print(f"{'='*60}")
        print(f"✅ TEST DE INTEGRACIÓN COMPLETADO EXITOSAMENTE")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
