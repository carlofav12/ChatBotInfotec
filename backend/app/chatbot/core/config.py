# filepath: backend/app/chatbot/core/config.py
"""
Configuración y datos básicos del chatbot
Contiene información de la empresa y respuestas preparadas
"""
from typing import Dict, List, Any

class ChatbotConfig:
    """Configuración y datos estáticos del chatbot"""
    
    # Información extendida de la empresa
    COMPANY_INFO = {
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
    PREPARED_RESPONSES = {
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

¿Qué opción te conviene más?"""
        }
    }
    
    # Patrones para extracción de entidades
    PRODUCT_PATTERNS = {
        "laptop": r"laptop|portatil|notebook",
        "pc": r"\bpc\b|computadora|desktop",
        "gaming": r"gaming|gamer|juegos",
        "monitor": r"monitor|pantalla",
        "teclado": r"teclado|keyboard",
        "mouse": r"mouse|raton",
        "impresora": r"impresora[s]?|printer[s]?",
        "procesador": r"procesador|cpu",
        "audifono": r"audifono|Headphone",
        
    }
    
    BRANDS = ["hp", "dell", "lenovo", "asus", "acer", "msi", "apple", "samsung"]
    
    USE_CASES = {
        "gaming": ["gaming", "gamer", "juegos", "videojuegos", "fps", "minecraft", "fortnite"],
        "universidad": ["universidad", "universitario", "estudios", "carrera", "tesis", "investigación"],
        "trabajo": ["trabajo", "oficina", "empresarial", "corporativo", "profesional"],
        "programacion": ["programar", "programación", "desarrollo", "código", "python", "java"],
        "diseño": ["diseño", "photoshop", "illustrator", "render", "3d", "gráfico"],
        "basico": ["básico", "simple", "internet", "word", "excel", "navegación"]
    }
    
    # Patrones de productos específicos
    SPECIFIC_PRODUCT_PATTERNS = [
        # ASUS patterns
        r"asus\s+vivobook\s+go\s+15\s+e1504fa[\s\w]*",
        r"asus\s+vivobook\s+go\s+15[\s\w]*",
        r"asus\s+rog\s+strix\s+g15[\s\w]*",
        r"asus\s+vivobook\s+16x[\s\w]*",
        r"asus\s+vivobook[\s\w]*",
        
        # HP patterns
        r"hp\s+pavilion\s+gaming[\s\w]*",
        r"hp\s+pavilion[\s\w]*",
        r"hp\s+15-fc0048la[\s\w]*",
        r"hp\s+14-ep0011la[\s\w]*",
        r"hp\s+envy\s+x360[\s\w]*",
        r"hp\s+omen[\s\w]*",
        
        # Lenovo patterns
        r"lenovo\s+legion\s+5[\s\w]*",
        r"lenovo\s+v15\s+g4\s+amn[\s\w]*",
        r"lenovo\s+v15\s+g4\s+i3[\s\w]*",
        r"lenovo\s+ideapad\s+flex\s+5[\s\w]*",
        r"lenovo\s+yoga\s+7[\s\w]*",
        r"lenovo\s+v15[\s\w]*",
        
        # Dell patterns
        r"dell\s+inspiron\s+3520[\s\w]*",
        r"dell\s+inspiron[\s\w]*"
    ]
    
    # Patrones de acciones
    CART_PATTERNS = [
        "agregar", "añadir", "carrito", "comprar", "llevar", "quiero", "necesito", 
        "agrega", "puedes agregar", "agregarlo", "añadirlo", "comprarlo", "lo quiero", 
        "lo agrego", "puedes agregarlo", "me lo das", "lo llevo"
    ]
    
    SPEC_PATTERNS = [
        "especificaciones", "specs", "características", "detalles", 
        "información detallada", "especificacion", "que especificacion", 
        "qué especificación", "info", "más info"
    ]
    
    RECOMMEND_PATTERNS = [
        "recomiendas", "recomendación", "recomendaciones", "cual recomiendas", 
        "qué recomiendas", "cual me recomiendas", "que me recomiendas", 
        "cual es mejor", "cuál es mejor", "cual eliges", "sugieres", "recomiendan"
    ]
    
    # Contextos referenciales
    CONTEXTUAL_REFS = [
        "agregarlo", "añadirlo", "comprarlo", "lo quiero", "este", "esa", "eso", "la anterior"
    ]
