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
        
        # PRIMERO: Detectar solicitudes de recomendación (tienen prioridad)
        self._extract_recommend_action(message_lower, entities)
        
        # SEGUNDO: Si no es recomendación, verificar si es pregunta tecnológica general
        if not entities.get("accion"):
            self._extract_tech_question(message_lower, entities)
        
        # TERCERO: Si no es recomendación ni pregunta tech, verificar comparaciones específicas
        if not entities.get("accion"):
            self._extract_comparison_entities(message_lower, entities)
        
        # CUARTO: Extraer otros datos si no es una acción específica
        if not entities.get("accion") or entities.get("accion") in ["buscar_productos", "pregunta_tecnologica"]:
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
            
            # Extraer nombre específico de producto mencionado
            self._extract_specific_product_name(message_lower, entities)
        else:
            pass 
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
        """Detectar solicitudes de especificaciones, incluyendo referencias contextuales"""
        
        # Verificar patrones básicos de especificaciones
        for pattern in self.config.SPEC_PATTERNS:
            if pattern.lower() in message_lower:
                entities["accion"] = "ver_especificaciones"
                logger.info("Detectada solicitud de especificaciones básica")
                break
        
        # Verificar patrones contextuales para especificaciones (la segunda, el primero, etc.)
        if entities.get("accion") != "ver_especificaciones":
            for pattern in self.config.CONTEXTUAL_SPEC_PATTERNS:
                if re.search(pattern, message_lower):
                    entities["accion"] = "ver_especificaciones"
                    entities["referencia_contextual"] = True
                    
                    # Extraer qué número de producto se refiere (mejorado para números directos)
                    if re.search(r"(?:la\s+)?segunda?|(?:\s|^)2(?:\s|$)", message_lower):
                        entities["numero_producto"] = 2
                    elif re.search(r"(?:la\s+)?primera?|(?:el\s+)?primero|(?:\s|^)1(?:\s|$)", message_lower):
                        entities["numero_producto"] = 1
                    elif re.search(r"(?:la\s+)?tercera?|(?:el\s+)?tercero|(?:\s|^)3(?:\s|$)", message_lower):
                        entities["numero_producto"] = 3
                    else:
                        # Fallback: buscar cualquier número del 1-5
                        number_match = re.search(r"(?:\s|^)([1-5])(?:\s|$)", message_lower)
                        if number_match:
                            entities["numero_producto"] = int(number_match.group(1))
                    
                    logger.info(f"Detectada solicitud de especificaciones contextual - Producto #{entities.get('numero_producto', 'N/A')}")
                    break

    def _extract_recommend_action(self, message_lower: str, entities: Dict[str, Any]) -> None:
        """Detectar solicitudes de recomendación inteligente"""
        # Verificar si el mensaje coincide con patrones de recomendación
        for pattern in self.config.RECOMMENDATION_QUERY_PATTERNS:
            if re.search(pattern, message_lower):
                entities["accion"] = "recomendar_categoria"
                
                # Extraer la categoría mencionada en el patrón
                category_match = re.search(r"(laptop|pc|computadora|equipo)s?", message_lower)
                if category_match:
                    category = category_match.group(1)
                    if category in ["laptop", "computadora"]:
                        entities["categoria"] = "laptop"
                    elif category in ["pc", "equipo"]:
                        entities["categoria"] = "pc"
                    else:
                        entities["categoria"] = category
                
                logger.info(f"Detectada solicitud de recomendación para categoría: {entities.get('categoria', 'general')}")
                break

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
        
        # PRIORITY 1: Si es una pregunta tecnológica general, NO mostrar productos
        if entities.get("accion") == "pregunta_tecnologica":
            return False
        
        # PRIORITY 2: Si hay acción específica de ver especificaciones
        if entities.get("accion") == "ver_especificaciones":
            return True
        
        # PRIORITY 3: Si hay acción de agregar al carrito
        if entities.get("accion") == "agregar_carrito":
            return True
        
        # PRIORITY 4: Si hay comparación específica de productos/marcas
        if entities.get("accion") == "comparar_productos" and (entities.get("productos_a_comparar") or entities.get("marcas_a_comparar")):
            return True
            
        # PRIORITY 5: Si es recomendación de categoría específica (no pregunta general)
        if entities.get("accion") == "recomendar_categoria":
            return True
        
        # PRIORITY 6: Si menciona un producto específico
        if entities.get("producto_especifico"):
            return True
        
        # PRIORITY 7: Si menciona una categoría de producto (pero no es pregunta tech)
        if entities.get("producto"):
            return True
        
        # PRIORITY 8: Si menciona una marca
        if entities.get("marca"):
            return True
        
        # PRIORITY 9: Si menciona presupuesto
        if entities.get("presupuesto"):
            return True
            
        # PRIORITY 10: Si menciona caso de uso específico
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
    
    def _extract_comparison_entities(self, message_lower: str, entities: Dict[str, Any]) -> None:
        """Detectar intención de comparación y extraer productos/atributos/marcas."""
        is_comparison_intent = False
        product_names_to_compare = []
        attributes_to_compare = []
        marcas_to_compare = []

        for pattern in self.config.COMPARISON_PATTERNS:
            match = re.search(pattern, message_lower)
            if match:
                is_comparison_intent = True
                # Extraer nombres de productos/marcas de los grupos de captura
                if len(match.groups()) >= 2:
                    # Limpiar y añadir los elementos a comparar
                    item1_full = match.group(1).strip()
                    item2_full = match.group(2).strip()
                    
                    # Intentar identificar si son marcas o nombres de producto más específicos
                    # Esto es una heurística y podría mejorarse
                    item1_is_brand = any(brand.lower() == item1_full.lower() for brand in self.config.BRANDS)
                    item2_is_brand = any(brand.lower() == item2_full.lower() for brand in self.config.BRANDS)

                    if item1_is_brand and item2_is_brand:
                        marcas_to_compare.extend([item1_full, item2_full])
                    elif item1_is_brand and not item2_is_brand: # Ej: "compara Asus con Dell XPS"
                        marcas_to_compare.append(item1_full)
                        product_names_to_compare.append(item2_full)
                    elif not item1_is_brand and item2_is_brand: # Ej: "compara Dell XPS con Asus"
                        product_names_to_compare.append(item1_full)
                        marcas_to_compare.append(item2_full)
                    else: # Asumir que son nombres de producto
                        product_names_to_compare.extend([item1_full, item2_full])
                
                # Extraer atributos de comparación del resto del mensaje (si no están en los grupos)
                # o de todo el mensaje si el patrón es simple como "vs"
                text_for_attributes = message_lower
                if len(match.groups()) >=2: # Si los productos estaban en grupos, buscar atributos en el resto
                    text_for_attributes = message_lower.replace(match.group(0), "").strip()
                
                for attr, attr_patterns in self.config.COMPARISON_ATTRIBUTE_PATTERNS.items():
                    for p_attr in attr_patterns:
                        if re.search(p_attr, text_for_attributes) or re.search(p_attr, message_lower): # Buscar en el resto o en todo
                            attributes_to_compare.append(attr)
                break 

        if is_comparison_intent:
            entities["accion"] = "comparar_productos"
            entities["productos_a_comparar"] = list(set(product_names_to_compare))
            entities["marcas_a_comparar"] = list(set(marcas_to_compare))
            entities["atributos_a_comparar"] = list(set(attributes_to_compare))

            if not entities["atributos_a_comparar"] and (entities["productos_a_comparar"] or entities["marcas_a_comparar"]):
                entities["atributos_a_comparar"] = ["caracteristicas"] # Default

            # Si solo se mencionan marcas y no productos específicos, priorizar marcas.
            if entities["marcas_a_comparar"] and not entities["productos_a_comparar"]:
                 # Podríamos querer buscar productos de estas marcas.
                 # Por ahora, el servicio de producto decidirá cómo manejar esto.
                 pass
    
    def _extract_tech_question(self, message_lower: str, entities: Dict[str, Any]) -> None:
        """Detectar preguntas tecnológicas generales (no sobre productos específicos)"""
          # Patrones para preguntas tecnológicas generales
        tech_question_patterns = [
            # Preguntas generales por categoría (que X es mejor)
            r"(?:qu[eé]|cu[aá]l)\s+laptop\s+es\s+mejor",                                # "que laptop es mejor"
            r"(?:qu[eé]|cu[aá]l)\s+pc\s+es\s+mejor",                                    # "que pc es mejor"
            r"(?:qu[eé]|cu[aá]l)\s+monitor\s+es\s+mejor",                               # "que monitor es mejor"
            r"(?:qu[eé]|cu[aá]l)\s+pantalla\s+es\s+mejor",                              # "que pantalla es mejor"
            r"(?:qu[eé]|cu[aá]l)\s+teclado\s+es\s+mejor",                               # "que teclado es mejor"
            r"(?:qu[eé]|cu[aá]l)\s+mouse\s+es\s+mejor",                                 # "que mouse es mejor"
            r"(?:qu[eé]|cu[aá]l)\s+procesador\s+es\s+mejor",                            # "que procesador es mejor"
            r"(?:qu[eé]|cu[aá]l)\s+tarjeta\s+(?:gráfica|de\s+video)\s+es\s+mejor",     # "que tarjeta grafica es mejor"
            
            # Comparaciones generales PC vs Laptop
            r"(?:qu[eé]|cu[aá]l)\s+es\s+mejor\s+(?:una\s+)?laptop\s+o\s+(?:una\s+)?pc",  # "que es mejor una laptop o una pc"
            r"(?:qu[eé]|cu[aá]l)\s+es\s+mejor\s+(?:una\s+)?pc\s+o\s+(?:una\s+)?laptop",  # "que es mejor una pc o una laptop"
            r"laptop\s+o\s+pc\s+(?:para|qu[eé])",                                        # "laptop o pc para gaming"
            r"pc\s+o\s+laptop\s+(?:para|qu[eé])",                                        # "pc o laptop para trabajo"
            r"diferencia\s+entre\s+laptop\s+y\s+pc",                                     # "diferencia entre laptop y pc"
            r"diferencia\s+entre\s+pc\s+y\s+laptop",                                     # "diferencia entre pc y laptop"
            r"ventajas?\s+(?:de\s+)?laptop\s+(?:vs?|o)\s+pc",                           # "ventajas de laptop vs pc"
            r"ventajas?\s+(?:de\s+)?pc\s+(?:vs?|o)\s+laptop",                           # "ventajas de pc vs laptop"
            r"(?:qu[eé]|cu[aá]l)\s+conviene\s+más\s+laptop\s+o\s+pc",                   # "que conviene más laptop o pc"
              # Comparaciones de componentes y marcas
            r"(?:qu[eé]|cu[aá]l)\s+es\s+mejor\s+amd\s+o\s+intel",                      # "cual es mejor amd o intel"
            r"(?:qu[eé]|cu[aá]l)\s+es\s+mejor\s+intel\s+o\s+amd",                      # "cual es mejor intel o amd"
            r"diferencia\s+entre\s+amd\s+e?\s*intel",                                   # "diferencia entre amd e intel"
            r"diferencia\s+entre\s+intel\s+y\s+amd",                                    # "diferencia entre intel y amd"
            r"amd\s+vs?\s+intel",                                                       # "amd vs intel"
            r"intel\s+vs?\s+amd",                                                       # "intel vs amd"
            r"(?:qu[eé]|cu[aá]l)\s+es\s+mejor\s+nvidia\s+o\s+amd",                     # "cual es mejor nvidia o amd"
            r"(?:qu[eé]|cu[aá]l)\s+es\s+mejor\s+amd\s+o\s+nvidia",                     # "cual es mejor amd o nvidia"
            r"nvidia\s+vs?\s+amd",                                                      # "nvidia vs amd"
            
            # Comparaciones de marcas de fabricantes (preguntas generales)
            r"(?:qu[eé]|cu[aá]l)\s+es\s+mejor\s+asus\s+o\s+lenovo",                    # "que es mejor asus o lenovo"
            r"(?:qu[eé]|cu[aá]l)\s+es\s+mejor\s+lenovo\s+o\s+asus",                    # "que es mejor lenovo o asus"
            r"(?:qu[eé]|cu[aá]l)\s+es\s+mejor\s+hp\s+o\s+dell",                        # "que es mejor hp o dell"
            r"(?:qu[eé]|cu[aá]l)\s+es\s+mejor\s+dell\s+o\s+hp",                        # "que es mejor dell o hp"
            r"(?:qu[eé]|cu[aá]l)\s+es\s+mejor\s+asus\s+o\s+hp",                        # "que es mejor asus o hp"
            r"(?:qu[eé]|cu[aá]l)\s+es\s+mejor\s+hp\s+o\s+asus",                        # "que es mejor hp o asus"            r"(?:qu[eé]|cu[aá]l)\s+es\s+mejor\s+lenovo\s+o\s+dell",                    # "que es mejor lenovo o dell"
            r"(?:qu[eé]|cu[aá]l)\s+es\s+mejor\s+dell\s+o\s+lenovo",                    # "que es mejor dell o lenovo"
            r"(?:qu[eé]|cu[aá]l)\s+es\s+mejor\s+lenovo\s+o\s+hp",                      # "que es mejor lenovo o hp"
            r"(?:qu[eé]|cu[aá]l)\s+es\s+mejor\s+hp\s+o\s+lenovo",                      # "que es mejor hp o lenovo"
            r"diferencia\s+entre\s+asus\s+y\s+lenovo",                                  # "diferencia entre asus y lenovo"
            r"diferencia\s+entre\s+lenovo\s+y\s+asus",                                  # "diferencia entre lenovo y asus"            r"diferencia\s+entre\s+hp\s+y\s+dell",                                      # "diferencia entre hp y dell"
            r"diferencia\s+entre\s+dell\s+y\s+hp",                                      # "diferencia entre dell y hp"
            r"diferencia\s+entre\s+lenovo\s+y\s+hp",                                    # "diferencia entre lenovo y hp"
            r"diferencia\s+entre\s+hp\s+y\s+lenovo",                                    # "diferencia entre hp y lenovo"
            r"asus\s+vs?\s+lenovo",                                                     # "asus vs lenovo"
            r"lenovo\s+vs?\s+asus",                                                     # "lenovo vs asus"            r"hp\s+vs?\s+dell",                                                         # "hp vs dell"
            r"dell\s+vs?\s+hp",                                                         # "dell vs hp"
            r"lenovo\s+vs?\s+hp",                                                       # "lenovo vs hp"
            r"hp\s+vs?\s+lenovo",                                                       # "hp vs lenovo"
            
            # Preguntas sobre tipos de componentes
            r"(?:qu[eé]|cu[aá]l)\s+es\s+mejor\s+ssd\s+o\s+hdd",                        # "cual es mejor ssd o hdd"
            r"(?:qu[eé]|cu[aá]l)\s+es\s+mejor\s+hdd\s+o\s+ssd",                        # "cual es mejor hdd o ssd"
            r"diferencia\s+entre\s+ssd\s+y\s+hdd",                                      # "diferencia entre ssd y hdd"
            r"ssd\s+vs?\s+hdd",                                                         # "ssd vs hdd"
            
            # Preguntas sobre sistemas operativos
            r"(?:qu[eé]|cu[aá]l)\s+es\s+mejor\s+windows\s+o\s+linux",                  # "cual es mejor windows o linux"
            r"(?:qu[eé]|cu[aá]l)\s+es\s+mejor\s+linux\s+o\s+windows",                  # "cual es mejor linux o windows"
            r"diferencia\s+entre\s+windows\s+y\s+linux",                               # "diferencia entre windows y linux"
        ]
        
        for pattern in tech_question_patterns:
            if re.search(pattern, message_lower):
                entities["accion"] = "pregunta_tecnologica"                # Clasificar el tipo de pregunta para respuestas más específicas
                if "laptop.*es.*mejor" in pattern and not ("pc" in pattern or "computadora" in pattern):
                    entities["tipo_pregunta"] = "best_laptop"
                elif "pc.*es.*mejor" in pattern:
                    entities["tipo_pregunta"] = "best_pc"
                elif "monitor.*es.*mejor" in pattern or "pantalla.*es.*mejor" in pattern:
                    entities["tipo_pregunta"] = "best_monitor"
                elif "teclado.*es.*mejor" in pattern:
                    entities["tipo_pregunta"] = "best_keyboard"
                elif "mouse.*es.*mejor" in pattern:
                    entities["tipo_pregunta"] = "best_mouse"
                elif "procesador.*es.*mejor" in pattern:
                    entities["tipo_pregunta"] = "best_processor"
                elif "tarjeta" in pattern and ("gráfica" in pattern or "video" in pattern):
                    entities["tipo_pregunta"] = "best_gpu"
                elif "laptop" in pattern and "pc" in pattern:
                    entities["tipo_pregunta"] = "laptop_vs_pc"
                elif "amd" in pattern and "intel" in pattern:
                    entities["tipo_pregunta"] = "amd_vs_intel"
                elif "nvidia" in pattern:
                    entities["tipo_pregunta"] = "gpu_comparison"
                elif "ssd" in pattern and "hdd" in pattern:
                    entities["tipo_pregunta"] = "storage_comparison"
                elif "windows" in pattern or "linux" in pattern:
                    entities["tipo_pregunta"] = "os_comparison"
                elif any(brand in pattern for brand in ["asus", "lenovo", "hp", "dell"]):
                    entities["tipo_pregunta"] = "brand_comparison"
                else:
                    entities["tipo_pregunta"] = "general_tech"
                
                logger.info(f"Detectada pregunta tecnológica general: {entities['tipo_pregunta']}")
                break