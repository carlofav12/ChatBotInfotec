# filepath: backend/app/chatbot/services/ai_response_generator.py
"""
Generador de respuestas usando inteligencia artificial
Maneja las respuestas generales del chatbot usando Gemini AI
"""
import logging
import google.generativeai as genai
from ..core.config import ChatbotConfig

logger = logging.getLogger(__name__)

class AIResponseGenerator:
    """Genera respuestas usando IA para conversaciones generales"""
    
    def __init__(self, api_key: str):
        """Inicializar el generador de respuestas con IA"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.config = ChatbotConfig()
    
    def generate_general_response(self, message: str, context_str: str = "") -> str:
        """Generar respuesta general usando IA"""
        try:
            # Detectar tipo de mensaje para respuesta personalizada
            message_lower = message.lower()
            
            # Respuestas específicas para saludos
            if any(greeting in message_lower for greeting in ["hola", "buenas", "buenos dias", "buenas tardes", "buenas noches", "hey", "hi"]):
                return "¡Hola! 👋 Soy InfoBot de GRUPO INFOTEC. Me da mucho gusto saludarte. 😊 Estamos aquí para ayudarte con laptops, PCs y todo lo que necesites en tecnología. ¿En qué puedo asistirte hoy? ✨"
            
            # Respuestas para preguntas casuales
            if any(casual in message_lower for casual in ["que tal", "como estas", "como va", "que hay", "que tal el dia"]):
                return "¡Todo excelente por aquí! 😄 Gracias por preguntar. Estoy listo para ayudarte con cualquier consulta sobre nuestros productos. En GRUPO INFOTEC tenemos las mejores ofertas en laptops y PCs. ¿Hay algo específico que te interese? 💻"
            
            # Respuestas para agradecimientos
            if any(thanks in message_lower for thanks in ["gracias", "muchas gracias", "te agradezco"]):
                return "¡De nada! 😊 Ha sido un placer ayudarte. Recuerda que en GRUPO INFOTEC estamos disponibles 24/7 para cualquier consulta. ¡Que tengas un excelente día! ✨"
            
            # Usar IA para respuestas más complejas
            prompt = self._build_ai_prompt(message, context_str)
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Error generando respuesta general: {e}")
            return "¡Hola! 👋 Soy InfoBot de GRUPO INFOTEC. Estoy aquí para ayudarte con información sobre nuestros productos y servicios. ¿En qué puedo asistirte hoy? 😊"
    
    def _build_ai_prompt(self, message: str, context_str: str) -> str:
        """Construir prompt para la IA"""
        company_info = self.config.COMPANY_INFO
        
        prompt = f"""
        Eres InfoBot, el asistente virtual amigable de GRUPO INFOTEC, empresa peruana líder en tecnología.
        
        INFORMACIÓN DE LA EMPRESA:
        - Nombre: {company_info['nombre']}
        - Especialidad: Laptops, PCs gaming, componentes, soporte técnico especializado
        - Ubicación: Lima, Perú (con envíos a todo el país)
        - Experiencia: +15 años en el mercado peruano
        - Servicios: Venta de equipos, soporte 24/7, garantías extendidas, financiamiento
        
        ESPECIALIDADES:
        {', '.join(company_info['especialidades'])}
        
        SERVICIOS:
        {', '.join(company_info['servicios'])}
        
        INSTRUCCIONES IMPORTANTES:
        1. Responde de manera amigable y conversacional (100-150 palabras máximo)
        2. Usa emojis moderadamente para hacer las respuestas más expresivas
        3. Mantén un tono entusiasta pero profesional
        4. Si preguntan sobre productos, ofrece ayuda específica
        5. Menciona beneficios de GRUPO INFOTEC cuando sea relevante
        6. Haz preguntas de seguimiento para mantener la conversación
        7. NUNCA inventes especificaciones técnicas
        8. Termina siempre invitando a continuar la conversación
        
        CONTEXTO DE CONVERSACIÓN: {context_str}
        
        MENSAJE DEL USUARIO: {message}
        
        Responde como InfoBot de GRUPO INFOTEC de manera conversacional:
        """
        
        return prompt
