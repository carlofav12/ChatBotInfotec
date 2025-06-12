# filepath: backend/app/chatbot/core/enhanced_chatbot_v4.py
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
        
        # Inicializar utilidades
        self.entity_extractor = EntityExtractor()
        self.response_formatter = ResponseFormatter()
        self.conversation_manager = ConversationManager()
        
        logger.info("ChatbotV4 inicializado correctamente con LLM mejorado")
    
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
            
            # Extraer entidades del mensaje con contexto
            entities = self.entity_extractor.extract_entities(message, conversation_history)
            
            # Determinar si debe mostrar productos
            should_search = self.entity_extractor.should_show_products(entities, conversation_history)
            
            intent = "buscar_producto" if should_search else "conversacion_general"
            products = []
            bot_response = ""
            cart_action = None
            
            if should_search:
                # Procesar solicitudes relacionadas con productos
                bot_response, products, cart_action = self._handle_product_request(
                    entities, conversation_history, db, user_id, session_id
                )
            else:
                # Generar respuesta general
                bot_response = self._handle_general_conversation(message, conversation_history)
            
            # Guardar conversación
            self.conversation_manager.save_conversation(
                session_id, message, bot_response, intent, entities, len(products) > 0
            )
            
            return {
                "response": bot_response,
                "intent": intent,
                "entities": entities,
                "products": [p.dict() if hasattr(p, 'dict') else p for p in products] if products else [],
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

        # Obtener datos de comparación solo si hay productos específicos
        comparison_data_list = []
        if product_names:
            # Solo buscar productos si hay nombres específicos
            comparison_data_list = self.product_service.get_comparison_data(
                db,
                product_names=product_names,
                brand_names=brand_names if product_names else [],  # Solo usar marcas si también hay productos específicos
                attributes=attributes
            )

        if len(comparison_data_list) < 2:
            # Si no hay suficientes productos, usar LLM para generar comparación basada en conocimiento general
            if len(comparison_data_list) == 1:
                # Un producto encontrado
                product_data = comparison_data_list[0]
                if brand_names and len(brand_names) >= 2:
                    # Comparar marcas usando LLM
                    bot_response = self.llm_service.generate_comparison_response(
                        brand_names[0], brand_names[1], attributes,
                        product_data if brand_names[0].lower() in product_data.get('name', '').lower() else None,
                        None
                    )
                else:
                    # Un producto vs otro mencionado pero no encontrado
                    missing_product = product_names[1] if len(product_names) > 1 else (brand_names[0] if brand_names else "producto no especificado")
                    bot_response = self.llm_service.generate_comparison_response(
                        product_data.get('name', product_names[0]),
                        missing_product,
                        attributes,
                        product_data,
                        None
                    )
            else:
                # Ningún producto encontrado, comparación basada solo en nombres
                if len(product_names) >= 2:
                    bot_response = self.llm_service.generate_comparison_response(
                        product_names[0], product_names[1], attributes
                    )
                elif len(brand_names) >= 2:
                    bot_response = self.llm_service.generate_comparison_response(
                        brand_names[0], brand_names[1], attributes
                    )
                else:
                    bot_response = "No pude encontrar productos específicos para comparar. ¿Podrías especificar dos productos o marcas?"
            
            return bot_response, comparison_data_list, None
        
        # Si tenemos 2 o más productos, usar LLM para comparación mejorada
        product1_data = comparison_data_list[0]
        product2_data = comparison_data_list[1]
        
        bot_response = self.llm_service.generate_comparison_response(
            product1_data.get('name', 'Producto 1'),
            product2_data.get('name', 'Producto 2'),
            attributes,
            product1_data,
            product2_data
        )
        
        return bot_response, comparison_data_list, None
    
    def _handle_intelligent_recommendation_request(self, entities: Dict[str, Any], db: Session) -> tuple:
        """Manejar solicitud de recomendación inteligente usando IA para analizar toda la BD"""
        logger.info("Procesando solicitud de recomendación inteligente")
        
        category = entities.get("categoria_recomendacion") or entities.get("producto")
        use_case = entities.get("uso")
        original_query = entities.get("_original_message", "recomendación de productos")
        
        # Obtener todos los productos relevantes para análisis
        candidate_products = self.product_service.get_all_products_for_recommendation(
            db, 
            category=category, 
            use_case=use_case,
            limit=50  # Analizar hasta 50 productos
        )
        
        if not candidate_products:
            bot_response = f"""💡 **Lo siento, no tengo productos disponibles en este momento.**

🔍 **Lo que puedo hacer:**
• Consultar productos específicos por nombre
• Ayudarte con categorías específicas como laptops, PCs, componentes
• Conectarte con nuestros especialistas

¿Te gustaría que busque algo más específico? 😊"""
            return bot_response, []
        
        # Convertir productos a formato dict para el LLM
        products_for_llm = []
        for product in candidate_products:
            product_dict = {
                "name": product.name,
                "price": product.price,
                "description": product.description,
                "brand": product.brand,
                "rating": product.rating,
                "stock_quantity": product.stock_quantity
            }
            
            # Añadir especificaciones si existen
            if hasattr(product, 'specifications') and product.specifications:
                if isinstance(product.specifications, dict):
                    product_dict["specifications"] = product.specifications
                else:
                    product_dict["specifications"] = {"details": str(product.specifications)}
            
            products_for_llm.append(product_dict)
        
        # Usar IA para analizar y recomendar los mejores productos
        try:
            bot_response = self.llm_service.recommend_top_products(
                candidate_products=products_for_llm,
                user_query=original_query,
                category=category,
                use_case=use_case,
                count=3  # Recomendar top 3
            )
            
            # Devolver los productos recomendados (primeros 3-5 para mostrar en la UI)
            recommended_products = candidate_products[:5]
            
        except Exception as e:
            logger.error(f"Error en recomendación inteligente: {e}")            # Fallback: usar formatter tradicional con los mejores productos por rating
            sorted_products = sorted(candidate_products, key=lambda x: (x.rating or 0, -x.price), reverse=True)
            recommended_products = sorted_products[:3]
            bot_response = f"""🎯 **Mis 3 mejores recomendaciones:**

"""
            for i, product in enumerate(recommended_products, 1):
                discount = ""
                if product.original_price and product.original_price > product.price:
                    discount_pct = int(((product.original_price - product.price) / product.original_price) * 100)
                    discount = f" 🏷️ **{discount_pct}% DESC**"
                
                # Generar descripción concisa
                features = []
                if hasattr(product, 'brand') and product.brand:
                    features.append(f"marca {product.brand}")
                if product.rating and product.rating > 0:
                    features.append(f"rating {product.rating}/5")
                
                feature_text = f" - {', '.join(features[:2])}" if features else ""
                
                bot_response += f"""**{i}. {product.name}** (S/ {product.price}){discount}
✨ Excelente opción{feature_text}

"""
            
            bot_response += "💡 ¿Te interesa alguna? ¡Puedo darte más detalles! 😊"
        
        return bot_response, recommended_products

    def _handle_tech_question(self, entities: Dict[str, Any], db: Session) -> tuple:
        """Manejar preguntas tecnológicas generales usando IA"""
        logger.info("Procesando pregunta tecnológica general")
        
        original_question = entities.get("_original_message", "pregunta tecnológica")
        question_type = entities.get("tipo_pregunta", "general")
        
        try:            # Usar el LLM para responder preguntas tecnológicas generales
            bot_response = self.llm_service.answer_tech_question(
                question=original_question,
                context=f"Tipo de pregunta: {question_type}"
            )
            
            # No devolver productos específicos para preguntas generales
            return bot_response, []
            
        except Exception as e:
            logger.error(f"Error procesando pregunta tecnológica: {e}")
            
            # Respuesta de fallback para preguntas tecnológicas
            if question_type == "laptop_vs_pc":
                bot_response = """💡 **Laptop vs PC - Guía rápida:**

**💻 Laptops (Portátiles):**
✅ Portabilidad y movilidad
✅ Menor consumo eléctrico 
✅ Todo integrado (pantalla, teclado, mouse)
❌ Menor rendimiento por el precio
❌ Más difícil de upgradar

**🖥️ PCs de Escritorio:**
✅ Mejor rendimiento por el precio
✅ Fácil de actualizar componentes
✅ Mejor refrigeración
❌ Requiere espacio fijo
❌ Mayor consumo eléctrico

**🎯 Recomendación:**
• **Para trabajo móvil/estudiantes:** Laptop
• **Para gaming/diseño:** PC de escritorio  
• **Para oficina fija:** Ambos funcionan bien

¿Te gustaría ver nuestras opciones disponibles? 😊"""
            else:
                bot_response = """💡 **Consulta Tecnológica:**

Gracias por tu pregunta. Para darte la mejor recomendación, necesito más detalles:

🔍 **¿Podrías especificar:**
• ¿Para qué la vas a usar? (trabajo, gaming, estudios)
• ¿Tienes algún presupuesto en mente?
• ¿Alguna marca de preferencia?

¡Así podré ayudarte mejor! 😊"""
            
            return bot_response, []

    def _handle_product_request(self, entities: Dict[str, Any], conversation_history: List[Dict[str, Any]], 
                               db: Session, user_id: Optional[int], session_id: str) -> tuple:
        """Manejar solicitudes relacionadas con productos"""
        products = []
        bot_response = ""
        cart_action = None
        
        # Manejar acciones específicas
        if entities.get("accion") == "comparar_productos":
            bot_response, products, cart_action = self._handle_comparison_request(entities, db)
        
        elif entities.get("accion") == "ver_especificaciones":
            bot_response, products = self._handle_specifications_request(entities, db)
        
        elif entities.get("accion") == "agregar_carrito":
            bot_response, products, cart_action = self._handle_add_to_cart_request(
                entities, conversation_history, db, user_id, session_id
            )
        
        elif entities.get("accion") == "recomendar_categoria":
            bot_response, products = self._handle_intelligent_recommendation_request(entities, db)
        
        elif entities.get("accion") == "pregunta_tecnologica":
            bot_response, products = self._handle_tech_question(entities, db)
        
        else:
            # Búsqueda normal de productos
            bot_response, products = self._handle_product_search(entities, conversation_history, db)
        
        return bot_response, products, cart_action

    def _handle_specifications_request(self, entities: Dict[str, Any], db: Session) -> tuple:
        """Manejar solicitud de especificaciones"""
        if entities.get("producto_especifico"):
            product = self.product_service.find_product_by_name(db, entities["producto_especifico"])
            if product:
                bot_response = self.response_formatter.generate_product_specifications(product)
                return bot_response, [product]
            else:
                bot_response = f"No encontré información específica sobre '{entities['producto_especifico']}'. ¿Podrías ser más específico con el modelo?"
                return bot_response, []
        else:
            bot_response = "¿Sobre qué producto específico te gustaría conocer las especificaciones? Puedes mencionar el modelo exacto."
            return bot_response, []

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
