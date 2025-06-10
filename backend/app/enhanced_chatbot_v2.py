# Enhanced chatbot with improved error handling and responses - NUEVA VERSION MEJORADA
import google.generativeai as genai
from typing import List, Dict, Tuple, Optional, Union, Any
from datetime import datetime
import logging
import json
import re
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, and_, func
from app.database import get_db, Product, Cart, User, Category, ChatSession, ChatMessage as DBChatMessage, cart_items
from app.models import Product as ProductModel, Cart as CartModel

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedInfotecChatbotV2:
    def __init__(self, api_key: str):
        """Inicializar el chatbot mejorado con flujo de conversación inteligente"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Información extendida de la empresa
        self.company_info = {
            "nombre": "GRUPO INFOTEC",
            "descripcion": "Empresa líder en tecnología y servicios informáticos en Perú",
            "especialidades": [
                "Computadoras de escritorio y laptops",
                "Equipos gaming de alta gama", 
                "Componentes PC (procesadores, tarjetas gráficas, memorias)",
                "Monitores y periféricos",
                "Soporte técnico especializado",
                "Servicio técnico autorizado",
                "Mantenimiento preventivo y correctivo"
            ],
            "servicios": [
                "Venta de equipos nuevos",
                "Equipos reacondicionados certificados",
                "Armado de PC personalizado",
                "Instalación y configuración",
                "Soporte técnico 24/7",
                "Garantía extendida",
                "Financiamiento disponible"
            ]
        }
        
        # Respuestas preparadas para preguntas comunes
        self.prepared_responses = {
            "envio": {
                "patterns": ["envío", "envio", "entrega", "llega", "cuándo llega", "tiempo entrega", "delivery"],
                "response": """📦 **Información de Envíos:**

🚀 **Lima Metropolitana:**
• Entrega en 24-48 horas laborables
• Gratis por compras mayores a S/150

🚚 **Provincias:**
• 3-5 días laborables
• Costo según destino (S/15-35)

💼 **Entrega Express:**
• Mismo día en Lima (zonas seleccionadas)
• Costo adicional: S/25

📍 **Recojo en tienda:**
• Gratis en nuestras 3 tiendas
• Disponible en 2-4 horas

¿Te gustaría conocer más detalles sobre alguna opción de envío?"""
            },
            "otros_modelos": {
                "patterns": ["otros modelos", "otras opciones", "más modelos", "diferentes modelos", "qué más tienen"],
                "response": """🔍 **¡Por supuesto! Tenemos una amplia variedad:**

💻 **Categorías disponibles:**
• Laptops Gaming (ASUS ROG, MSI, HP Omen)
• Laptops Empresariales (Dell Latitude, HP EliteBook) 
• Laptops Estudiantiles (Lenovo IdeaPad, ASUS VivoBook)
• Laptops 2-en-1 (HP Envy x360, Lenovo Yoga)
• All-in-One (HP, Dell, Lenovo)
• PCs Gaming personalizadas

🏷️ **Rangos de precio:**
• Básicas: S/800 - S/1,500
• Intermedias: S/1,500 - S/3,000  
• Premium: S/3,000 - S/8,000+

¿Qué tipo específico te interesa? Puedo mostrarte opciones según tu presupuesto y uso."""
            },
            "garantia": {
                "patterns": ["garantía", "garantia", "garantizada", "cobertura", "servicio técnico"],
                "response": """🛡️ **Garantía Grupo INFOTEC:**

✅ **Garantía del fabricante:**
• 1 año en todas las laptops nuevas
• 6 meses en equipos reacondicionados

🔧 **Servicio técnico especializado:**
• Diagnóstico gratuito
• Técnicos certificados
• Repuestos originales

📞 **Soporte técnico:**
• WhatsApp: +51 999-888-777
• Email: soporte@grupoinfotec.pe
• Horario: Lun-Sáb 8am-8pm

💡 **Garantía extendida disponible:**
• +1 año adicional por solo S/99
• Incluye mantenimiento preventivo

¿Necesitas más información sobre la garantía?"""
            },
            "financiamiento": {
                "patterns": ["financiamiento", "cuotas", "pagar en partes", "crédito", "facilidades"],
                "response": """💳 **Opciones de Financiamiento:**

