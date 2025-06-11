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
                    "conversation_id": session_id
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
            
            if should_search:
                # Procesar solicitudes relacionadas con productos
                bot_response, products = self._handle_product_request(
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
                "conversation_id": session_id
            }
            
        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}")
            return {
                "response": "Disculpa, tuve un problema técnico. ¿Podrías repetir tu mensaje? Estoy aquí para ayudarte 🤖",
                "intent": "error",
                "entities": {},
                "products": [],
                "conversation_id": session_id
            }
    
    def _handle_product_request(self, entities: Dict[str, Any], conversation_history: List[Dict[str, Any]], 
                               db: Session, user_id: Optional[int], session_id: str) -> tuple:
        """Manejar solicitudes relacionadas con productos"""
        products = []
        bot_response = ""
        
        # Manejar acciones específicas
        if entities.get("accion") == "ver_especificaciones":
            bot_response, products = self._handle_specifications_request(entities, db)
        
        elif entities.get("accion") == "agregar_carrito":
            bot_response, products = self._handle_add_to_cart_request(
                entities, conversation_history, db, user_id, session_id
            )
        
        else:
            # Búsqueda normal de productos
            bot_response, products = self._handle_product_search(entities, conversation_history, db)
        
        return bot_response, products
    
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
        """Manejar solicitud de agregar al carrito"""
        if entities.get("producto_especifico"):
            product = self.product_service.find_product_by_name(db, entities["producto_especifico"])
            if product:
                quantity = entities.get("cantidad", 1)
                success = self.product_service.add_to_cart(db, product.id, quantity, user_id, session_id)
                if success:
                    bot_response = f"✅ ¡Perfecto! He agregado **{product.name}** a tu carrito.\n\n"
                    bot_response += f"📦 **Cantidad:** {quantity}\n"
                    bot_response += f"💰 **Precio:** S/ {product.price:.2f}\n"
                    bot_response += f"💳 **Total:** S/ {product.price * quantity:.2f}\n\n"
                    bot_response += "¿Te gustaría ver más productos o proceder con la compra? 😊"
                else:
                    bot_response = f"❌ Lo siento, no pude agregar **{product.name}** al carrito. Podría estar agotado o no tener suficiente stock."
                return bot_response, [product]
            else:
                bot_response = f"No encontré el producto '{entities['producto_especifico']}' en nuestro inventario. ¿Podrías verificar el nombre del modelo?"
                return bot_response, []
        else:
            # Buscar productos para que elija cuál agregar
            search_query = self.entity_extractor.get_search_query_from_context(entities, conversation_history)
            products = self.product_service.search_products(db, search_query, max_price=entities.get("presupuesto"))
            
            if products:
                bot_response = "¿Cuál de estos productos te gustaría agregar al carrito? Solo menciona el nombre específico:\n\n"
                bot_response += self.response_formatter.generate_product_response(products)
                return bot_response, products
            else:
                bot_response = "No encontré productos disponibles que coincidan con tu búsqueda. ¿Podrías ser más específico?"
                return bot_response, []
    
    def _handle_product_search(self, entities: Dict[str, Any], conversation_history: List[Dict[str, Any]], 
                              db: Session) -> tuple:
        """Manejar búsqueda normal de productos"""
        search_query = self.entity_extractor.get_search_query_from_context(entities, conversation_history)
        products = self.product_service.search_products(
            db, search_query, max_price=entities.get("presupuesto")
        )
        
        if products:
            detected_use_case = entities.get("uso")
            bot_response = self.response_formatter.generate_product_response(products, detected_use_case)
            return bot_response, products
        else:
            # Fallback: buscar productos generales
            fallback_products = self.product_service.search_products(db, "laptop")
            if fallback_products:
                products = fallback_products[:5]
                bot_response = "No encontré exactamente lo que buscas, pero aquí tienes algunas opciones populares que podrían interesarte:\n\n"
                bot_response += self.response_formatter.generate_product_response(products)
                return bot_response, products
            else:
                bot_response = "Por el momento no tenemos productos disponibles en nuestro inventario. Te sugerimos contactarnos directamente para consultar disponibilidad. 📞"
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
