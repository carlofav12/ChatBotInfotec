# filepath: backend/app/chatbot/utils/response_formatter_fixed.py
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
            return "❌ No se encontraron productos que coincidan con tu búsqueda. ¿Podrías ser más específico? 🤔"
        
        response = f"🛍️ Encontré {len(products)} producto(s) para ti:\n\n"
        
        for i, product in enumerate(products[:10]):  # Limitar a 10 productos
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
        
        response += "💡 ¿Te interesa alguno en particular? ¡Puedo darte más detalles o agregarlo al carrito! 😊"
        return response
    
    def generate_specification_response(self, product: ProductModel) -> str:
        """Generar respuesta con especificaciones del producto"""
        try:
            if not product:
                return "❌ No se encontró información del producto especificado."
            
            spec_response = f"📋 **Especificaciones de {product.name}**\n\n"
            
            # Precio
            spec_response += f"💰 **Precio:** S/ {product.price:.2f}\n"
            
            # Marca y modelo
            spec_response += f"🏢 **Marca:** {product.brand}\n"
            
            # Extracción de especificaciones del producto
            if hasattr(product, 'specifications') and product.specifications:
                # Si el producto tiene especificaciones como atributo
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
                    spec_response += f"🖥️ **Sistema Operativo:** {os_info}\n"
                
                # GPU
                gpu_info = self._extract_gpu_info(name_lower)
                if gpu_info:
                    spec_response += f"🎮 **Tarjeta Gráfica:** {gpu_info}\n"
                
                # Características especiales
                features = self._extract_special_features(name_lower)
                if features:
                    spec_response += f"✨ **Características:** {features}\n"
            
            spec_response += f"\n📦 **Stock:** {product.stock_quantity} unidades\n"
            spec_response += f"⭐ **Rating:** {product.rating}/5\n\n"
            spec_response += "💡 ¿Te interesa este producto? ¡Puedo agregarlo al carrito! 🛒"
            
            return spec_response
            
        except Exception as e:
            logger.error(f"Error generando especificaciones: {e}")
            return f"❌ Error al obtener las especificaciones de {product.name if product else 'el producto'}."
    
    def _extract_processor_info(self, name_lower: str) -> str:
        """Extraer información del procesador del nombre del producto"""
        processor_patterns = {
            "intel i9": "Intel Core i9",
            "intel i7": "Intel Core i7", 
            "intel i5": "Intel Core i5",
            "intel i3": "Intel Core i3",
            "amd ryzen 9": "AMD Ryzen 9",
            "amd ryzen 7": "AMD Ryzen 7",
            "amd ryzen 5": "AMD Ryzen 5",
            "amd ryzen 3": "AMD Ryzen 3",
            "intel celeron": "Intel Celeron",
            "intel pentium": "Intel Pentium"
        }
        
        for pattern, value in processor_patterns.items():
            if pattern in name_lower:
                # Tratar de extraer generación
                import re
                gen_match = re.search(r'(\d+)(?:th|st|nd|rd)?\s*gen', name_lower)
                if gen_match:
                    return f"{value} {gen_match.group(1)}ª Gen"
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
        
        return ""
    
    def _extract_display_info(self, name_lower: str) -> str:
        """Extraer información de pantalla del nombre del producto"""
        display_patterns = {
            "15.6": "15.6 pulgadas",
            "17.3": "17.3 pulgadas",
            "14": "14 pulgadas",
            "13.3": "13.3 pulgadas",
            "1920x1080": "Full HD (1920x1080)",
            "full hd": "Full HD (1920x1080)",
            "4k": "4K UHD",
            "uhd": "4K UHD"
        }
        
        for pattern, value in display_patterns.items():
            if pattern in name_lower:
                return value
        
        return ""
    
    def _extract_os_info(self, name_lower: str) -> str:
        """Extraer información del sistema operativo del nombre del producto"""
        if "windows 11" in name_lower:
            return "Windows 11"
        elif "windows 10" in name_lower:
            return "Windows 10"
        elif "ubuntu" in name_lower or "linux" in name_lower:
            return "Linux/Ubuntu"
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
        
        # Pantalla táctil
        if "táctil" in name_lower or "touch" in name_lower:
            features.append("Pantalla táctil")
        
        # Retroiluminación
        if "retroiluminado" in name_lower or "backlit" in name_lower:
            features.append("Teclado retroiluminado")
        
        # Convertible
        if "convertible" in name_lower or "2 en 1" in name_lower:
            features.append("Convertible 2 en 1")
        
        # Gaming
        if "gaming" in name_lower or "gamer" in name_lower:
            features.append("Orientado a gaming")
        
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
            for attr in attributes:
                if attr in product and attr != 'precio':
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
