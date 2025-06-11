# filepath: backend/app/chatbot/utils/response_formatter.py
"""
Formateador de respuestas del chatbot
Maneja la generación de respuestas formateadas para productos y especificaciones
"""
import logging
from typing import List, Optional, Dict, Any
from app.models import Product as ProductModel
from ..core.config import ChatbotConfig

logger = logging.getLogger(__name__)

class ResponseFormatter:
    """Formatea las respuestas del chatbot"""
    
    def __init__(self):
        self.config = ChatbotConfig()
    
    def check_prepared_response(self, message: str) -> Optional[str]:
        """Verificar si el mensaje coincide con alguna respuesta preparada"""
        message_lower = message.lower()
        
        for category, info in self.config.PREPARED_RESPONSES.items():
            for pattern in info["patterns"]:
                if pattern in message_lower:
                    return info["response"]
        
        return None
    
    def generate_product_response(self, products: List[ProductModel], use_case: Optional[str] = None) -> str:
        """Generar respuesta con productos"""
        if not products:
            return "No encontré productos que coincidan con tu búsqueda. ¿Podrías darme más detalles sobre lo que buscas? 😊"
        
        # Mensaje personalizado según el caso de uso
        intro_messages = {
            "gaming": "🎮 ¡Perfecto para gaming! Aquí tienes las mejores opciones:",
            "universidad": "🎓 Ideales para tus estudios:",
            "trabajo": "💼 Excelentes para uso profesional:",
            "programacion": "👨‍💻 Perfectas para programación:",
            "basico": "💻 Ideales para uso básico:",
        }
        
        if use_case and use_case in intro_messages:
            intro = intro_messages[use_case]
        else:
            intro = f"Encontré {len(products)} opciones que podrían interesarte:"
        
        response = f"{intro}\n\n"
        
        # Mostrar hasta 3 productos principales
        for i, product in enumerate(products[:3]):
            try:
                # Calcular descuento si existe
                discount_info = ""
                if hasattr(product, 'original_price') and product.original_price and product.original_price > product.price:
                    discount = round((1 - product.price / product.original_price) * 100)
                    discount_info = f" 🏷️ **{discount}% DESC**"
                
                # Stock status
                stock_status = "✅ En stock" if product.stock_quantity > 5 else f"⚠️ Quedan {product.stock_quantity}"
                
                response += f"**{i+1}. {product.name}**\n"
                response += f"💰 **S/ {product.price:.2f}**{discount_info}\n"
                response += f"📦 {stock_status}\n\n"
                
            except Exception as e:
                logger.warning(f"Error formateando producto {product.id}: {e}")
                continue
        
        # Mensaje de seguimiento
        if len(products) > 3:
            response += f"💡 *Y {len(products) - 3} opciones más disponibles*\n\n"
        
        response += "¿Te interesa alguna opción específica? ¡Puedo darte más detalles o agregarlo al carrito! 😊"
        
        return response
    
    def generate_product_specifications(self, product: ProductModel) -> str:
        """Generar especificaciones detalladas de un producto"""
        spec_response = f"📋 **Especificaciones Técnicas - {product.name}**\n\n"
        
        # Precio y disponibilidad
        spec_response += f"💰 **Precio:** S/ {product.price:.2f}\n"
        if hasattr(product, 'original_price') and product.original_price and product.original_price > product.price:
            discount = round((1 - product.price / product.original_price) * 100)
            spec_response += f"🏷️ **Precio anterior:** S/ {product.original_price:.2f} ({discount}% de descuento)\n"
        
        spec_response += f"📦 **Stock:** {product.stock_quantity} unidades disponibles\n"
        spec_response += f"⭐ **Calificación:** {getattr(product, 'rating', 'N/A')}/5\n\n"
        
        # Marca y modelo
        spec_response += f"🏢 **Marca:** {product.brand}\n"
        
        # Descripción técnica (extraer specs desde el nombre)
        name_lower = product.name.lower()
        
        # Procesador
        self._add_processor_info(name_lower, spec_response)
        
        # Memoria RAM
        self._add_ram_info(name_lower, spec_response)
        
        # Almacenamiento
        self._add_storage_info(name_lower, spec_response)
        
        # Pantalla
        self._add_display_info(name_lower, spec_response)
        
        # Características especiales
        self._add_special_features(name_lower, spec_response)
        
        spec_response += f"\n💡 **¿Te interesa este modelo? ¡Puedo agregarlo a tu carrito!**"
        
        return spec_response
    
    def _add_processor_info(self, name_lower: str, spec_response: str) -> str:
        """Agregar información del procesador"""
        if "ryzen 5" in name_lower:
            spec_response += f"⚡ **Procesador:** AMD Ryzen 5\n"
        elif "ryzen 7" in name_lower:
            spec_response += f"⚡ **Procesador:** AMD Ryzen 7\n"
        elif "i3" in name_lower:
            spec_response += f"⚡ **Procesador:** Intel Core i3\n"
        elif "i5" in name_lower:
            spec_response += f"⚡ **Procesador:** Intel Core i5\n"
        elif "i7" in name_lower:
            spec_response += f"⚡ **Procesador:** Intel Core i7\n"
        return spec_response
    
    def _add_ram_info(self, name_lower: str, spec_response: str) -> str:
        """Agregar información de memoria RAM"""
        if "8gb" in name_lower:
            spec_response += f"🧠 **Memoria RAM:** 8GB\n"
        elif "16gb" in name_lower:
            spec_response += f"🧠 **Memoria RAM:** 16GB\n"
        elif "32gb" in name_lower:
            spec_response += f"🧠 **Memoria RAM:** 32GB\n"
        return spec_response
    
    def _add_storage_info(self, name_lower: str, spec_response: str) -> str:
        """Agregar información de almacenamiento"""
        if "256gb ssd" in name_lower:
            spec_response += f"💾 **Almacenamiento:** 256GB SSD\n"
        elif "512gb ssd" in name_lower:
            spec_response += f"💾 **Almacenamiento:** 512GB SSD\n"
        elif "1tb ssd" in name_lower:
            spec_response += f"💾 **Almacenamiento:** 1TB SSD\n"
        return spec_response
    
    def _add_display_info(self, name_lower: str, spec_response: str) -> str:
        """Agregar información de pantalla"""
        if "15.6" in name_lower:
            spec_response += f"🖥️ **Pantalla:** 15.6 pulgadas\n"
        elif "14" in name_lower:
            spec_response += f"🖥️ **Pantalla:** 14 pulgadas\n"
        elif "16" in name_lower:
            spec_response += f"🖥️ **Pantalla:** 16 pulgadas\n"
        
        if "fhd" in name_lower:
            spec_response += f"📺 **Resolución:** Full HD (1920x1080)\n"
        
        if "táctil" in name_lower or "touch" in name_lower:
            spec_response += f"👆 **Pantalla táctil:** Sí\n"
        
        return spec_response
    
    def _add_special_features(self, name_lower: str, spec_response: str) -> str:
        """Agregar características especiales"""
        if "gaming" in name_lower or "gamer" in name_lower:
            spec_response += f"🎮 **Gaming:** Optimizada para juegos\n"
        
        if "2 en 1" in name_lower or "2en1" in name_lower:
            spec_response += f"🔄 **Convertible:** Laptop 2 en 1\n"
        
        return spec_response
    
    def format_cart_response(self, cart_result: dict) -> str:
        """Formatear respuesta de agregar al carrito"""
        if not cart_result:
            return "❌ Hubo un error al procesar tu solicitud. Inténtalo nuevamente."
        
        if not cart_result.get("success", False):
            # Respuesta de error
            return cart_result.get("message", "❌ No se pudo agregar el producto al carrito.")
        
        # Respuesta exitosa
        product = cart_result.get("product")
        quantity = cart_result.get("quantity", 1)
        item_subtotal = cart_result.get("item_subtotal", 0)
        cart_total = cart_result.get("cart_total", 0)
        
        if not product:
            return "✅ Producto agregado al carrito exitosamente."
        
        response = f"🎉 **¡Excelente elección!**\n\n"
        response += f"✅ **{product.name}** agregado al carrito\n"
        response += f"📦 **Cantidad:** {quantity} unidad{'es' if quantity > 1 else ''}\n"
        response += f"💰 **Precio unitario:** S/ {product.price:.2f}\n"
        response += f"💵 **Subtotal:** S/ {item_subtotal:.2f}\n"
        
        if cart_total > 0:
            response += f"🛒 **Total del carrito:** S/ {cart_total:.2f}\n\n"
        
        response += "🔔 **¿Qué deseas hacer ahora?**\n"
        response += "• Ver más productos similares\n"
        response += "• Proceder al checkout\n"
        response += "• Seguir comprando\n\n"
        response += "¡Estoy aquí para ayudarte! 😊"
        
        return response

    def format_product_comparison(self, products_data: List[Dict[str, Any]], attributes_requested: List[str], original_query: str = "") -> str:
        """
        Formatea los datos de comparación de productos en una respuesta legible.
        products_data: Lista de diccionarios, cada uno representando un producto con sus atributos.
        attributes_requested: Lista de atributos que el usuario pidió comparar.
        original_query: La consulta original del usuario, para contexto.
        """
        if not products_data:
            return f"No pude encontrar información para los productos que mencionaste ({original_query}). ¿Podrías verificar los nombres o intentar con otros? 🤔"

        num_products = len(products_data)
        
        if original_query:
             response = f"Aquí tienes una comparación basada en tu consulta: '{original_query}':\n\n"
        else:
            response = "Aquí tienes la comparación de los productos:\n\n"


        if num_products == 1:
            response = f"Solo encontré un producto que coincide con tu solicitud de comparación: **{products_data[0].get('name', 'Producto Desconocido')}**.\n"
            response += "Aquí están sus detalles:\n"
            product = products_data[0]
            for key, value in product.items():
                if key not in ["id"]: 
                    response += f"  - **{key.replace('_', ' ').capitalize()}:** {value}\n"
            return response

        # Determinar los atributos a mostrar en la tabla
        # Usar los atributos solicitados, y si es "caracteristicas", usar todos los disponibles.
        # Siempre mostrar 'name' y 'price' como base.
        
        # Recopilar todos los atributos únicos presentes en los productos.
        all_keys_from_data = set()
        for p_data in products_data:
            all_keys_from_data.update(p_data.keys())
        
        # Atributos base que siempre intentamos mostrar primero
        base_attributes = ["price", "marca", "rating"] # rating y category pueden no estar siempre
        
        display_attributes_set = set()

        if "caracteristicas" in attributes_requested or not attributes_requested:
            # Mostrar un conjunto amplio de atributos
            display_attributes_set.update(base_attributes)
            # Añadir otros atributos comunes o todos los disponibles, excluyendo 'id' y 'name'
            for key in all_keys_from_data:
                if key not in ["id", "name"]:
                    display_attributes_set.add(key)
        else:
            # Mostrar solo los atributos solicitados, más los base
            display_attributes_set.update(base_attributes)
            for attr_req in attributes_requested:
                # El servicio ya debería haber mapeado/obtenido el atributo
                # Así que buscamos la clave tal como está en products_data
                if attr_req in all_keys_from_data:
                     display_attributes_set.add(attr_req)
                # Si el atributo solicitado no está en all_keys_from_data,
                # es porque el servicio no lo pudo encontrar/mapear. Se omitirá.

        # Ordenar los atributos para la tabla: base primero, luego el resto alfabéticamente
        sorted_display_attributes = [attr for attr in base_attributes if attr in display_attributes_set]
        sorted_display_attributes.extend(sorted([attr for attr in display_attributes_set if attr not in base_attributes]))


        # Crear la tabla Markdown
        headers = ["Características 📝"] + [p.get("name", f"Producto {i+1}")[:30] for i, p in enumerate(products_data)] # Limitar longitud de nombre
        response += "| " + " | ".join(headers) + " |\n"
        response += "|-" + "-|-".join(["-" * min(len(h), 30) for h in headers]) + "-|\n" # Limitar longitud de separador

        for attr_key in sorted_display_attributes:
            if attr_key in ["id", "name"]: # 'name' ya está en encabezados, 'id' no se muestra
                continue
            
            row_values = [attr_key.replace('_', ' ').capitalize()]
            for p_data in products_data:
                value = p_data.get(attr_key, "N/A")
                if isinstance(value, float) and attr_key == "price":
                    value = f"S/ {value:.2f}"
                elif isinstance(value, list): # Si un atributo es una lista
                    value = ", ".join(map(str,value))
                elif isinstance(value, dict): # Si es un dict
                    value = "; ".join([f"{k_}: {v_}" for k_,v_ in value.items()])

                row_values.append(str(value)[:30]) # Limitar longitud del valor en celda
            response += "| " + " | ".join(row_values) + " |\n"
        
        response += f"\nEspero que esta comparación de los {num_products} productos te sea útil. ¿Hay algo más en lo que pueda ayudarte? 😊"
        return response