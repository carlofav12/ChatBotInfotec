'''
Servicio mejorado para interactuar con un Large Language Model (LLM).
Utiliza Gemini AI para comparaciones de productos y consultas tecnológicas avanzadas.
'''
import logging
from typing import List, Dict, Any, Optional
import google.generativeai as genai

logger = logging.getLogger(__name__)

class LLMService:
    """
    Servicio mejorado para interactuar con Gemini AI.
    Maneja comparaciones de productos y consultas tecnológicas avanzadas.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        if not api_key:
            logger.warning("LLMService inicializado sin API key. Funcionalidad limitada.")
            self.model = None
        else:
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                logger.info("LLMService inicializado correctamente con Gemini AI")
            except Exception as e:
                logger.error(f"Error inicializando Gemini AI: {e}")
                self.model = None

    def generate_comparison_fallback(
        self,
        item1_name: str,
        item2_name: str,
        attributes: List[str],
        item1_data: Optional[Dict[str, Any]] = None,
        item2_data: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Genera una comparación detallada usando Gemini AI cuando la búsqueda estructurada falla o es insuficiente.
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
        Recomienda los 'count' mejores productos de una lista de candidatos usando LLM.
        """
        logger.info(f"LLM Recomendación: Top {count} productos para query: '{user_query}', categoría: {category}, uso: {use_case}")

        if not candidate_products:
            return "Lo siento, no tengo suficientes datos en este momento para hacer una recomendación precisa con IA sobre eso."

        prompt = (
            f"Eres un asistente de ventas experto en tecnología. Basado en la siguiente lista de productos de nuestra base de datos y la consulta del cliente, "
            f"recomienda los {count} mejores y explica brevemente por qué cada uno es una buena opción.\n"
            f"Consulta del cliente: '{user_query}'\n"
        )
        if category:
            prompt += f"Categoría de interés: {category}\n"
        if use_case:
            prompt += f"Uso principal: {use_case}\n"
        
        prompt += "Productos disponibles (nombre, precio, y otros datos relevantes):\n"
        for i, prod_data in enumerate(candidate_products[:10]): # Limitar a 10 para no exceder el prompt
            simple_prod_data = {
                "nombre": prod_data.get("name"),
                "precio": prod_data.get("price"),
                "descripción_corta": prod_data.get("description", "")[:100] + "...",
                "rating": prod_data.get("rating", "N/A")
            }
            if 'specifications' in prod_data and isinstance(prod_data['specifications'], dict):
                simple_prod_data.update({k: v for k, v in prod_data['specifications'].items() if k in ['processor_model', 'ram_amount', 'storage_capacity', 'graphics_card_model']})

            prompt += f"{i+1}. {simple_prod_data}\n"
        
        prompt += f"\nPor favor, presenta tu recomendación de los {count} mejores de forma clara y convincente."

        # ----- SIMULACIÓN DE RESPUESTA LLM -----
        response_text = (
            f"¡Claro! Basado en tu solicitud '{user_query}' y nuestros productos, aquí están mis {count} recomendaciones principales:\n"
        )
        for i, prod in enumerate(candidate_products[:count]):
            response_text += (
                f"{i+1}. **{prod.get('name', 'Producto Increíble')}** (Precio: S/ {prod.get('price', 'Consultar')})\n"
                f"   - *Por qué es genial*: [Explicación generada por IA destacando por qué es bueno para '{user_query}'. Esta es una simulación.]\n"
            )
        response_text += "\nEspero que esto te ayude a decidir. ¡Avísame si tienes más preguntas!"
        # ----- FIN SIMULACIÓN -----

        logger.debug(f"LLM Prompt para recomendación: {prompt}")
        logger.debug(f"LLM Respuesta simulada: {response_text}")
        return response_text
