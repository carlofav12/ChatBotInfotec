"""
Chatbot principal modularizado - Versión 4
Orquesta todos los componentes del chatbot de manera organizada
"""
import logging
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session

from ..services.product_service import ProductService
from ..services.ai_response_generator import AIResponseGenerator
from ..services.enhanced_llm_service import EnhancedLLMService
from ..services.intent_classifier import IntentClassifier
from ..utils.entity_extractor import EntityExtractor
from ..utils.response_formatter import ResponseFormatter
from ..utils.conversation_manager import ConversationManager

logger = logging.getLogger(__name__)

class EnhancedInfotecChatbotV4:
    """Chatbot principal mejorado y modularizado"""
    
    def __init__(self, api_key: str):
        """Inicializar el chatbot con todos sus componentes"""
        # Inicializar servicios
        self.product_service = ProductService()
        self.ai_generator = AIResponseGenerator(api_key)
        self.llm_service = EnhancedLLMService(api_key)
        self.intent_classifier = IntentClassifier(api_key)
        # Inicializar utilidades
        self.entity_extractor = EntityExtractor()
        self.response_formatter = ResponseFormatter()
        self.conversation_manager = ConversationManager()
        
        logger.info("ChatbotV4 inicializado correctamente con LLM mejorado y clasificador de intenciones")
    
    def process_message(self, message: str, db: Session, user_id: Optional[int] = None, 
                       session_id: str = "default") -> Dict[str, Any]:
        """Procesar mensaje del usuario - Método principal"""
        try:
            # Validar entrada
            if not message or not message.strip():
                return {
                    "response": "¡Hola! 👋 Soy InfoBot de GRUPO INFOTEC. ¿En qué puedo ayudarte hoy?",
                    "intent": "saludo",
                    "entities": {},
                    "products": [],
                    "conversation_id": session_id,
                    "cart_action": None
                }
            
            # Obtener historial de conversación
            conversation_history = self.conversation_manager.get_conversation_history(session_id)
            
            # Usar IA para clasificar la intención del mensaje
            intent_result = self.intent_classifier.classify_intent(message, conversation_history)
            intent = intent_result["intent"]
            should_search = intent_result["should_show_products"]
            
            # Extraer entidades adicionales si es necesario (mantenemos para compatibilidad)
            entities = self.entity_extractor.extract_entities(message, conversation_history)
            
            # Agregar información del clasificador de intenciones
            entities["_intent_confidence"] = intent_result["confidence"]
            entities["_intent_reasoning"] = intent_result["reasoning"]
            entities["_ai_entities"] = intent_result["entities"]
            entities["_original_message"] = message  # Guardar mensaje original
            
            # Mapear intent a acción para compatibilidad con el sistema existente
            if intent == "pregunta_tecnologica":
                entities["accion"] = "pregunta_tecnologica"
            elif intent == "buscar_producto":
                entities["accion"] = "buscar_productos"
            elif intent == "comparar_productos":
                entities["accion"] = "comparar_productos"
            elif intent == "ver_especificaciones":
                entities["accion"] = "ver_especificaciones"
            elif intent == "agregar_carrito":
                entities["accion"] = "agregar_carrito"
                
            products = []
            bot_response = ""
            cart_action = None
            
            if should_search or entities.get("accion") == "pregunta_tecnologica":
                # Procesar solicitudes relacionadas con productos o preguntas tecnológicas
                bot_response, products, cart_action = self._handle_product_request(
                    entities, conversation_history, db, user_id, session_id
                )
            else:
                # Generar respuesta general
                bot_response = self._handle_general_conversation(message, conversation_history)
            
            # MEJORA: Mejorar la serialización de productos para guardar en conversación
            products_list = []
            if products:
                # Convertir los productos a un formato serializable optimizado
                for p in products:
                    if hasattr(p, 'dict'):
                        # Si tiene método dict, usarlo directamente
                        product_dict = p.dict()
                        # Guardar solo campos esenciales para optimizar
                        products_list.append({
                            "name": product_dict.get("name", ""),
                            "id": product_dict.get("id", None),
                            "price": product_dict.get("price", 0),
                            "brand": product_dict.get("brand", ""),
                            "type": product_dict.get("type", ""),
                        })
                    elif isinstance(p, dict):
                        # Si ya es un diccionario, guardar campos esenciales
                        products_list.append({
                            "name": p.get("name", ""),
                            "id": p.get("id", None),
                            "price": p.get("price", 0),
                            "brand": p.get("brand", ""),
                            "type": p.get("type", ""),
                        })
                    else:
                        # Si no podemos convertirlo, al menos guardar el nombre como string
                        try:
                            products_list.append({"name": str(p)})
                        except Exception as e:
                            logger.warning(f"No se pudo convertir producto para guardar: {e}")
            
            # MEJORA: Mejor manejo de productos mostrados
            showed_products = len(products) > 0
            
            # Agregar contexto de la respuesta para hacer tracking de productos
            if showed_products and not products_list:
                # Si la respuesta indica productos pero no tenemos lista, extraer nombres
                import re
                product_patterns = [
                    r'\*\*\d+\.\s+([^*\(]+?)(?:\*\*|\()',   # **1. Nombre del producto** o **1. Nombre del producto(
                    r'\d+\.\s+\*\*([^*\(]+?)(?:\*\*|\()',   # 1. **Nombre del producto** o 1. **Nombre del producto(
                ]
                
                all_matches = []
                for pattern in product_patterns:
                    matches = re.findall(pattern, bot_response)
                    if matches:
                        all_matches.extend(matches)
                
                for name in all_matches:
                    products_list.append({"name": name.strip()})
            
            # Registrar para depuración
            logger.info(f"Guardando conversación con {len(products_list)} productos")
              # Guardar conversación con toda la información relevante
            self.conversation_manager.save_conversation(
                session_id, message, bot_response, intent, entities, 
                products_shown=showed_products,
                products_list=products_list
            )
            
            return {
                "response": bot_response,
                "intent": intent,
                "entities": entities,
                "products": products,
                "conversation_id": session_id,
                "cart_action": cart_action
            }
            
        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}")
            return {
                "response": "Disculpa, tuve un problema técnico. ¿Podrías repetir tu mensaje? Estoy aquí para ayudarte 🤖",
                "intent": "error",
                "entities": {},
                "products": [],
                "conversation_id": session_id,
                "cart_action": None
            }
        
    def _handle_comparison_request(self, entities: Dict[str, Any], db: Session) -> tuple:
        """Manejar solicitud de comparación de productos usando LLM mejorado."""
        product_names = entities.get("productos_a_comparar", [])
        brand_names = entities.get("marcas_a_comparar", [])
        attributes = entities.get("atributos_a_comparar", ["caracteristicas"])
        original_query = entities.get("_original_message", "comparación de productos")
        
        if not product_names and not brand_names:
            # Usar LLM para responder si no se especifican productos
            bot_response = self.llm_service.answer_tech_question(
                f"El usuario quiere comparar productos pero no especificó cuáles. Mensaje: '{original_query}'",
                "Necesito nombres específicos de productos o marcas para hacer una comparación"
            )
            return bot_response, [], None 

        # MEJORA: Si solo hay marcas, ir directamente al LLM sin buscar productos
        if brand_names and len(brand_names) >= 2 and not product_names:
            logger.info(f"Comparación directa de marcas detectada: {brand_names}")
            bot_response = self.llm_service.generate_comparison_response(
                brand_names[0], 
                brand_names[1], 
                attributes,
                None,  # Sin datos de productos específicos
                None
            )
            return bot_response, [], None
            
        # Buscar los productos en la base de datos
        products = []
        for name in product_names:
            product = self.product_service.find_product_by_name(db, name)
            if product:
                products.append(product)
        
        # Si se encuentra al menos un producto, seguir con el proceso
        if len(products) >= 2:
            # Comparar los dos primeros productos encontrados
            bot_response = self.response_formatter.format_product_comparison(
                products[0], products[1], attributes
            )
            return bot_response, products, None
        elif len(products) == 1 and brand_names and len(brand_names) >= 1:
            # Si tenemos un producto y una marca, usar LLM para comparación
            bot_response = self.llm_service.generate_comparison_response(
                products[0].brand, 
                brand_names[0], 
                attributes,
                products[0].dict(),
                None
            )
            return bot_response, products, None
        else:
            # No se encontraron suficientes productos, buscar productos recomendados
            search_query = " ".join(product_names + brand_names)
            recommended_products = self.product_service.search_products(db, search_query)
            
            if recommended_products and len(recommended_products) >= 2:
                # Mostrar productos encontrados para que el usuario elija
                bot_response = "🔍 No encontré exactamente los productos que mencionaste, pero te muestro algunas opciones disponibles:\n\n"
                bot_response += self.response_formatter.generate_product_response(recommended_products)
                bot_response += "\n\n💡 Para comparar, puedes decirme: 'Compara la primera con la tercera opción' o usar los nombres específicos."
                return bot_response, recommended_products, None
            else:
                # No se encontraron productos, usar LLM para generar respuesta
                if product_names and len(product_names) >= 2:
                    bot_response = self.llm_service.generate_comparison_response(
                        product_names[0], 
                        product_names[1], 
                        attributes,
                        None,
                        None
                    )
                else:
                    bot_response = "Lo siento, no pude encontrar suficientes productos para hacer una comparación. ¿Podrías mencionar los nombres específicos de los productos que quieres comparar?"
                    
                return bot_response, [], None
    
    def _handle_tech_question(self, message: str, conversation_history: List[Dict[str, Any]]) -> str:
        """Manejar preguntas técnicas usando LLM especializado"""
        # Generar contexto para la IA
        context_str = self.conversation_manager.get_context_string(conversation_history)
        
        # Usar servicio LLM para responder preguntas tecnológicas
        return self.llm_service.answer_tech_question(message, context_str)
    
    def _handle_product_request(self, entities: Dict[str, Any], 
                               conversation_history: List[Dict[str, Any]],
                               db: Session, user_id: Optional[int], 
                               session_id: str) -> tuple:
        """Manejar solicitudes relacionadas con productos"""
        # Usar entidades y acción para determinar el tipo de solicitud
        action = entities.get("accion", "")
        
        # Si es una pregunta tecnológica, manejarla con el servicio LLM
        if action == "pregunta_tecnologica":
            original_message = entities.get("_original_message", "")
            bot_response = self._handle_tech_question(original_message, conversation_history)
            return bot_response, [], None
        
        # Solicitud de ver especificaciones de un producto
        if action == "ver_especificaciones":
            # Si hay un producto específico mencionado, mostrar sus especificaciones
            if entities.get("producto_especifico"):
                return self._handle_specific_product_request(entities, db)
            else:
                # Si hay una referencia contextual (la segunda, el primero, etc.)
                if entities.get("numero_producto"):
                    return self._handle_contextual_spec_request(entities, conversation_history, db)
                else:
                    # Si no hay un producto específico ni referencia contextual, mostrar ayuda
                    bot_response = """Parece que quieres ver especificaciones de un producto, pero no sé cuál.

💡 **¿Podrías ser más específico?**
• Menciona el nombre exacto: "Especificaciones de la laptop HP Pavilion"
• O si ya te mostré opciones antes, puedes decir: "Muéstrame la primera opción"
• También puedes iniciar una nueva búsqueda: "Busco laptops para gaming"

¿Cómo te gustaría continuar? 😊"""
                    return bot_response, [], None
        
        # Solicitud de comparación de productos
        elif action == "comparar_productos":
            return self._handle_comparison_request(entities, db)
        
        # Solicitud de agregar al carrito
        elif action == "agregar_carrito":
            return self._handle_add_to_cart_request(entities, conversation_history, db, user_id, session_id)
            
        # Por defecto, búsqueda de productos
        else:
            bot_response, products = self._handle_product_search(entities, conversation_history, db)
            return bot_response, products, None
    
    def _handle_specific_product_request(self, entities: Dict[str, Any], db: Session) -> tuple:
        """Manejar solicitud de ver detalles de un producto específico"""
        product = self.product_service.find_product_by_name(db, entities["producto_especifico"])
        
        if product:
            # Generar respuesta con todos los detalles del producto
            bot_response = self.response_formatter.format_product_details(product)
            return bot_response, [product], None
        else:
            # Producto no encontrado
            bot_response = f"""🔍 No pude encontrar el producto **"{entities['producto_especifico']}"** en nuestro inventario.

💡 **Sugerencias:**
• Verifica que el nombre esté correctamente escrito
• Prueba buscando con términos más generales
• O pregúntame por categorías de productos disponibles

¿Te gustaría que busque alternativas similares? 😊"""
            return bot_response, [], None
    
    def _handle_contextual_spec_request(self, entities: Dict[str, Any], 
                                      conversation_history: Optional[List[Dict[str, Any]]], 
                                      db: Session) -> tuple:
        """Manejar solicitudes de especificaciones con referencias contextuales (la segunda, el primero, etc.)"""
        numero_producto = entities.get("numero_producto", 1)
        logger.info(f"Solicitud de especificaciones para producto #{numero_producto}")
        
        # Verificar si hay conversación previa
        if not conversation_history:
            bot_response = f"""Lo siento, no puedo identificar cuál es "{'la ' + ['primera', 'segunda', 'tercera'][numero_producto-1] if numero_producto <= 3 else 'el producto'}" porque no hay conversación previa.

¿Podrías mencionar el nombre específico del producto del que quieres ver las especificaciones? 😊"""
            return bot_response, []
        
        # MEJORA: Buscar en el historial la última vez que se mostraron productos
        # Extraer los nombres de productos desde el historial de conversación
        recommended_products = self._extract_last_recommended_products(conversation_history)
        
        # Registrar información detallada para depuración
        logger.info(f"Productos encontrados en conversación (total: {len(recommended_products)}): {recommended_products}")
        
        # Verificar si se encontraron suficientes productos
        if not recommended_products or len(recommended_products) < numero_producto:
            # Preparar un mensaje más informativo
            if not recommended_products:
                message = "No encontré productos mencionados en nuestra conversación reciente."
            else:
                message = f"Solo encontré {len(recommended_products)} productos en nuestra conversación, pero estás preguntando por el #{numero_producto}."
                
            ordinal = ['primera', 'segunda', 'tercera'][numero_producto-1] if numero_producto <= 3 else f'producto #{numero_producto}'
            bot_response = f"""Lo siento, no puedo mostrar información sobre la {ordinal} opción. {message}

¿Podrías decirme el nombre específico del producto que te interesa? También puedo mostrarte nuestras mejores recomendaciones nuevamente. 😊"""
            return bot_response, []
        
        # Obtener el producto específico por su índice
        target_product_name = recommended_products[numero_producto - 1]
        logger.info(f"Buscando especificaciones para: '{target_product_name}'")
        
        # MEJORA: Buscar el producto en la base de datos de forma más flexible
        product = self.product_service.find_product_by_name(db, target_product_name)
        
        if product:
            # Generar respuesta con los detalles del producto
            bot_response = self.response_formatter.format_product_details(product)
            return bot_response, [product], None
        else:
            # Si no se encuentra el producto exacto, intentar buscar alternativas
            logger.warning(f"No se encontró el producto '{target_product_name}' en la base de datos")
            
            # Intento de búsqueda más flexible con términos clave del nombre
            search_terms = ' '.join([term for term in target_product_name.split() if len(term) > 3])
            alternative_products = self.product_service.search_products(db, search_terms, limit=3)
            
            if alternative_products:
                bot_response = f"""No encontré exactamente el producto "**{target_product_name}**" en nuestro inventario, pero te muestro algunas alternativas similares:

{self.response_formatter.generate_product_response(alternative_products)}

¿Te gustaría ver detalles de alguno de estos productos? 😊"""
                return bot_response, alternative_products, None
            else:
                bot_response = f"""Lo siento, no pude encontrar el producto "**{target_product_name}**" ni alternativas similares en nuestro inventario.

💡 **Opciones:**
• Intenta con una nueva búsqueda usando términos diferentes
• Pregúntame por categorías de productos disponibles
• Contactes directamente con nuestros especialistas

¿Cómo prefieres continuar? 😊"""
                return bot_response, []
    
    def _extract_last_recommended_products(self, conversation_history: List[Dict[str, Any]]) -> List[str]:
        """Extraer la lista de productos recomendados de la conversación más reciente"""
        product_names = []
        
        # Buscar hacia atrás en el historial la última respuesta que contenga productos
        for entry in reversed(conversation_history):            # Registrar entrada para depuración
            logger.info(f"Analizando entrada de conversación: products_shown={entry.get('products_shown')}, intent={entry.get('intent')}")
            
            # MEJORA: Verificar primero si el mensaje es una respuesta a una búsqueda de productos
            intent = entry.get("intent", "")
            is_product_related = intent in ["buscar_producto", "comparar_productos", "ver_especificaciones"]
            showed_products = entry.get("products_shown", False)
            
            # Intentar obtener productos de la nueva estructura optimizada
            products_list = entry.get("products_list", [])
            
            if products_list:
                logger.info(f"Encontrada lista de productos con {len(products_list)} elementos")
                for product in products_list:
                    if isinstance(product, dict):
                        if 'name' in product:
                            name = product.get("name", "").strip()
                            if name:  # Verificar que no sea vacío
                                product_names.append(name)
                                logger.info(f"Producto extraído de products_list: {name}")
                    else:
                        # Si es un objeto product, intentar extraer el nombre
                        try:
                            name = product.name if hasattr(product, 'name') else str(product)
                            if name.strip():  # Verificar que no sea vacío
                                product_names.append(name)
                                logger.info(f"Producto extraído de products_list (objeto): {name}")
                        except Exception as e:
                            logger.warning(f"No se pudo extraer nombre de producto: {e}")
                
                if product_names:
                    logger.info(f"Se extrajeron {len(product_names)} productos de products_list")
                    break
            
            # MEJORA: Extraer productos directamente del texto de la respuesta
            bot_response = entry.get("bot_response", "")
            
            # MEJORA: Comprobar si la respuesta contiene listado de productos numerados
            # Patrones más comunes en las respuestas del chatbot
            if (showed_products or is_product_related) and bot_response:
                import re
                
                # MEJORA: Usar patrones específicos para detectar productos en respuestas formateadas
                patterns = [
                    # Patrones específicos del formato de respuesta
                    r'\*\*\d+\.\s+([^*\(]+?)(?:\*\*|\()',   # **1. Nombre del producto** o **1. Nombre del producto(
                    r'\d+\.\s+\*\*([^*\(]+?)(?:\*\*|\()',   # 1. **Nombre del producto** o 1. **Nombre del producto(
                    r'\*\*([^*\n\(]+?)\*\*\s+\(S/\s+\d+',   # **Nombre del producto** (S/ precio)
                    
                    # Patrones generales para capturar productos en diferentes formatos
                    r'\*\*\d+\.\s+([^*]+?)\*\*',            # **1. Nombre de producto**
                    r'\d+\.\s+([^(]+?)\(',                  # 1. Nombre de producto (
                    r'\d+\.\s+([^:]+?):\s',                 # 1. Nombre de producto: 
                    r'\d+\.\s+([^\n]+?)(?=\n|$)',           # 1. Nombre de producto (final de línea)
                    
                    # Patrones de marca y modelo específicos
                    r'laptop ([A-Za-z0-9]+\s+[A-Za-z0-9]+)',  # laptop + marca modelo
                    r'([A-Za-z0-9]+\s+[A-Za-z0-9]+\s+[A-Za-z0-9]+)(?:\s+\d+GB|\s+\d+TB|\s+i\d)', # Patrones de marca, modelo y especificación
                ]
                
                all_matches = []
                for pattern in patterns:
                    matches = re.findall(pattern, bot_response)
                    if matches:
                        all_matches.extend(matches)
                        logger.info(f"Patrón '{pattern}' encontró {len(matches)} coincidencias")
                
                if all_matches:
                    # Limpiar los nombres de productos
                    for match in all_matches:
                        # MEJORA: Mejor limpieza de nombres
                        clean_name = match.strip()
                        # Eliminar separadores comunes
                        for sep in ['💰', '🏷️', '(', ')', ':', '*', '  ']:
                            if sep in clean_name:
                                clean_name = clean_name.split(sep)[0].strip()
                        
                        # Eliminar emojis y caracteres especiales comunes
                        clean_name = re.sub(r'[💻🎮⭐✨🔥💡📱🖥️💾🧠⚡]', '', clean_name).strip()
                        
                        # Validación más estricta para nombres de productos
                        if (clean_name and len(clean_name) > 3 and 
                            not clean_name.isdigit() and 
                            not clean_name.lower().startswith(('precio', 'total', 'subtotal', 'cantidad'))):
                            product_names.append(clean_name)
                            logger.info(f"Producto extraído del texto: '{clean_name}'")
                    
                    if product_names:
                        logger.info(f"Se extrajeron {len(product_names)} productos del texto de la respuesta")
                        break
        
        # Eliminar duplicados manteniendo el orden
        unique_products = []
        seen = set()
        for name in product_names:
            # Normalizar para comparación (minúsculas, sin espacios extras)
            norm_name = ' '.join(name.lower().split())
            if norm_name not in seen and len(norm_name) > 3:  # Filtro adicional por longitud
                seen.add(norm_name)
                unique_products.append(name)
        
        logger.info(f"Total de productos extraídos (únicos): {len(unique_products)}")
        logger.info(f"Productos encontrados: {unique_products}")
        return unique_products

    def _handle_add_to_cart_request(self, entities: Dict[str, Any], conversation_history: List[Dict[str, Any]], 
                                   db: Session, user_id: Optional[int], session_id: str) -> tuple:
        """Manejar solicitud de agregar al carrito - MEJORADO"""
        if entities.get("producto_especifico"):
            product = self.product_service.find_product_by_name(db, entities["producto_especifico"])
            if product:
                quantity = entities.get("cantidad", 1)
                result = self.product_service.add_to_cart(db, product.id, quantity, user_id, session_id)
                # Usar el response formatter para generar respuesta consistente
                bot_response = self.response_formatter.format_cart_response(result)
                
                # Retornar información adicional del carrito para sincronización
                cart_action = None
                if result.get("success"):
                    cart_action = {
                        "action": "add_to_cart",
                        "product": product.dict() if product else None,
                        "quantity": quantity,
                        "success": True
                    }
                
                return bot_response, [product], cart_action
            else:
                bot_response = f"🔍 No encontré el producto **'{entities['producto_especifico']}'** en nuestro inventario.\n\n"
                bot_response += "💡 **Sugerencias:**\n"
                bot_response += "• Verifica que el nombre del modelo esté correcto\n"
                bot_response += "• Prueba con palabras clave más simples\n"
                bot_response += "• Consulta nuestra lista completa de productos\n\n"
                bot_response += "¿Te gustaría que busque productos similares? 😊"
                return bot_response, [], None
        else:
            # Buscar productos para que elija cuál agregar
            search_query = self.entity_extractor.get_search_query_from_context(entities, conversation_history)
            products = self.product_service.search_products(db, search_query, max_price=entities.get("presupuesto"))
            
            if products:
                bot_response = "🛒 **¡Perfecto! Aquí tienes las opciones disponibles:**\n\n"
                bot_response += "Para agregar algún producto al carrito, solo menciona el **nombre específico** del modelo que te interese.\n\n"
                bot_response += self.response_formatter.generate_product_response(products)
                bot_response += "\n💡 **Ejemplo:** \"Agrega la laptop ASUS Vivobook\" o \"Quiero el HP ENVY\""
                return bot_response, products, None
            else:
                bot_response = "🔍 No encontré productos disponibles que coincidan con tu búsqueda.\n\n"
                bot_response += "💡 **¿Podrías ayudarme con más detalles?**\n"
                bot_response += "• ¿Qué tipo de producto buscas?\n"
                bot_response += "• ¿Tienes alguna marca preferida?\n"
                bot_response += "• ¿Cuál es tu presupuesto aproximado?\n\n"
                bot_response += "¡Estoy aquí para encontrar la mejor opción para ti! 😊"
                return bot_response, [], None

    def _handle_product_search(self, entities: Dict[str, Any], conversation_history: List[Dict[str, Any]],
                              db: Session) -> tuple:
        """Manejar búsqueda normal de productos"""
        search_query = self.entity_extractor.get_search_query_from_context(entities, conversation_history)
        
        if search_query:
            products = self.product_service.search_products(db, search_query, max_price=entities.get("presupuesto"))
            
            if products:
                use_case = entities.get("uso")
                bot_response = self.response_formatter.generate_product_response(products, use_case)
                return bot_response, products
            else:
                bot_response = "Por el momento no tenemos productos disponibles en nuestro inventario. Te sugerimos contactarnos directamente para consultar disponibilidad. 📞"
                return bot_response, []
        else:
            # Si no hay query de búsqueda, proporcionar ayuda general
            bot_response = "¡Hola! 👋 Estoy aquí para ayudarte a encontrar los mejores productos de tecnología.\n\n"
            bot_response += "💡 **¿Qué puedo hacer por ti?**\n"
            bot_response += "• Buscar laptops, computadoras, accesorios\n"
            bot_response += "• Ayudarte a elegir según tu presupuesto\n"
            bot_response += "• Mostrar especificaciones detalladas\n"
            bot_response += "• Agregar productos a tu carrito\n\n"
            bot_response += "¿Qué tipo de producto estás buscando? 😊"
            return bot_response, []

    def _handle_general_conversation(self, message: str, conversation_history: List[Dict[str, Any]]) -> str:
        """Manejar conversación general con capacidades tecnológicas mejoradas"""
        # Verificar respuestas preparadas primero
        prepared_response = self.response_formatter.check_prepared_response(message)
        if prepared_response:
            return prepared_response
        
        # Detectar si es una consulta tecnológica específica
        tech_keywords = [
            "diferencia entre", "qué es mejor", "cuál es la diferencia", "procesador", "cpu", "gpu", 
            "tarjeta gráfica", "memoria ram", "ssd", "hdd", "intel", "amd", "nvidia", "rendimiento",
            "gaming", "diseño gráfico", "programación", "desarrollo", "software", "hardware",
            "benchmark", "overclocking", "refrigeración", "fuente de poder", "monitor", "resolución",
            "hertz", "refresh rate", "linux", "windows", "mac", "sistema operativo"
        ]
        
        message_lower = message.lower()
        is_tech_question = any(keyword in message_lower for keyword in tech_keywords)
        
        # Generar contexto para la IA
        context_str = self.conversation_manager.get_context_string(conversation_history)
        
        if is_tech_question:
            # Usar LLM especializado para consultas tecnológicas
            return self.llm_service.answer_tech_question(message, context_str)
        else:
            # Usar IA general para respuesta conversacional
            return self.ai_generator.generate_general_response(message, context_str)

    # Métodos de utilidad para compatibilidad
    def get_conversation_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Obtener historial de conversación"""
        return self.conversation_manager.get_conversation_history(session_id)

    def clear_session(self, session_id: str) -> None:
        """Limpiar sesión"""
        self.conversation_manager.clear_session(session_id)
