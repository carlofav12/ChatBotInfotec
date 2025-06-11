# filepath: backend/app/chatbot/utils/conversation_manager.py
"""
Manejador de conversaciones y contexto
Maneja el historial de conversaciones y el contexto entre mensajes
"""
import logging
from datetime import datetime
from typing import Dict, List, Any

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
                         intent: str, entities: Dict[str, Any], products_shown: bool = False) -> None:
        """Guardar conversación en el historial"""
        if session_id not in self.session_conversations:
            self.session_conversations[session_id] = []
        
        conversation_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "bot_response": bot_response,
            "intent": intent,
            "entities": entities,
            "showed_products": products_shown
        }
        
        self.session_conversations[session_id].append(conversation_entry)
        
        # Mantener solo las últimas 10 conversaciones por eficiencia
        if len(self.session_conversations[session_id]) > 10:
            self.session_conversations[session_id] = self.session_conversations[session_id][-10:]
    
    def get_context_string(self, conversation_history: List[Dict[str, Any]]) -> str:
        """Generar string de contexto para la IA"""
        if not conversation_history:
            return ""
        
        recent_context = conversation_history[-2:]  # Últimas 2 conversaciones
        context_str = "Conversación previa: " + " | ".join([
            f"Usuario: {conv['user_message'][:50]} -> Bot: {conv['bot_response'][:50]}" 
            for conv in recent_context
        ])
        
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
        
        products_shown_count = sum(1 for conv in history if conv.get("showed_products", False))
        
        return {
            "message_count": len(history),
            "products_shown": products_shown_count,
            "start_time": history[0]["timestamp"] if history else None,
            "last_activity": history[-1]["timestamp"] if history else None
        }
