# filepath: backend/app/chatbot/utils/response_formatter.py
"""
Formateador de respuestas del chatbot
Maneja la generación de respuestas formateadas para productos y especificaciones
"""
import logging
from typing import List, Optional
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
