"""Agente LangGraph para análisis de conversaciones políticas."""
from typing import TypedDict, Annotated, List, Dict, Any
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
import json
from datetime import datetime
import os
from backend import config


class AgentState(TypedDict):
    """Estado del agente."""
    mensaje: str
    plataforma: str
    persona_id: int | None
    nombre_usuario: str | None # Nuevo campo
    datos_extraidos: Dict[str, Any]
    historial_conversacion: List[str]
    necesita_mas_info: bool
    error: str | None

# ... (inside AgenteExtraccionDatos)

class AgenteExtraccionDatos:
    """
    Agente LangGraph que analiza conversaciones y extrae información estructurada.
    
    El agente identifica:
    - Información personal (nombre, edad, género)
    - Intereses (categorizados)
    - Datos de contacto
    - Ocupación y ubicación
    """
    
    def __init__(self):
        """Inicializar el agente con el modelo de lenguaje."""
        self.llm = self._create_llm()
        
        # Construir el grafo
        self.graph = self._build_graph()
    
    def _create_llm(self):
        """Crear el modelo de lenguaje según la configuración disponible."""
        # Opción 1: Vertex AI con GCP Project (usa ADC - gcloud auth application-default login)
        if config.GCP_PROJECT_ID:
            # Usamos ChatVertexAI para autenticación via GCP/ADC
            # Nota: Hay un warning de deprecación pero la funcionalidad es correcta
            import warnings
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            from langchain_google_vertexai import ChatVertexAI
            
            print("[Vertex AI] Usando Vertex AI con ADC (Google CLI)")
            print(f"   Proyecto: {config.GCP_PROJECT_ID}")
            print(f"   Ubicacion: {config.GCP_LOCATION}")
            print(f"   Modelo: {config.GEMINI_MODEL}")
            
            # Si hay credenciales de service account, configurarlas
            if config.GOOGLE_APPLICATION_CREDENTIALS:
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.GOOGLE_APPLICATION_CREDENTIALS
                print("   Credenciales: Service Account")
            else:
                print("   Credenciales: Application Default Credentials (gcloud auth)")
            
            return ChatVertexAI(
                model=config.GEMINI_MODEL,
                project=config.GCP_PROJECT_ID,
                location=config.GCP_LOCATION,
                temperature=0.3,
            )
        
        # Opción 2: Google AI Studio con API Key (Free Tier)
        elif config.GOOGLE_API_KEY:
            from langchain_google_genai import ChatGoogleGenerativeAI
            
            print("[API Key] Usando Google AI Studio (Free Tier)")
            print(f"   Modelo: {config.GEMINI_MODEL}")
            
            return ChatGoogleGenerativeAI(
                model=config.GEMINI_MODEL,
                temperature=0.3,
                google_api_key=config.GOOGLE_API_KEY
            )
        
        else:
            raise ValueError(
                "[ERROR] No se encontraron credenciales de Google.\n"
                "Para usar Vertex AI con Google CLI:\n"
                "  1. Ejecuta: gcloud auth application-default login\n"
                "  2. Configura GCP_PROJECT_ID en tu archivo .env\n"
                "\nPara usar Google AI Studio (gratis):\n"
                "  1. Obten una API key en: https://aistudio.google.com/app/apikey\n"
                "  2. Configura GOOGLE_API_KEY en tu archivo .env"
            )
    
    def _build_graph(self) -> StateGraph:
        """Construir el grafo de estado del agente."""
        workflow = StateGraph(AgentState)
        
        # Añadir nodos
        workflow.add_node("analizar_mensaje", self._analizar_mensaje)
        workflow.add_node("extraer_datos", self._extraer_datos)
        workflow.add_node("validar_datos", self._validar_datos)
        
        # Definir el flujo
        workflow.set_entry_point("analizar_mensaje")
        workflow.add_edge("analizar_mensaje", "extraer_datos")
        workflow.add_edge("extraer_datos", "validar_datos")
        workflow.add_edge("validar_datos", END)
        
        return workflow.compile()
    
    def _analizar_mensaje(self, state: AgentState) -> AgentState:
        """Analizar el mensaje para determinar el contexto."""
        mensaje = state["mensaje"]
        plataforma = state.get("plataforma", "desconocida")
        
        system_prompt = """Eres un asistente político que analiza conversaciones con ciudadanos.
Tu objetivo es identificar si el mensaje contiene información relevante sobre la persona.

Determina si el mensaje contiene:
- Información personal (nombre, edad, género)
- Intereses o preocupaciones
- Datos de contacto
- Ubicación u ocupación

Responde con un breve análisis del contenido."""

        try:
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Plataforma: {plataforma}\nMensaje: {mensaje}")
            ])
            
            # Actualizar historial
            historial = state.get("historial_conversacion", [])
            historial.append(mensaje)
            state["historial_conversacion"] = historial
            
        except Exception as e:
            state["error"] = f"Error al analizar mensaje: {str(e)}"
        
        return state
    
    def _extraer_datos(self, state: AgentState) -> AgentState:
        """Extraer datos estructurados del mensaje."""
        mensaje = state["mensaje"]
        historial = state.get("historial_conversacion", [])
        nombre_usuario = state.get("nombre_usuario", "Desconocido")
        
        # Contexto del historial
        contexto_historial = "\n".join(historial[-5:]) if historial else mensaje
        
        system_prompt = f"""Eres un experto en extracción de información. Analiza la conversación y extrae datos estructurados.

CATEGORÍAS DE INTERESES DISPONIBLES:
{', '.join(config.CATEGORIAS_INTERES)}

GÉNEROS DISPONIBLES:
{', '.join(config.GENEROS)}

INSTRUCCIONES:
1. Extrae información EXPLÍCITAMENTE mencionada en el texto.
2. Si el GÉNERO no se menciona explícitamente, INFIÉRELO a partir del nombre de usuario: "{nombre_usuario}".
3. Si el nombre no es claro, déjalo como null o "No especificado".

Devuelve un JSON con esta estructura:
{{
    "nombre_completo": "nombre si se menciona, sino usar '{nombre_usuario}' si parece un nombre real",
    "edad": número si se menciona, sino null,
    "genero": "uno de los géneros disponibles",
    "telefono": "si se menciona, sino null",
    "email": "si se menciona, sino null",
    "ocupacion": "si se menciona, sino null",
    "ubicacion": "si se menciona, sino null",
    "intereses": ["lista de categorías que coincidan con las preocupaciones mencionadas"],
    "resumen_conversacional": "un resumen breve (max 100 caracteres) de lo que trata la conversación actual",
    "otros_datos": {{"clave": "valor para cualquier información adicional relevante"}},
    "confianza": "alta/media/baja según qué tan explícita es la información"
}}"""

        try:
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Conversación:\n{contexto_historial}")
            ])
            
            # Parsear la respuesta JSON
            response_text = response.content
            
            # Extraer JSON de la respuesta
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            datos = json.loads(response_text)
            state["datos_extraidos"] = datos
            
        except json.JSONDecodeError as e:
            state["error"] = f"Error al parsear JSON: {str(e)}"
            state["datos_extraidos"] = {}
        except Exception as e:
            state["error"] = f"Error al extraer datos: {str(e)}"
            state["datos_extraidos"] = {}
        
        return state
    
    def _validar_datos(self, state: AgentState) -> AgentState:
        """Validar y limpiar los datos extraídos."""
        datos = state.get("datos_extraidos", {})
        
        # Validar categorías de intereses
        if "intereses" in datos and datos["intereses"]:
            intereses_validos = [
                i for i in datos["intereses"] 
                if i in config.CATEGORIAS_INTERES
            ]
            datos["intereses"] = intereses_validos
        
        # Validar género
        if "genero" in datos and datos["genero"]:
            if datos["genero"] not in config.GENEROS:
                datos["genero"] = "No especificado"
        
        # Validar edad
        if "edad" in datos and datos["edad"]:
            try:
                edad = int(datos["edad"])
                if edad < 0 or edad > 120:
                    datos["edad"] = None
            except (ValueError, TypeError):
                datos["edad"] = None
        
        # Determinar si necesita más información
        campos_importantes = ["nombre_completo", "intereses", "edad", "genero"]
        campos_presentes = sum(1 for campo in campos_importantes if datos.get(campo))
        
        state["necesita_mas_info"] = campos_presentes < 2
        state["datos_extraidos"] = datos
        
        return state
    
    def procesar_mensaje(
        self, 
        mensaje: str, 
        plataforma: str = "desconocida",
        persona_id: int = None,
        historial: List[str] = None,
        nombre_usuario: str = None
    ) -> Dict[str, Any]:
        """
        Procesar un mensaje y extraer información estructurada.
        
        Args:
            mensaje: Texto del mensaje a analizar
            plataforma: Plataforma de origen (facebook/instagram)
            persona_id: ID de la persona si ya existe
            historial: Historial de mensajes previos
            nombre_usuario: Nombre de usuario para inferencia
            
        Returns:
            Diccionario con los datos extraídos y metadatos
        """
        initial_state = AgentState(
            mensaje=mensaje,
            plataforma=plataforma,
            persona_id=persona_id,
            nombre_usuario=nombre_usuario,
            datos_extraidos={},
            historial_conversacion=historial or [],
            necesita_mas_info=False,
            error=None
        )
        
        # Ejecutar el grafo
        result = self.graph.invoke(initial_state)
        
        return {
            "datos_extraidos": result.get("datos_extraidos", {}),
            "necesita_mas_info": result.get("necesita_mas_info", False),
            "error": result.get("error"),
            "fecha_procesamiento": datetime.utcnow().isoformat()
        }


# Instancia global del agente
agente = AgenteExtraccionDatos()


def procesar_conversacion(
    mensaje: str,
    plataforma: str = "desconocida",
    persona_id: int = None,
    historial: List[str] = None,
    nombre_usuario: str = None
) -> Dict[str, Any]:
    """
    Función auxiliar para procesar una conversación.
    
    Args:
        mensaje: Texto del mensaje
        plataforma: Plataforma de origen
        persona_id: ID de la persona
        historial: Historial de conversación
        nombre_usuario: Nombre de usuario
        
    Returns:
        Datos extraídos
    """
    return agente.procesar_mensaje(mensaje, plataforma, persona_id, historial, nombre_usuario)
