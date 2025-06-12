# filepath: backend/app/chatbot/utils/response_formatter_temp.py
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
        
    def generate_product_specifications(self, product: ProductModel, include_header: bool = True) -> str:
        """Generar especificaciones detalladas de un producto"""
        spec_response = ""
        
        # Agregar encabezado si es necesario
        if include_header:
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
        
        # Extracción de especificaciones del producto
        if hasattr(product, 'specifications') and product.specifications:        # Si el producto tiene especificaciones como atributo
            if isinstance(product.specifications, dict):
                for key, value in product.specifications.items():
                    if key and value and key.lower() not in ["id", "product_id"]:
                        spec_response += f"**{key.replace('_', ' ').capitalize()}:** {value}\n"
            elif isinstance(product.specifications, str):
                spec_response += f"**Especificaciones:** {product.specifications}\n"
        else:
            # Extracción basada en el nombre del producto
            name_lower = product.name.lower()
            
            # Procesador
            processor_info = self._extract_processor_info(name_lower)
            if processor_info:
                spec_response += f"⚡ **Procesador:** {processor_info}\n"
            
            # Memoria RAM
            ram_info = self._extract_ram_info(name_lower)
            if ram_info:
                spec_response += f"🧠 **Memoria RAM:** {ram_info}\n"
            
            # Almacenamiento
            storage_info = self._extract_storage_info(name_lower)
            if storage_info:
                spec_response += f"💾 **Almacenamiento:** {storage_info}\n"
            
            # Pantalla
            display_info = self._extract_display_info(name_lower)
            if display_info:
                spec_response += f"🖥️ **Pantalla:** {display_info}\n"
            
            # Sistema operativo
            os_info = self._extract_os_info(name_lower)
            if os_info:
                spec_response += f"🌐 **Sistema operativo:** {os_info}\n"
            
            # Tarjeta gráfica
            gpu_info = self._extract_gpu_info(name_lower)
            if gpu_info:
                spec_response += f"🎮 **Tarjeta gráfica:** {gpu_info}\n"
            
            # Características especiales
            special_features = self._extract_special_features(name_lower)
            if special_features:
                spec_response += f"✨ **Características especiales:** {special_features}\n"
        
        spec_response += f"\n💡 **¿Te interesa este modelo? ¡Puedo agregarlo a tu carrito!**"
        
        return spec_response
    
    def _extract_processor_info(self, name_lower: str) -> str:
        """Extraer información del procesador del nombre del producto"""
        processor_patterns = {
            "ryzen 5": "AMD Ryzen 5",
            "ryzen 7": "AMD Ryzen 7",
            "ryzen 9": "AMD Ryzen 9",
            "i3": "Intel Core i3",
            "i5": "Intel Core i5",
            "i7": "Intel Core i7",
            "i9": "Intel Core i9",
            "core ultra 5": "Intel Core Ultra 5",
            "core ultra 7": "Intel Core Ultra 7",
            "n4500": "Intel Celeron N4500"
        }
        
        for pattern, value in processor_patterns.items():
            if pattern in name_lower:
                # Buscar el modelo específico
                import re
                model_match = re.search(r'(\d{4,5}[a-z]*)', name_lower)
                if model_match and pattern in ["i3", "i5", "i7", "i9", "ryzen 5", "ryzen 7", "ryzen 9"]:
                    return f"{value} {model_match.group(1)}"
                return value
        
        return ""
    
    def _extract_ram_info(self, name_lower: str) -> str:
        """Extraer información de RAM del nombre del producto"""
        ram_patterns = {
            "8gb": "8GB",
            "16gb": "16GB",
            "32gb": "32GB",
            "64gb": "64GB"
        }
        
        for pattern, value in ram_patterns.items():
            if pattern in name_lower:
                # Tratar de extraer tipo de memoria (DDR4, DDR5)
                import re
                ddr_match = re.search(r'(ddr\d)', name_lower)
                if ddr_match:
                    return f"{value} {ddr_match.group(1).upper()}"
                return value
        
        return ""
    
    def _extract_storage_info(self, name_lower: str) -> str:
        """Extraer información de almacenamiento del nombre del producto"""
        storage_patterns = {
            "256gb ssd": "256GB SSD",
            "512gb ssd": "512GB SSD",
            "1tb ssd": "1TB SSD",
            "2tb ssd": "2TB SSD"
        }
        
        for pattern, value in storage_patterns.items():
            if pattern in name_lower:
                return value
        
        # Búsqueda más flexible
        import re
        storage_match = re.search(r'(\d+(?:\.\d+)?(?:gb|tb))\s*ssd', name_lower)
        if storage_match:
            return f"{storage_match.group(1).upper()} SSD"
        
        return ""
    
    def _extract_display_info(self, name_lower: str) -> str:
        """Extraer información de pantalla del nombre del producto"""
        display_info = ""
        
        # Tamaño de pantalla
        import re
        size_match = re.search(r'(\d{2}(?:\.\d)?)"', name_lower)
        if size_match:
            display_info = f"{size_match.group(1)} pulgadas"
        elif "15.6" in name_lower:
            display_info = "15.6 pulgadas"
        elif "14" in name_lower and "pulgadas" not in name_lower:
            display_info = "14 pulgadas"
        elif "16" in name_lower and "pulgadas" not in name_lower:
            display_info = "16 pulgadas"
        elif "13" in name_lower and "pulgadas" not in name_lower:
            display_info = "13 pulgadas"
        
        # Resolución
        if "fhd" in name_lower or "full hd" in name_lower:
            if display_info:
                display_info += ", "
            display_info += "Full HD (1920x1080)"
        elif "uhd" in name_lower or "4k" in name_lower:
            if display_info:
                display_info += ", "
            display_info += "Ultra HD 4K"
        elif "qhd" in name_lower or "2k" in name_lower:
            if display_info:
                display_info += ", "
            display_info += "QHD (2560x1440)"
        
        # Características adicionales
        if "táctil" in name_lower or "touch" in name_lower:
            if display_info:
                display_info += ", "
            display_info += "táctil"
        
        if "ips" in name_lower:
            if display_info:
                display_info += ", "
            display_info += "IPS"
        
        if "144hz" in name_lower:
            if display_info:
                display_info += ", "
            display_info += "144Hz"
        elif "120hz" in name_lower:
            if display_info:
                display_info += ", "
            display_info += "120Hz"
        
        return display_info
    
    def _extract_os_info(self, name_lower: str) -> str:
        """Extraer información del sistema operativo del nombre del producto"""
        if "windows 11" in name_lower:
            return "Windows 11"
        elif "windows 10" in name_lower:
            return "Windows 10"
        elif "windows" in name_lower:
            return "Windows"
        elif "macos" in name_lower or "mac os" in name_lower:
            return "macOS"
        elif "linux" in name_lower:
            return "Linux"
        elif "sin sistema operativo" in name_lower or "free dos" in name_lower:
            return "Sin sistema operativo"
        return ""
    
    def _extract_gpu_info(self, name_lower: str) -> str:
        """Extraer información de la tarjeta gráfica del nombre del producto"""
        gpu_patterns = {
            "rtx 4090": "NVIDIA GeForce RTX 4090",
            "rtx 4080": "NVIDIA GeForce RTX 4080",
            "rtx 4070": "NVIDIA GeForce RTX 4070",
            "rtx 4060": "NVIDIA GeForce RTX 4060",
            "rtx 4050": "NVIDIA GeForce RTX 4050",
            "rtx 3090": "NVIDIA GeForce RTX 3090",
            "rtx 3080": "NVIDIA GeForce RTX 3080",
            "rtx 3070": "NVIDIA GeForce RTX 3070",
            "rtx 3060": "NVIDIA GeForce RTX 3060",
            "rtx 3050": "NVIDIA GeForce RTX 3050",
            "gtx 1660": "NVIDIA GeForce GTX 1660",
            "gtx 1650": "NVIDIA GeForce GTX 1650",
            "gtx 1050": "NVIDIA GeForce GTX 1050",
            "radeon 6700": "AMD Radeon RX 6700",
            "radeon 6600": "AMD Radeon RX 6600",
            "radeon vega": "AMD Radeon Vega",
            "intel arc": "Intel Arc",
            "intel iris xe": "Intel Iris Xe",
            "intel uhd": "Intel UHD Graphics"
        }
        
        for pattern, value in gpu_patterns.items():
            if pattern in name_lower:
                return value
        
        # Detectar integradas genéricas
        if "gráficos integrados" in name_lower or "graphics integrated" in name_lower:
            return "Gráficos integrados"
        
        return ""
    
    def _extract_special_features(self, name_lower: str) -> str:
        """Extraer características especiales del nombre del producto"""
        features = []
        
        # Gaming features
        if "gaming" in name_lower or "gamer" in name_lower:
            features.append("Optimizado para gaming")
        
        # Business features
        if "business" in name_lower or "profesional" in name_lower:
            features.append("Diseño profesional")
        
        # Convertible/2-in-1
        if "2 en 1" in name_lower or "2-en-1" in name_lower or "convertible" in name_lower or "2-in-1" in name_lower:
            features.append("Convertible 2-en-1")
        
        # Teclado retroiluminado
        if "retroiluminado" in name_lower or "backlit" in name_lower:
            features.append("Teclado retroiluminado")
        
        # Huella digital
        if "huella" in name_lower or "fingerprint" in name_lower:
            features.append("Lector de huella digital")
        
        # Peso ligero
        if "ultraligero" in name_lower or "ultra ligero" in name_lower or "lightweight" in name_lower:
            features.append("Diseño ultraligero")
        
        if features:
            return ", ".join(features)
          return ""
    
    def format_cart_response(self, result: Dict[str, Any]) -> str:
        """Formatear respuesta para agregar al carrito"""
        if not result or not isinstance(result, dict):
            return "❌ Ocurrió un error al procesar tu solicitud. Por favor, intenta nuevamente."
        
        if result.get("success"):
            product = result.get("product")
            product_name = product.name if product and hasattr(product, "name") else "Producto"
            quantity = result.get("quantity", 1)
            price = product.price if product and hasattr(product, "price") else 0
            subtotal = price * quantity
            
            response = f"""✅ **¡Producto agregado al carrito!**

🛒 **Detalle:**
• **{product_name}**
• Cantidad: {quantity}
• Precio unitario: S/ {price:.2f}
• Subtotal: S/ {subtotal:.2f}

"""
            # Agregar total del carrito si está disponible
            if result.get("cart_total"):
                response += f"💰 **Total del carrito:** S/ {result.get('cart_total'):.2f}\n\n"
            
            response += "¿Deseas agregar algo más o proceder al pago? 😊"
            return response
        else:
            error_message = result.get("message", "Error desconocido")
            return f"{error_message}\n\n¿Puedo ayudarte con algo más? 😊"

    def format_product_details(self, product: ProductModel) -> str:
        """Formatear detalles completos de un producto específico"""
        try:
            response = f"📋 **Especificaciones Técnicas - {product.name}**\n\n"
            
            # Información básica
            response += f"💰 **Precio:** S/ {product.price:.2f}\n"
            
            if hasattr(product, 'brand') and product.brand:
                response += f"🏷️ **Marca:** {product.brand}\n"
            
            if hasattr(product, 'rating') and product.rating:
                response += f"⭐ **Rating:** {product.rating}/5\n"
              response += f"📦 **Stock:** {product.stock_quantity} unidades\n\n"
            
            # Especificaciones técnicas
            if hasattr(product, 'specifications') and product.specifications:
                response += "🔧 **Especificaciones Técnicas:**\n"
                if isinstance(product.specifications, dict):
                    for key, value in product.specifications.items():
                        if value:
                            response += f"• **{key.title()}:** {value}\n"
                elif isinstance(product.specifications, str):
                    response += f"• {product.specifications}\n"
                else:
                    response += f"• {str(product.specifications)}\n"
                response += "\n"
            
            # Descripción
            if hasattr(product, 'description') and product.description:
                response += f"📝 **Descripción:**\n{product.description}\n\n"
            
            response += "💡 ¿Te interesa este producto? ¡Puedo agregarlo al carrito! 😊"
            return response
            
        except Exception as e:
            logger.error(f"Error formateando detalles del producto: {e}")
            return ("📋 **Información del Producto - " + getattr(product, 'name', 'Producto') + "**\n\n" +
                   f"💰 Precio: S/ {getattr(product, 'price', 0):.2f}\n" +
                   f"📦 Stock: {getattr(product, 'stock_quantity', 0)} unidades\n\n" +
                   "💡 ¿Te interesa este producto? ¡Puedo agregarlo al carrito! 😊")

    def format_product_comparison(self, comparison_data: List[Dict[str, Any]], attributes: List[str]) -> str:
        """Formatear respuesta para comparación de productos"""
        if not comparison_data:
            return "❌ No pude encontrar productos para comparar. ¿Podrías especificar productos o marcas específicas?"
        
        response = f"📊 **Comparación de Productos** ({len(comparison_data)} productos)\n\n"
        
        # Mostrar comparación detallada
        for i, product in enumerate(comparison_data, 1):
            response += f"**{i}. {product.get('name', 'Producto')}**\n"
            
            # Mostrar precio siempre
            if 'precio' in product:
                response += f"• 💰 Precio: S/ {product['precio']}\n"
            
            # Mostrar otros atributos
            for attr in ["marca", "rating"] + attributes:
                if attr in product and product[attr] != "N/A" and attr != "precio":
                    value = product[attr]
                    if attr == "marca":
                        response += f"• 🏷️ Marca: {value}\n"
                    elif attr == "rating":
                        response += f"• ⭐ Rating: {value}/5\n"
                    else:
                        response += f"• {attr.title()}: {value}\n"
            
            response += "\n"
        
        response += "💡 ¿Te interesa alguno en particular? ¡Puedo darte más detalles! 😊"
        return response