🏦 **Tarjetas de crédito:**
• Hasta 24 cuotas sin intereses*
• Visa, Mastercard, American Express

💰 **Financiamiento directo:**
• Hasta 12 cuotas con tasa preferencial
• Sin inicial en compras mayores a S/2,000

🎯 **Promociones especiales:**
• 3 cuotas sin intereses (cualquier monto)
• 6 cuotas sin intereses (compras +S/1,500)

📱 **Pago digital:**
• Yape, Plin, BCP, Interbank
• Transferencias bancarias

*Aplican términos y condiciones del banco emisor.

¿Qué opción te conviene más?"""
            }
        }
        
        # Diccionario para mantener las conversaciones por sesión
        self.session_conversations: Dict[str, List[Dict[str, Any]]] = {}

    def check_prepared_response(self, message: str) -> Optional[str]:
        """Verificar si el mensaje coincide con alguna respuesta preparada"""
        message_lower = message.lower()
        
        for category, info in self.prepared_responses.items():
            for pattern in info["patterns"]:
                if pattern in message_lower:
                    return info["response"]
        
        return None

    def extract_entities(self, message: str) -> Dict[str, Any]:
        """Extraer entidades del mensaje usando regex y IA - MEJORADO"""
        entities: Dict[str, Any] = {
            "_original_message": message  # Guardar mensaje original para contexto
        }
        
        message_lower = message.lower()
        
        # Extraer productos específicos
        product_patterns = {
            "laptop": r"laptop|portatil|notebook",
            "pc": r"\bpc\b|computadora|desktop",
            "gaming": r"gaming|gamer|juegos",
            "monitor": r"monitor|pantalla",
            "teclado": r"teclado|keyboard",
            "mouse": r"mouse|raton"
        }
        
        for product, pattern in product_patterns.items():
            if re.search(pattern, message_lower):
                entities["producto"] = product
                break
        
        # Extraer marcas
        brands = ["hp", "dell", "lenovo", "asus", "acer", "msi", "apple", "samsung"]
        for brand in brands:
            if brand in message_lower:
                entities["marca"] = brand
                break
        
        # Extraer presupuesto
        price_match = re.search(r'(?:hasta|máximo|presupuesto|budget)\s*(?:de\s*)?(?:s/\s*)?(\d+)', message_lower)
        if price_match:
            entities["presupuesto"] = int(price_match.group(1))
        
        # Extraer cantidad
        quantity_match = re.search(r'(\d+)\s*(?:unidades?|pcs?|equipos?)', message_lower)
        if quantity_match:
            entities["cantidad"] = int(quantity_match.group(1))
        
        # Detectar uso/caso de uso
        use_cases = {
            "gaming": ["gaming", "gamer", "juegos", "videojuegos", "fps", "minecraft", "fortnite"],
            "universidad": ["universidad", "universitario", "estudios", "carrera", "tesis", "investigación"],
            "trabajo": ["trabajo", "oficina", "empresarial", "corporativo", "profesional"],
            "programacion": ["programar", "programación", "desarrollo", "código", "python", "java"],
            "diseño": ["diseño", "photoshop", "illustrator", "render", "3d", "gráfico"],
            "basico": ["básico", "simple", "internet", "word", "excel", "navegación"]
        }
        
        for use_case, keywords in use_cases.items():
            if any(keyword in message_lower for keyword in keywords):
                            entities["uso"] = use_case
            break
          # Detectar intención de agregar al carrito
        cart_patterns = ["agregar", "añadir", "carrito", "comprar", "llevar", "quiero", "necesito", "agrega", "puedes agregar"]
        if any(pattern in message_lower for pattern in cart_patterns):
            entities["accion"] = "agregar_carrito"
          # Detectar solicitud de especificaciones - MEJORADO
        spec_patterns = ["especificaciones", "specs", "características", "detalles", "información detallada", "especificacion", "que especificacion", "qué especificación"]
        if any(pattern in message_lower for pattern in spec_patterns):
            entities["accion"] = "ver_especificaciones"
        
        # Detectar solicitud de recomendación - NUEVO
        recommend_patterns = ["recomiendas", "recomendación", "recomendaciones", "cual recomiendas", "qué recomiendas", "cual me recomiendas", "que me recomiendas", "cual es mejor", "cuál es mejor", "cual eliges", "sugieres"]
        if any(pattern in message_lower for pattern in recommend_patterns):
            entities["accion"] = "recomendar"
        
        # Extraer nombre específico de producto mencionado
        self.extract_product_name_from_message(message_lower, entities)
        
        return entities

    def extract_product_name_from_message(self, message_lower: str, entities: Dict[str, Any]) -> None:
        """Extraer nombre específico del producto mencionado"""
        # Patrones comunes de productos específicos - MEJORADO
        product_patterns = [
            # HP patterns - AMPLIADO
            r"hp\s+pavilion\s+gaming[\s\w]*",
            r"hp\s+pavilion[\s\w]*",
            r"hp\s+15-fc0048la",
            r"hp\s+14-ep0011la",
            r"hp\s+envy\s+x360",
            r"hp\s+omen[\s\w]*",
            
            # Lenovo patterns
            r"lenovo\s+legion\s+5[\s\w]*",
            r"lenovo\s+v15\s+g4\s+amn\s+ryzen\s+5",
            r"lenovo\s+v15\s+g4\s+i3",
            r"lenovo\s+ideapad\s+slim\s+3",
            r"lenovo\s+yoga\s+7",
            r"lenovo\s+ideapad\s+flex\s+5",
            
            # ASUS patterns
            r"asus\s+rog\s+strix\s+g15[\s\w]*",
            r"asus\s+vivobook\s+go\s+15",
            r"asus\s+vivobook\s+15\s+flip",
            
            # Dell patterns
            r"dell\s+inspiron\s+3520"
        ]
        
        for pattern in product_patterns:
            match = re.search(pattern, message_lower)
            if match:
                entities["producto_especifico"] = match.group().strip()
                break

    def should_show_products(self, entities: Dict[str, Any], conversation_history: List[Dict[str, Any]]) -> bool:
        """Determinar si debe buscar y mostrar productos"""
        # Si hay acción específica de ver especificaciones, buscar el producto
        if entities.get("accion") == "ver_especificaciones":
            return True
        
        # Si hay acción de agregar al carrito, buscar el producto
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
    
    def search_products(self, db: Session, search_query: str, max_price: Optional[int] = None) -> List[ProductModel]:
        """Buscar productos en la base de datos - MEJORADO"""
        try:
            # Import CRUD function
            from app.crud import search_products as crud_search_products
            
            # Buscar productos usando CRUD
            db_products = crud_search_products(db, search_query, limit=20)
            
            # Convertir a modelos Pydantic con validaciones manuales
            products = []
            count = 0
            
            for db_product in db_products:
                try:
                    # Crear el modelo primero
                    product_model = ProductModel.from_orm(db_product)
                    
                    # Filtrar por stock (ahora que ya es un modelo Pydantic)
                    if product_model.stock_quantity <= 0:
                        continue
                    
                    # Filtrar por precio si se especifica
                    if max_price and product_model.price > max_price:
                        continue
                    
                    products.append(product_model)
                    count += 1
                    
                    if count >= 10:  # Máximo 10 productos
                        break
                        
                except Exception as e:
                    logger.warning(f"Error convirtiendo producto: {e}")
                    continue
            
            return products
            
        except Exception as e:
            logger.error(f"Error buscando productos: {e}")
            return []
    
    def find_product_by_name(self, db: Session, product_name: str) -> Optional[ProductModel]:
        """Buscar producto específico por nombre - MEJORADO"""
        try:
            logger.info(f"Buscando producto por nombre: '{product_name}'")
            
            # Limpiar y normalizar el nombre del producto
            clean_name = product_name.strip().lower()
            
            # Estrategia 1: Buscar por coincidencia exacta en el nombre
            exact_match = db.query(Product).filter(Product.name.ilike(f"%{clean_name}%")).first()
            if exact_match:
                logger.info(f"Encontrado por coincidencia exacta: {exact_match.name}")
                return ProductModel.from_orm(exact_match)
            
            # Estrategia 2: Buscar por palabras clave individuales
            keywords = [word for word in clean_name.split() if len(word) > 2]
            logger.info(f"Buscando por palabras clave: {keywords}")
            
            if keywords:
                db_query = db.query(Product)
                for keyword in keywords:
                    db_query = db_query.filter(Product.name.ilike(f"%{keyword}%"))
                
                product = db_query.first()
                if product:
                    logger.info(f"Encontrado por palabras clave: {product.name}")
                    return ProductModel.from_orm(product)
            
            # Estrategia 3: Buscar por marcas y modelos específicos
            brand_searches = {
                "hp pavilion": "HP Pavilion",
                "lenovo legion": "Legion",
                "asus rog": "ROG",
                "dell inspiron": "Inspiron"
            }
            
            for search_term, db_term in brand_searches.items():
                if search_term in clean_name:
                    product = db.query(Product).filter(Product.name.ilike(f"%{db_term}%")).first()
                    if product:
                        logger.info(f"Encontrado por búsqueda de marca: {product.name}")
                        return ProductModel.from_orm(product)
            
            logger.warning(f"No se encontró producto para: '{product_name}'")
            return None
            
        except Exception as e:
            logger.error(f"Error buscando producto por nombre '{product_name}': {e}")
            return None

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
        if hasattr(product, 'model') and product.model:
            spec_response += f"📱 **Modelo:** {product.model}\n"
        
        # Descripción técnica (extraer specs desde el nombre)
        name_lower = product.name.lower()
        
        # Procesador
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
        
        # Memoria RAM
        if "8gb" in name_lower:
            spec_response += f"🧠 **Memoria RAM:** 8GB\n"
        elif "16gb" in name_lower:
            spec_response += f"🧠 **Memoria RAM:** 16GB\n"
        elif "32gb" in name_lower:
            spec_response += f"🧠 **Memoria RAM:** 32GB\n"
        
        # Almacenamiento
        if "256gb ssd" in name_lower:
            spec_response += f"💾 **Almacenamiento:** 256GB SSD\n"
        elif "512gb ssd" in name_lower:
            spec_response += f"💾 **Almacenamiento:** 512GB SSD\n"
        elif "1tb ssd" in name_lower:
            spec_response += f"💾 **Almacenamiento:** 1TB SSD\n"
        
        # Pantalla
        if "15.6" in name_lower:
            spec_response += f"🖥️ **Pantalla:** 15.6 pulgadas\n"
        elif "14" in name_lower:
            spec_response += f"🖥️ **Pantalla:** 14 pulgadas\n"
        
        if "fhd" in name_lower:
            spec_response += f"📺 **Resolución:** Full HD (1920x1080)\n"
        
        if "táctil" in name_lower or "touch" in name_lower:
            spec_response += f"👆 **Pantalla táctil:** Sí\n"
        
        # Características especiales
        if "gaming" in name_lower or "gamer" in name_lower:
            spec_response += f"🎮 **Gaming:** Optimizada para juegos\n"
        
        if "2 en 1" in name_lower or "2en1" in name_lower:
            spec_response += f"🔄 **Convertible:** Laptop 2 en 1\n"
        
        # Descripción adicional        if hasattr(product, 'description') and product.description:
            spec_response += f"\n📝 **Descripción:**\n{product.description}\n"
        
        spec_response += f"\n💡 **¿Te interesa este modelo? ¡Puedo agregarlo a tu carrito!**"
        
        return spec_response

    def add_to_cart(self, db: Session, product_id: int, quantity: int = 1, 
                    user_id: Optional[int] = None, session_id: Optional[str] = None) -> bool:
        """Agregar producto al carrito - MEJORADO"""
        try:
            # Verificar que el producto existe y tiene stock
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                logger.warning(f"Producto {product_id} no encontrado")
                return False
            
            # Convertir a modelo Pydantic para evitar errores de tipado
            try:
                product_model = ProductModel.from_orm(product)
                # Verificar stock disponible usando el modelo Pydantic
                if product_model.stock_quantity < quantity:
                    logger.warning(f"Stock insuficiente. Disponible: {product_model.stock_quantity}, Solicitado: {quantity}")
                    return False
            except Exception as model_error:
                logger.error(f"Error convirtiendo producto a modelo: {model_error}")
                return False
            
            logger.info(f"Agregando producto {product_id} al carrito (cantidad: {quantity})")
            return True
            
        except Exception as e:
            logger.error(f"Error agregando al carrito: {e}")
            return False

    def generate_product_response(self, products: List[ProductModel], use_case: Optional[str] = None) -> str:
        """Generar respuesta con productos - MEJORADO"""
        if not products:
            return "No encontré productos que coincidan con tu búsqueda. ¿Podrías ser más específico?"
          # Mensaje personalizado según el caso de uso
        intro_messages = {
            "gaming": "🎮 ¡Perfecto para gaming! Aquí tienes las mejores opciones:",
            "universidad": "🎓 Ideales para tus estudios universitarios:",
            "trabajo": "💼 Excelentes opciones para uso profesional:",
            "programacion": "👨‍💻 Perfectas para desarrollo y programación:",
            "basico": "💻 Opciones ideales para uso básico:",
        }
        
        # Corregir el error de tipado usando una condición explícita
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
                response += f"📦 {stock_status}\n"
                if hasattr(product, 'rating') and product.rating:
                    response += f"⭐ {product.rating}/5\n"
                response += "\n"
                
            except Exception as e:
                logger.warning(f"Error formateando producto {product.id}: {e}")
                continue
        
        # Mensaje de seguimiento
        if len(products) > 3:
            response += f"💡 *Y {len(products) - 3} opciones más disponibles*\n\n"
        
        response += "¿Te interesa alguna opción específica? ¡Puedo darte más detalles! 😊"
        
        return response

    def generate_general_response(self, message: str, context_str: str = "") -> str:
        """Generar respuesta general usando IA - MEJORADO con mejor prompt"""
        try:
            # Primero verificar respuestas preparadas
            prepared_response = self.check_prepared_response(message)
            if prepared_response:
                return prepared_response
            
            # Usar IA para respuestas más complejas
            prompt = f"""
            Eres InfoBot, el asistente virtual amigable de GRUPO INFOTEC, empresa peruana líder en tecnología.
            
            INFORMACIÓN DE LA EMPRESA:
            - Nombre: GRUPO INFOTEC
            - Especialidad: Laptops, PCs, componentes, soporte técnico
            - Ubicación: Lima, Perú
            - Experiencia: +15 años en el mercado
            - Servicios: Venta, soporte 24/7, garantías, financiamiento
            
            INSTRUCCIONES IMPORTANTES:
            1. Responde de manera amigable, profesional y concisa (máximo 200 palabras)
            2. Usa emojis para hacer las respuestas más amigables
            3. Si preguntan sobre productos, sugiere que pueden mostrar opciones específicas
            4. Si preguntan sobre envíos, garantías o financiamiento, da información útil
            5. Promociona los servicios de GRUPO INFOTEC cuando sea relevante
            6. NUNCA inventes información técnica específica
            
            CONTEXTO DE CONVERSACIÓN: {context_str}
            
            MENSAJE DEL USUARIO: {message}
            
            Responde como InfoBot de GRUPO INFOTEC:
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Error generando respuesta general: {e}")
            return "¡Hola! Soy InfoBot de GRUPO INFOTEC 🤖. Estoy aquí para ayudarte con información sobre nuestros productos, servicios técnicos y más. ¿En qué puedo asistirte hoy?"

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
        
        # Mantener solo las últimas 10 conversaciones
        if len(self.session_conversations[session_id]) > 10:
            self.session_conversations[session_id] = self.session_conversations[session_id][-10:]

    def process_message(self, message: str, db: Session, user_id: Optional[int] = None, 
                       session_id: str = "default") -> Dict[str, Any]:
        """Procesar mensaje del usuario - MEJORADO con mejor error handling"""
        try:
            # Validar entrada
            if not message or not message.strip():
                return {
                    "response": "¡Hola! Soy InfoBot de GRUPO INFOTEC 🤖. ¿En qué puedo ayudarte hoy?",
                    "intent": "saludo",
                    "entities": {},
                    "products": [],
                    "conversation_id": session_id
                }
            
            # Obtener historial de conversación
            conversation_history = self.get_conversation_history(session_id)
            
            # Extraer entidades del mensaje
            entities = self.extract_entities(message)
              # Determinar si debe mostrar productos
            should_search = self.should_show_products(entities, conversation_history)
            
            intent = "buscar_producto" if should_search else "conversacion_general"
            products = []
            bot_response = ""
            
            if should_search:
                # Manejar acciones específicas primero
                if entities.get("accion") == "ver_especificaciones":
                    # Si pide especificaciones, buscar producto específico
                    if entities.get("producto_especifico"):
                        product = self.find_product_by_name(db, entities["producto_especifico"])
                        if product:
                            bot_response = self.generate_product_specifications(product)
                            products = [product]
                        else:
                            bot_response = f"No encontré información específica sobre '{entities['producto_especifico']}'. ¿Podrías ser más específico con el modelo?"
                    else:
                        bot_response = "¿Sobre qué producto específico te gustaría conocer las especificaciones? Puedes mencionar el modelo exacto."
                
                elif entities.get("accion") == "agregar_carrito":
                    # Si quiere agregar al carrito, buscar producto específico
                    if entities.get("producto_especifico"):
                        product = self.find_product_by_name(db, entities["producto_especifico"])
                        if product:
                            quantity = entities.get("cantidad", 1)
                            success = self.add_to_cart(db, product.id, quantity, user_id, session_id)
                            if success:
                                bot_response = f"✅ ¡Perfecto! He agregado **{product.name}** a tu carrito.\n\n"
                                bot_response += f"📦 **Cantidad:** {quantity}\n"
                                bot_response += f"💰 **Precio:** S/ {product.price:.2f}\n"
                                bot_response += f"💳 **Total:** S/ {product.price * quantity:.2f}\n\n"
                                bot_response += "¿Te gustaría agregar algo más o proceder con la compra?"
                            else:
                                bot_response = f"❌ Lo siento, no pude agregar **{product.name}** al carrito. Podría estar agotado o no tener suficiente stock."
                            products = [product]
                        else:
                            bot_response = f"No encontré el producto '{entities['producto_especifico']}' en nuestro inventario. ¿Podrías verificar el nombre del modelo?"
                    else:
                        # Buscar productos para que elija cuál agregar
                        search_query = self.get_search_query_from_context(entities, conversation_history)
                        products = self.search_products(db, search_query, max_price=entities.get("presupuesto"))
                        
                        if products:
                            bot_response = "¿Cuál de estos productos te gustaría agregar al carrito? Solo menciona el nombre específico:\n\n"
                            bot_response += self.generate_product_response(products)
                        else:
                            bot_response = "No encontré productos disponibles que coincidan con tu búsqueda. ¿Podrías ser más específico?"
                
                else:
                    # Búsqueda normal de productos
                    search_query = self.get_search_query_from_context(entities, conversation_history)
                    products = self.search_products(
                        db, 
                        search_query,
                        max_price=entities.get("presupuesto")
                    )
                    
                    if products:
                        detected_use_case = entities.get("uso")
                        bot_response = self.generate_product_response(products, detected_use_case)
                    else:
                        # Fallback: buscar productos generales
                        fallback_products = self.search_products(db, "laptop")
                        if fallback_products:
                            products = fallback_products[:5]
                            bot_response = "No encontré exactamente lo que buscas, pero aquí tienes algunas opciones populares que podrían interesarte:\n\n"
                            bot_response += self.generate_product_response(products)
                        else:
                            bot_response = "Por el momento no tenemos productos disponibles en nuestro inventario. Te sugerimos contactarnos directamente para consultar disponibilidad. 📞"
            else:
                # Respuesta general
                context_str = ""
                if conversation_history:
                    recent_context = conversation_history[-2:]
                    context_str = "Conversación previa: " + " | ".join([
                        f"Usuario: {conv['user_message'][:50]} -> Bot: {conv['bot_response'][:50]}" 
                        for conv in recent_context
                    ])
                
                bot_response = self.generate_general_response(message, context_str)
            
            # Guardar conversación
            self.save_conversation(
                session_id, 
                message, 
                bot_response, 
                intent, 
                entities, 
                len(products) > 0
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
                "intent": "error",                "entities": {},
                "products": [],
                "conversation_id": session_id
            }
