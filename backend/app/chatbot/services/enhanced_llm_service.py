'''
Servicio mejorado para interactuar con Gemini AI.
Maneja comparaciones de productos, consultas tecnológicas y recomendaciones avanzadas.
'''
import logging
from typing import List, Dict, Any, Optional
import google.generativeai as genai

logger = logging.getLogger(__name__)

class EnhancedLLMService:
    """
    Servicio mejorado para interactuar con Gemini AI.
    Maneja comparaciones de productos y consultas tecnológicas avanzadas.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        if not api_key:
            logger.warning("EnhancedLLMService inicializado sin API key. Funcionalidad limitada.")
            self.model = None
        else:
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                logger.info("EnhancedLLMService inicializado correctamente con Gemini AI")
            except Exception as e:
                logger.error(f"Error inicializando Gemini AI: {e}")
                self.model = None

    def generate_comparison_response(
        self,
        item1_name: str,
        item2_name: str,
        attributes: List[str],
        item1_data: Optional[Dict[str, Any]] = None,
        item2_data: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Genera una comparación detallada usando Gemini AI.
        """
        logger.info(f"LLM Comparación: '{item1_name}' vs '{item2_name}' en atributos: {attributes}")
        
        if not self.model:
            return self._fallback_comparison_response(item1_name, item2_name, attributes)
        
        try:
            prompt = self._build_comparison_prompt(item1_name, item2_name, attributes, item1_data, item2_data)
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Error en comparación LLM: {e}")
            return self._fallback_comparison_response(item1_name, item2_name, attributes)
    
    def _build_comparison_prompt(self, item1_name: str, item2_name: str, attributes: List[str], 
                                item1_data: Optional[Dict[str, Any]], item2_data: Optional[Dict[str, Any]]) -> str:
        """Construir prompt especializado para comparación de productos tecnológicos"""
        
        prompt = f"""
Eres un experto consultor en tecnología de GRUPO INFOTEC, empresa líder en equipos tecnológicos en Perú.

TAREA: Compara detalladamente '{item1_name}' con '{item2_name}' para ayudar a un cliente a tomar la mejor decisión.

ASPECTOS A COMPARAR:
{', '.join(attributes) if attributes and 'caracteristicas' not in attributes else 'Todas las características relevantes'}

INFORMACIÓN DISPONIBLE:
"""
        
        if item1_data:
            prompt += f"\n📊 DATOS DE {item1_name.upper()}:\n"
            for key, value in item1_data.items():
                if value and value != "N/A":
                    prompt += f"• {key.replace('_', ' ').title()}: {value}\n"
        
        if item2_data:
            prompt += f"\n📊 DATOS DE {item2_name.upper()}:\n"
            for key, value in item2_data.items():
                if value and value != "N/A":
                    prompt += f"• {key.replace('_', ' ').title()}: {value}\n"
        
        prompt += f"""

INSTRUCCIONES:
1. Proporciona una comparación clara y estructurada
2. Destaca las ventajas y desventajas de cada producto
3. Considera factores como rendimiento, precio, calidad-precio
4. Usa un tono profesional pero amigable
5. Incluye emojis moderadamente para mejor legibilidad
6. Termina con una recomendación según diferentes tipos de usuario
7. Máximo 300 palabras
8. Si falta información específica, basa la comparación en conocimiento general de estos productos

Formato de respuesta:
🔍 **Comparación: {item1_name} vs {item2_name}**

[Comparación detallada aquí]

💡 **Recomendación:**
[Sugerencia según tipo de usuario]
"""
        
        return prompt
    
    def _fallback_comparison_response(self, item1_name: str, item2_name: str, attributes: List[str]) -> str:
        """Respuesta de respaldo cuando no está disponible el LLM"""
        return f"""🔍 **Comparación: {item1_name} vs {item2_name}**

Lo siento, en este momento tengo limitaciones para realizar una comparación detallada con IA. 

📋 **Lo que puedo hacer:**
• Buscar especificaciones individuales de cada producto
• Mostrar precios y disponibilidad actual
• Conectarte con un asesor especializado

💡 **Te sugiero:**
1. Consultar las especificaciones de cada producto por separado
2. Contactar a nuestro equipo de ventas para una asesoría personalizada
3. Visitar nuestra tienda para ver los productos en persona

¿Te gustaría que busque información específica de alguno de estos productos?"""

    def recommend_top_products(
        self,
        candidate_products: List[Dict[str, Any]],
        user_query: str,
        category: Optional[str] = None,
        use_case: Optional[str] = None,
        count: int = 3
    ) -> str:
        """
        Genera recomendaciones inteligentes de productos usando IA
        """
        logger.info(f"Generando recomendaciones IA para {len(candidate_products)} productos")
        
        if not self.model:
            return self._fallback_recommendation_response(candidate_products, user_query, count)
        
        try:
            prompt = self._build_recommendation_prompt(
                candidate_products, user_query, category, use_case, count
            )
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Error generando recomendaciones con IA: {e}")
            return self._fallback_recommendation_response(candidate_products, user_query, count)

    def _build_recommendation_prompt(
        self,
        products: List[Dict[str, Any]],
        user_query: str,
        category: Optional[str],
        use_case: Optional[str],
        count: int
    ) -> str:
        """Construir prompt para recomendaciones"""
        
        # Formatear productos para el prompt
        products_text = ""
        for i, product in enumerate(products[:50], 1):  # Máximo 50 productos para análisis
            specs_text = ""
            if product.get("specifications"):
                specs = product["specifications"]
                if isinstance(specs, dict):
                    specs_text = ", ".join([f"{k}: {v}" for k, v in specs.items() if v])
                else:
                    specs_text = str(specs)
            
            products_text += f"""
{i}. {product.get('name', 'N/A')}
   - Precio: S/ {product.get('price', 0)}
   - Marca: {product.get('brand', 'N/A')}
   - Rating: {product.get('rating', 'N/A')}/5
   - Stock: {product.get('stock_quantity', 0)}
   - Descripción: {product.get('description', 'N/A')}
   - Especificaciones: {specs_text or 'N/A'}
"""

        context_info = ""
        if category:
            context_info += f"Categoría solicitada: {category}\n"
        if use_case:
            context_info += f"Caso de uso: {use_case}\n"

        return f"""Eres InfoBot de GRUPO INFOTEC, especialista en tecnología. Analiza estos {len(products)} productos y recomienda los {count} mejores para la consulta del usuario.

CONSULTA DEL USUARIO: "{user_query}"
{context_info}

PRODUCTOS DISPONIBLES:
{products_text}

INSTRUCCIONES:
1. Analiza TODOS los productos considerando: precio, especificaciones, rating, stock, relación calidad-precio
2. Selecciona los {count} mejores productos que respondan mejor a la consulta
3. Ordénalos del mejor al menos recomendado
4. Para cada recomendación incluye:
   - Nombre del producto exacto
   - Precio
   - 2-3 razones principales por las que lo recomiendas
   - Un beneficio clave específico

FORMATO DE RESPUESTA (máximo 150 palabras):
🎯 **Mis {count} mejores recomendaciones:**

**1. [Nombre exacto]** (S/ [precio])
✨ [Razón principal] - [Beneficio específico]

**2. [Nombre exacto]** (S/ [precio])  
✨ [Razón principal] - [Beneficio específico]

**3. [Nombre exacto]** (S/ [precio])
✨ [Razón principal] - [Beneficio específico]

💡 ¿Te interesa alguna? ¡Puedo darte más detalles! 😊

IMPORTANTE: 
- Solo recomienda productos de la lista proporcionada
- Usa los nombres exactos de los productos
- Sé conciso pero informativo
- Responde como InfoBot de GRUPO INFOTEC
"""

    def _fallback_recommendation_response(
        self,
        products: List[Dict[str, Any]],
        user_query: str,
        count: int
    ) -> str:
        """Respuesta de respaldo para recomendaciones"""
        # Ordenar productos por rating y precio para dar mejores primero
        sorted_products = sorted(
            products, 
            key=lambda x: (x.get('rating', 0) or 0, -(x.get('price', 0) or 0)), 
            reverse=True
        )
        
        response = f"🎯 **Mis {count} mejores recomendaciones:**\n\n"
        
        for i, product in enumerate(sorted_products[:count], 1):
            name = product.get('name', 'Producto')
            price = product.get('price', 0)
            brand = product.get('brand', '')
            rating = product.get('rating', 0)
            
            brand_text = f" de {brand}" if brand else ""
            rating_text = f" - Rating {rating}/5" if rating else ""
            
            response += f"**{i}. {name}** (S/ {price})\n"
            response += f"✨ Excelente opción{brand_text}{rating_text}\n\n"
        
        response += "💡 ¿Te interesa alguna? ¡Puedo darte más detalles! 😊"
        return response

    def answer_tech_question(self, question: str, context: str = "") -> str:
        """
        Responde preguntas generales sobre tecnología usando IA.
        """
        logger.info(f"Consulta tecnológica: {question[:50]}...")
        
        if not self.model:
            return self._fallback_tech_response(question)
        
        try:
            prompt = self._build_tech_question_prompt(question, context)
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Error en consulta tecnológica: {e}")
            return self._fallback_tech_response(question)

    def _build_tech_question_prompt(self, question: str, context: str) -> str:
        """Construir prompt para consultas tecnológicas"""
        
        prompt = f"""
Eres InfoBot, el asistente especializado en tecnología de GRUPO INFOTEC, empresa líder en Perú.

CONSULTA DEL CLIENTE: "{question}"

CONTEXTO ADICIONAL: {context if context else "Ninguno"}

CONOCIMIENTO BASE:
- Eres experto en laptops, PCs, componentes, hardware y software
- Tienes conocimiento actualizado sobre marcas como HP, Dell, Asus, Lenovo, Acer, MSI
- Conoces sobre procesadores Intel, AMD, tarjetas gráficas NVIDIA, AMD
- Sabes sobre tendencias tecnológicas, gaming, productividad, desarrollo

INSTRUCCIONES:
1. Responde de manera clara y educativa
2. Usa un tono amigable pero profesional
3. Incluye ejemplos prácticos cuando sea relevante
4. Si la pregunta requiere productos específicos, menciona que puedes ayudar a buscarlos
5. Máximo 200 palabras
6. Incluye emojis moderadamente
7. Termina invitando a seguir la conversación

IMPORTANTE: No inventes especificaciones exactas de productos. Si necesitas datos específicos, sugiere buscar productos en nuestra tienda.

Responde como InfoBot de GRUPO INFOTEC:
"""
        
        return prompt

    def _fallback_tech_response(self, question: str) -> str:
        """Respuesta de respaldo para consultas tecnológicas"""
        return f"""💡 **Sobre tu consulta tecnológica:**

Gracias por tu pregunta sobre tecnología. Aunque tengo algunas limitaciones técnicas en este momento, puedo ayudarte de estas maneras:

🔍 **Lo que puedo hacer:**
• Buscar productos específicos en nuestro catálogo
• Mostrar especificaciones detalladas de equipos
• Ayudarte a comparar opciones disponibles
• Conectarte con nuestros especialistas

💬 **Mi sugerencia:**
¿Podrías reformular tu pregunta especificando qué tipo de producto o información buscas? Por ejemplo:
• "Busco una laptop para gaming"
• "Quiero comparar procesadores Intel vs AMD"
• "Necesito una PC para diseño gráfico"

¡Estoy aquí para ayudarte a encontrar la mejor solución tecnológica! 😊"""