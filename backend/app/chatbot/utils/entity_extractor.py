# filepath: backend/app/chatbot/utils/entity_extractor.py
"""
Extractor de entidades del mensaje del usuario
Maneja la extracción de productos, marcas, precios, intenciones, etc.
"""
import re
import logging
from typing import Dict, Any, List, Optional
from ..core.config import ChatbotConfig

logger = logging.getLogger(__name__)

class EntityExtractor:
    """Extrae entidades relevantes del mensaje del usuario"""
    
    def __init__(self):
        self.config = ChatbotConfig()
    
    def extract_entities(self, message: str, conversation_history: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Extraer entidades del mensaje usando regex y contexto"""
        entities: Dict[str, Any] = {
            "_original_message": message
        }
        
        message_lower = message.lower()
        
        # Extraer productos específicos
        self._extract_product_category(message_lower, entities)
        
        # Extraer marcas
        self._extract_brand(message_lower, entities)
        
        # Extraer presupuesto
        self._extract_budget(message_lower, entities)
        
        # Extraer cantidad
        self._extract_quantity(message_lower, entities)
        
        # Detectar uso/caso de uso
        self._extract_use_case(message_lower, entities)
        
        # Detectar intención de agregar al carrito
        self._extract_cart_action(message_lower, entities, conversation_history)
        
        # Detectar solicitud de especificaciones
        self._extract_spec_action(message_lower, entities)
        
        # Detectar solicitud de recomendación
        self._extract_recommend_action(message_lower, entities)
        
        # Extraer nombre específico de producto mencionado
        self._extract_specific_product_name(message_lower, entities)
        
        return entities
    
    def _extract_product_category(self, message_lower: str, entities: Dict[str, Any]) -> None:
        """Extraer categoría de producto"""
        for product, pattern in self.config.PRODUCT_PATTERNS.items():
            if re.search(pattern, message_lower):
                entities["producto"] = product
                break
    
    def _extract_brand(self, message_lower: str, entities: Dict[str, Any]) -> None:
        """Extraer marca del producto"""
        for brand in self.config.BRANDS:
            if brand in message_lower:
                entities["marca"] = brand
                break
    
    def _extract_budget(self, message_lower: str, entities: Dict[str, Any]) -> None:
        """Extraer presupuesto/precio máximo"""
        price_match = re.search(r'(?:hasta|máximo|presupuesto|budget)\s*(?:de\s*)?(?:s/\s*)?(\d+)', message_lower)
        if price_match:
            entities["presupuesto"] = int(price_match.group(1))
    
    def _extract_quantity(self, message_lower: str, entities: Dict[str, Any]) -> None:
        """Extraer cantidad de productos"""
        quantity_match = re.search(r'(\d+)\s*(?:unidades?|pcs?|equipos?)', message_lower)
        if quantity_match:
            entities["cantidad"] = int(quantity_match.group(1))
    
    def _extract_use_case(self, message_lower: str, entities: Dict[str, Any]) -> None:
        """Detectar caso de uso/propósito"""
        for use_case, keywords in self.config.USE_CASES.items():
            if any(keyword in message_lower for keyword in keywords):
                entities["uso"] = use_case
                break
    
    def _extract_cart_action(self, message_lower: str, entities: Dict[str, Any], 
                           conversation_history: Optional[List[Dict[str, Any]]]) -> None:
        """Detectar intención de agregar al carrito"""
        if any(pattern in message_lower for pattern in self.config.CART_PATTERNS):
            entities["accion"] = "agregar_carrito"
            
            # Si usa referencias contextuales sin especificar producto
            if any(ref in message_lower for ref in self.config.CONTEXTUAL_REFS) and conversation_history:
                last_product = self._get_last_discussed_product(conversation_history)
                if last_product:
                    entities["producto_especifico"] = last_product
    
    def _extract_spec_action(self, message_lower: str, entities: Dict[str, Any]) -> None:
        """Detectar solicitud de especificaciones"""
        if any(pattern in message_lower for pattern in self.config.SPEC_PATTERNS):
            entities["accion"] = "ver_especificaciones"
    
    def _extract_recommend_action(self, message_lower: str, entities: Dict[str, Any]) -> None:
        """Detectar solicitud de recomendación"""
        if any(pattern in message_lower for pattern in self.config.RECOMMEND_PATTERNS):
            entities["accion"] = "recomendar"
    
    def _extract_specific_product_name(self, message_lower: str, entities: Dict[str, Any]) -> None:
        """Extraer nombre específico del producto mencionado"""
        for pattern in self.config.SPECIFIC_PRODUCT_PATTERNS:
            match = re.search(pattern, message_lower)
            if match:
                entities["producto_especifico"] = match.group().strip()
                break
    
    def _get_last_discussed_product(self, conversation_history: List[Dict[str, Any]]) -> Optional[str]:
        """Obtener el último producto específico discutido en la conversación"""
        for conv in reversed(conversation_history):
            # Si mostró especificaciones, extraer el producto del mensaje del bot
            if "📋 **Especificaciones Técnicas -" in conv.get("bot_response", ""):
                match = re.search(r"📋 \*\*Especificaciones Técnicas - (.+?)\*\*", conv["bot_response"])
                if match:
                    return match.group(1).strip()
            
            # Si el usuario mencionó un producto específico
            entities = conv.get("entities", {})
            if entities.get("producto_especifico"):
                return entities["producto_especifico"]
        
        return None
    
    def should_show_products(self, entities: Dict[str, Any], conversation_history: List[Dict[str, Any]]) -> bool:
        """Determinar si debe buscar y mostrar productos"""
        # Si hay acción específica de ver especificaciones
        if entities.get("accion") == "ver_especificaciones":
            return True
        
        # Si hay acción de agregar al carrito
        if entities.get("accion") == "agregar_carrito":
            return True
        
        # Si menciona un producto específico
        if entities.get("producto_especifico"):
            return True
        
        # Si menciona una categoría de producto
        if entities.get("producto"):
            return True
        
        # Si menciona una marca
        if entities.get("marca"):
            return True
        
        # Si menciona presupuesto
        if entities.get("presupuesto"):
            return True
        
        # Si menciona caso de uso específico
        if entities.get("uso"):
            return True
            
        return False
    
    def get_search_query_from_context(self, entities: Dict[str, Any], conversation_history: List[Dict[str, Any]]) -> str:
        """Obtener consulta de búsqueda basada en entidades y contexto"""
        search_terms = []
        
        # Agregar producto específico si existe
        if entities.get("producto_especifico"):
            return entities["producto_especifico"]
        
        # Agregar categoría de producto
        if entities.get("producto"):
            search_terms.append(entities["producto"])
        
        # Agregar marca
        if entities.get("marca"):
            search_terms.append(entities["marca"])
        
        # Agregar caso de uso
        if entities.get("uso"):
            if entities["uso"] == "gaming":
                search_terms.append("gaming")
            elif entities["uso"] == "universidad":
                search_terms.append("estudiante")
            elif entities["uso"] == "trabajo":
                search_terms.append("empresarial")
        
        # Si no hay términos específicos, usar término genérico
        if not search_terms:
            search_terms.append("laptop")
        
        return " ".join(search_terms)
