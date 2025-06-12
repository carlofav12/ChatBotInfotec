# filepath: backend/app/chatbot/services/intent_classifier.py
"""
Clasificador de intenciones usando IA para determinar el tipo de consulta del usuario
"""
import logging
import google.generativeai as genai
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class IntentClassifier:
    """Clasificador de intenciones usando Gemini AI"""
    
    def __init__(self, api_key: str):
        """Inicializar el clasificador con la API key"""
        self.api_key = api_key
        self.model = None
        self._initialize_model()
        
    def _initialize_model(self):
        """Inicializar el modelo de Gemini"""
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            logger.info("Clasificador de intenciones inicializado correctamente")
        except Exception as e:
            logger.error(f"Error inicializando clasificador: {e}")
            self.model = None
    
    def classify_intent(self, message: str, conversation_history: Optional[list] = None) -> Dict[str, Any]:
        """
        Clasificar la intención del mensaje del usuario
        
        Returns:
        {
            "intent": str,  # Tipo de intención detectada
            "confidence": float,  # Confianza en la clasificación (0-1)
            "entities": dict,  # Entidades extraídas
            "should_show_products": bool  # Si debe mostrar productos
        }
        """
        if not self.model:
            return self._fallback_classification(message, conversation_history)
        
        try:
            prompt = self._build_classification_prompt(message, conversation_history)
            response = self.model.generate_content(prompt)
            
            # Parsear la respuesta de Gemini
            return self._parse_classification_response(response.text, message, conversation_history)
            
        except Exception as e:
            logger.error(f"Error en clasificación de intención: {e}")
            return self._fallback_classification(message, conversation_history)
    
    def _build_classification_prompt(self, message: str, conversation_history: Optional[list] = None) -> str:
        """Construir prompt para clasificación de intenciones"""
        
        context = ""
        if conversation_history:
            # Tomar últimos 3 mensajes para contexto
            recent = conversation_history[-3:] if len(conversation_history) > 3 else conversation_history
            context_parts = []
            for msg in recent:
                if msg.get("user_message"):
                    context_parts.append(f"Usuario: {msg['user_message']}")
                if msg.get("bot_response"):
                    # Solo primeras 100 chars de la respuesta del bot
                    bot_msg = msg["bot_response"][:100] + "..." if len(msg["bot_response"]) > 100 else msg["bot_response"]
                    context_parts.append(f"Bot: {bot_msg}")
            context = "\n".join(context_parts)
        prompt = f"""
Eres un clasificador de intenciones para un chatbot de venta de productos tecnológicos (GRUPO INFOTEC).

MENSAJE DEL USUARIO: "{message}"

CONTEXTO PREVIO:
{context if context else "Sin contexto previo"}

INSTRUCCIONES:
Analiza el mensaje y clasifícalo en UNA de estas categorías:

1. **pregunta_tecnologica**: Preguntas generales sobre tecnología, comparaciones teóricas entre marcas/componentes, diferencias técnicas SIN mencionar productos específicos del catálogo
   - Ejemplos: "qué es mejor AMD o Intel", "diferencia entre SSD y HDD", "cuál procesador es mejor"
   - NO incluye: preguntas sobre productos específicos de la tienda

2. **buscar_producto**: Búsqueda de productos del catálogo, solicitudes de recomendaciones, preguntas sobre "el mejor producto que tienes"
   - Ejemplos: "busco una laptop", "cuál es la mejor laptop que tienes", "recomiéndame una PC", "qué laptops HP tienen"
   - Incluye: cualquier pregunta sobre productos específicos de la tienda

3. **comparar_productos**: Comparación entre productos específicos del catálogo mencionados por nombre
   - Ejemplos: "compara laptop Dell XPS vs HP Spectre", "diferencias entre estas dos PCs específicas"

4. **ver_especificaciones**: Solicitud de especificaciones técnicas de un producto específico mencionado
   - Ejemplos: "especificaciones del modelo Lenovo V15", "detalles técnicos de esta laptop"
   - Incluye: cualquier solicitud para ver especificaciones de un producto previamente listado como "la segunda" o "el número 2"

5. **agregar_carrito**: Intención explícita de comprar o agregar productos al carrito
   - Ejemplos: "quiero comprar este", "agrega al carrito", "lo llevo"

6. **conversacion_general**: Saludos, despedidas, agradecimientos, consultas generales no técnicas
   - Ejemplos: "hola", "gracias", "cómo estás", "información de la empresa"

RESPONDE EXACTAMENTE en este formato JSON:
{{
  "intent": "categoria_detectada",
  "confidence": 0.95,
  "reasoning": "breve explicación de por qué se clasificó así",
  "should_show_products": true,
  "extracted_entities": {{
    "brands": ["marca1", "marca2"],
    "products": ["producto1"],
    "components": ["componente1"]
  }}
}}

IMPORTANTE:
- Para preguntas como "qué es mejor X o Y" donde X,Y son marcas/componentes → "pregunta_tecnologica"
- Para "busco/quiero/necesito + producto" → "buscar_producto"  
- Para "cuál es la mejor laptop que tienes" → "buscar_producto"
- Para "cuáles son las especificaciones de la segunda" → "ver_especificaciones"
- Para referencias como "la segunda", "el número 2", etc. → "ver_especificaciones"
- Confidence: 0.9+ para casos claros, 0.7-0.9 para casos moderados, <0.7 para casos ambiguos
- should_show_products: false para pregunta_tecnologica y conversacion_general
"""
        
        return prompt
    
    def _parse_classification_response(self, response_text: str, original_message: str, conversation_history: Optional[list] = None) -> Dict[str, Any]:
        """Parsear la respuesta de clasificación de Gemini"""
        try:
            # Intentar extraer JSON de la respuesta
            import json
            import re
            
            # Buscar JSON en la respuesta
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                result = json.loads(json_str)
                
                # Validar campos requeridos
                if "intent" in result:
                    return {
                        "intent": result.get("intent", "conversacion_general"),
                        "confidence": float(result.get("confidence", 0.8)),
                        "entities": result.get("extracted_entities", {}),
                        "should_show_products": result.get("should_show_products", False),
                        "reasoning": result.get("reasoning", "")
                    }
        except Exception as e:
            logger.error(f"Error parseando respuesta de clasificación: {e}")
        
        # Fallback si no se puede parsear
        return self._fallback_classification(original_message, conversation_history)
        
    def _fallback_classification(self, message: str, conversation_history: Optional[list] = None) -> Dict[str, Any]:
        """Clasificación básica de respaldo"""
        message_lower = message.lower()
        
        # Palabras clave para diferentes intenciones
        tech_comparison_keywords = ["mejor", "diferencia", "vs", "versus", "cual", "que", "comparar", "entre"]
        tech_brands_components = [
            "hp", "lenovo", "dell", "asus", "acer", "msi", "apple", "samsung",
            "intel", "amd", "nvidia", "qualcomm", "mediatek",
            "android", "ios", "windows", "linux", "mac",
            "tvbox", "androidtv", "roku", "chromecast", "firestick",
            "ssd", "hdd", "ram", "procesador", "cpu", "gpu", "tarjeta"
        ]
        product_keywords = ["busco", "quiero", "necesito", "comprar", "ver", "mostrar", "tienes", "tienen"]
        product_types = ["laptop", "pc", "tablet", "smartphone", "monitor", "computadora", "equipo"]
        greeting_keywords = ["hola", "buenos", "gracias", "adios", "saludos"]
        spec_keywords = ["especificaciones", "specs", "características", "detalles", "información"]
        reference_keywords = ["primera", "primero", "1", "segunda", "segundo", "2", "tercera", "tercero", "3"]
        
        # Verificar si es una solicitud de especificaciones referencial
        is_spec_request = False
        if any(keyword in message_lower for keyword in spec_keywords):
            if any(ref in message_lower for ref in reference_keywords):
                is_spec_request = True
        
        # Verificar si es una solicitud simple de "la segunda", "el 2", etc.
        if any(ref in message_lower for ref in reference_keywords) and len(message_lower.split()) <= 4:
            # Si es un mensaje corto con referencia, probablemente quiere ver especificaciones
            is_spec_request = True
            
        # Para "cual es la mejor"
        if "cual es la mejor" in message_lower and len(message_lower.split()) <= 6:
            # Verificar si hay historial de conversación y si hay productos listados
            if conversation_history and len(conversation_history) > 0:
                last_bot_response = ""
                for msg in reversed(conversation_history):
                    if msg.get("bot_response"):
                        last_bot_response = msg["bot_response"]
                        break
                        
                if "encontré" in last_bot_response.lower() and "opciones" in last_bot_response.lower():
                    # Si el bot acaba de mostrar productos, probablemente el usuario quiere una recomendación
                    return {
                        "intent": "buscar_producto",
                        "confidence": 0.85,
                        "entities": {},
                        "should_show_products": True,
                        "reasoning": "Solicita recomendación de los productos mostrados previamente"
                    }
            
        # Primero detectar si es una solicitud de producto específica (tiene alta prioridad)
        is_product_request = False
        
        # Patrones comunes para solicitudes de productos
        if any(f"mejor {prod}" in message_lower for prod in product_types):
            is_product_request = True
        
        if any(f"{prod} que tienes" in message_lower for prod in product_types):
            is_product_request = True
            
        if any(f"recomienda {prod}" in message_lower for prod in product_types):
            is_product_request = True
            
        if any(keyword in message_lower for keyword in product_keywords):
            if any(prod in message_lower for prod in product_types):
                is_product_request = True
                
        # Patrón específico: "Cual es la mejor laptop que tienes"
        if ("cual" in message_lower or "que" in message_lower or "cuál" in message_lower or "qué" in message_lower) and "mejor" in message_lower:
            if any(prod in message_lower for prod in product_types) and ("tienes" in message_lower or "tienen" in message_lower):
                is_product_request = True
        
        # Detectar patrón de pregunta tecnológica "qué es mejor X o Y"
        is_tech_comparison = False
        if any(keyword in message_lower for keyword in tech_comparison_keywords):
            # Verificar si menciona tecnologías, marcas o componentes
            mentioned_tech = [tech for tech in tech_brands_components if tech in message_lower]
            if len(mentioned_tech) >= 1:  # Al menos una tecnología mencionada
                # Si también solicita un producto, darle prioridad a eso
                if not is_product_request and not is_spec_request:
                    is_tech_comparison = True
        
        # Determinar la intención final
        if is_spec_request:
            intent = "ver_especificaciones"
            should_show = True
        elif any(keyword in message_lower for keyword in greeting_keywords):
            intent = "conversacion_general"
            should_show = False
        elif is_product_request:
            intent = "buscar_producto"
            should_show = True
        elif is_tech_comparison:
            intent = "pregunta_tecnologica"
            should_show = False
        else:
            # Verificar si hay historial de conversación
            if conversation_history and len(conversation_history) > 0:
                # Si el último mensaje del bot fue mostrar productos, asumir que quiere buscar más
                last_bot_response = ""
                for msg in reversed(conversation_history):
                    if msg.get("bot_response"):
                        last_bot_response = msg["bot_response"]
                        break
                        
                if "encontré" in last_bot_response.lower() and "opciones" in last_bot_response.lower():
                    intent = "buscar_producto"
                    should_show = True
                else:
                    intent = "conversacion_general"
                    should_show = False
            else:
                intent = "conversacion_general"
                should_show = False
        
        # Asignar entidades específicas para ver_especificaciones cuando se refiere a un producto por número
        entities = {}
        if intent == "ver_especificaciones":
            if "1" in message_lower or "primer" in message_lower or "primera" in message_lower:
                entities["numero_producto"] = 1
            elif "2" in message_lower or "segund" in message_lower:
                entities["numero_producto"] = 2
            elif "3" in message_lower or "tercer" in message_lower:
                entities["numero_producto"] = 3
            elif "4" in message_lower or "cuart" in message_lower:
                entities["numero_producto"] = 4
            elif "5" in message_lower or "quint" in message_lower:
                entities["numero_producto"] = 5
            entities["referencia_contextual"] = True
        
        return {
            "intent": intent,
            "confidence": 0.9 if is_spec_request else (0.8 if is_product_request else (0.7 if is_tech_comparison else 0.6)),
            "entities": entities,
            "should_show_products": should_show,
            "reasoning": f"Clasificación de respaldo - Detectado: {'solicitud de especificaciones' if is_spec_request else ('solicitud de producto' if is_product_request else ('pregunta tecnológica' if is_tech_comparison else 'conversación general'))}"
        }
