"""
Manejador de conversaciones y contexto
Maneja el historial de conversaciones y el contexto entre mensajes
"""
import logging
import re
from datetime import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class ConversationManager:
    """Maneja el historial y contexto de conversaciones"""
    
    def __init__(self):
        # Diccionario para mantener las conversaciones por sesión
        self.session_conversations: Dict[str, List[Dict[str, Any]]] = {}
    
    def get_conversation_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Obtener historial de conversación para una sesión específica"""
        return self.session_conversations.get(session_id, [])
    
    def save_conversation(self, session_id: str, user_message: str, bot_response: str, 
                         intent: str, entities: Dict[str, Any], products_shown: bool = False,
                         products_list: Optional[List[Dict]] = None) -> None:
        """Guardar conversación en el historial"""
        if session_id not in self.session_conversations:
            self.session_conversations[session_id] = []
        
        conversation_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "bot_response": bot_response,
            "intent": intent,
            "entities": entities,
            "products_shown": products_shown,
            "products_list": products_list if products_list is not None else []
        }
        
        self.session_conversations[session_id].append(conversation_entry)
        
        # Mantener solo las últimas 10 conversaciones por eficiencia
        if len(self.session_conversations[session_id]) > 10:
            self.session_conversations[session_id] = self.session_conversations[session_id][-10:]
    
    def get_context_string(self, conversation_history: List[Dict[str, Any]]) -> str:
        """Generar string de contexto para la IA con información detallada"""
        if not conversation_history:
            return "Sin conversación previa."
        
        # Tomar las últimas 3-4 conversaciones para mejor contexto
        recent_context = conversation_history[-4:] if len(conversation_history) > 4 else conversation_history
        
        context_parts = []
        product_info = []
        
        for i, conv in enumerate(recent_context, 1):
            user_msg = conv.get('user_message', '')
            bot_msg = conv.get('bot_response', '')
            intent = conv.get('intent', '')
            products_shown = conv.get('products_shown', False)
            products_list = conv.get('products_list', [])
            
            # Resumir el intercambio
            user_summary = user_msg[:100] + "..." if len(user_msg) > 100 else user_msg
            
            # Información específica sobre el intent
            intent_info = ""
            if intent == "buscar_producto":
                intent_info = " (búsqueda de productos)"
            elif intent == "recomendar_producto":
                intent_info = " (solicitud de recomendación)"
            elif intent == "ver_especificaciones":
                intent_info = " (ver especificaciones)"
            elif intent == "agregar_carrito":
                intent_info = " (agregar al carrito)"
            
            context_parts.append(f"{i}. Usuario: {user_summary}{intent_info}")
            
            # Si se mostraron productos, incluir información específica
            if products_shown and products_list:
                product_names = []
                for product in products_list[:5]:  # Máximo 5 productos para no saturar
                    if isinstance(product, dict):
                        name = product.get('name', '')
                        if name:
                            product_names.append(name)
                
                if product_names:
                    product_info.append(f"   Productos mostrados: {', '.join(product_names)}")
            elif products_shown:
                # Si se mostraron productos pero no tenemos la lista, extraer del texto de respuesta
                # Buscar patrones de productos en la respuesta
                product_matches = re.findall(r'\*\*\d+\.\s+([^*\n]+?)\*\*', bot_msg)
                if product_matches:
                    product_info.append(f"   Productos mostrados: {', '.join(product_matches[:3])}...")
        
        # Construir el contexto final
        context_str = "CONVERSACIÓN RECIENTE:\n" + "\n".join(context_parts)
        
        if product_info:
            context_str += "\n\nPRODUCTOS MENCIONADOS:\n" + "\n".join(product_info)
        
        # Agregar información sobre el patrón de comportamiento del usuario
        if len(recent_context) > 1:
            last_intent = recent_context[-1].get('intent', '')
            if last_intent == 'buscar_producto' and any(conv.get('products_shown') for conv in recent_context):
                context_str += "\n\nCONTEXTO: El usuario ha visto productos y ahora puede estar pidiendo una recomendación específica."
        
        return context_str
    
    def clear_session(self, session_id: str) -> None:
        """Limpiar historial de una sesión específica"""
        if session_id in self.session_conversations:
            del self.session_conversations[session_id]
            logger.info(f"Historial de sesión {session_id} eliminado")
    
    def get_active_sessions(self) -> List[str]:
        """Obtener lista de sesiones activas"""
        return list(self.session_conversations.keys())
    
    def get_session_stats(self, session_id: str) -> Dict[str, Any]:
        """Obtener estadísticas de una sesión"""
        history = self.get_conversation_history(session_id)
        
        if not history:
            return {"message_count": 0, "products_shown": 0, "start_time": None, "last_activity": None}
        
        products_shown_count = sum(1 for conv in history if conv.get("products_shown", False))
        
        return {
            "message_count": len(history),
            "products_shown": products_shown_count,
            "start_time": history[0]["timestamp"] if history else None,
            "last_activity": history[-1]["timestamp"] if history else None
        }
    
    def clear_all_sessions(self) -> int:
        """Limpiar todos los historiales de conversación"""
        session_count = len(self.session_conversations)
        self.session_conversations.clear()
        logger.info(f"Todos los historiales eliminados ({session_count} sesiones)")
        return session_count
