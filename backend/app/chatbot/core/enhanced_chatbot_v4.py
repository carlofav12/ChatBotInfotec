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
        
        # Inicializar utilidades
        self.entity_extractor = EntityExtractor()
        self.response_formatter = ResponseFormatter()
        self.conversation_manager = ConversationManager()
        
        logger.info("ChatbotV4 inicializado correctamente")
    
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
                "products": [p.dict() for p in products] if products else [],
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

    def _handle_product_request(self, entities: Dict[str, Any], conversation_history: List[Dict[str, Any]], 
                               db: Session, user_id: Optional[int], session_id: str) -> tuple:
        """Manejar solicitudes relacionadas con productos"""
        products = []
        bot_response = ""
        cart_action = None
        
        # Manejar acciones específicas
        if entities.get("accion") == "ver_especificaciones":
            bot_response, products = self._handle_specifications_request(entities, db)
        
        elif entities.get("accion") == "agregar_carrito":
            bot_response, products, cart_action = self._handle_add_to_cart_request(
                entities, conversation_history, db, user_id, session_id
            )
        
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
        """Manejar conversación general"""
        # Verificar respuestas preparadas primero
        prepared_response = self.response_formatter.check_prepared_response(message)
        if prepared_response:
            return prepared_response
        
        # Generar contexto para la IA
        context_str = self.conversation_manager.get_context_string(conversation_history)
        
        # Usar IA para respuesta general
        return self.ai_generator.generate_general_response(message, context_str)

    # Métodos de utilidad para compatibilidad
    def get_conversation_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Obtener historial de conversación"""
        return self.conversation_manager.get_conversation_history(session_id)

    def clear_session(self, session_id: str) -> None:
        """Limpiar sesión"""
        self.conversation_manager.clear_session(session_id)
