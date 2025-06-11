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
        "despedida": "¡Gracias por chatear con InfoBot! Que tengas un buen día. 😊",
        "agradecimiento": "¡De nada! Estoy aquí para ayudarte. 😊",
        "producto_no_encontrado": "Lo siento, no pude encontrar ese producto específico. ¿Podrías verificar el nombre o darme más detalles? 🤔",
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
        "laptop": r"laptop|port[aá]til|notebook",
        "pc": r"pc|computadora de escritorio|desktop|ordenador",
        "monitor": r"monitor|pantalla",
        "teclado": r"teclado|keyboard",
        "mouse": r"mouse|rat[oó]n",
        "impresora": r"impresora|printer",
        "tablet": r"tablet",
        "smartphone": r"smartphone|celular|m[oó]vil",
        "audifonos": r"aud[ií]fonos|auriculares|headset",
        "componente_pc": r"tarjeta de video|gpu|procesador|cpu|memoria ram|ram|disco duro|ssd|placa madre|motherboard"
    }
    
    BRANDS = [
        "asus", "lenovo", "hp", "dell", "acer", "apple", "samsung", 
        "lg", "microsoft", "xiaomi", "huawei", "msi", "gigabyte", 
        "corsair", "logitech", "razer", "kingston", "intel", "amd"
    ]
    
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
        r"agrega(?:r)? al carrito", r"a[ñn]ade(?:r)? al carrito", r"quiero comprar",
        r"comprar est[oa]", r"pon(?:er)? en el carrito", r"lo llevo",
        r"agregar", r"añadir", "carrito", r"comprar", r"llevar", r"quiero", r"necesito", 
        r"agrega", r"puedes agregar", r"agregarlo", r"añadirlo", r"comprarlo", r"lo quiero", 
        r"lo agrego", r"puedes agregarlo", r"me lo das", r"lo llevo"
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
        r"es[ea]", r"es[oa]s", r"el anterior", r"la primera", r"el [uú]ltimo", r"ese modelo"
    ]
    
    SPECIFIC_PRODUCT_PATTERNS = [
        r"(?:laptop|pc|monitor|tablet)\s+(?:[a-zA-Z0-9]+\s*){1,5}", 
        r"(?:[a-zA-Z]+\s+){0,2}(?:xps|macbook|thinkpad|rog|omen|spectre|zenbook|ideapad|legion|alienware|envy|pavilion|aspire|predator|surface)\s*\d*\s*[a-zA-Z0-9]*" # Ej: Dell XPS 13, ROG Strix G15
    ]
    
    COMPARISON_PATTERNS = [
        r"cu[aá]l es mejor\s*(.+)\s*o\s*(.+)",          # "cual es mejor lenovo o hp"
        r"qu[eé] es mejor\s*(.+)\s*o\s*(.+)",           # "que es mejor asus o dell"
        r"mejor\s*(.+)\s*o\s*(.+)",                     # "mejor hp o lenovo"
        r"compara(?:r)?\s*(.+)\s*(?:con|vs|versus)\s*(.+)",  # "compara lenovo con hp"
        r"diferencias?\s+entre\s*(.+)\s*y\s*(.+)",      # "diferencia entre" o "diferencias entre"
        r"cu[aá]l es mejor entre\s*(.+)\s*y\s*(.+)",    # "cual es mejor entre asus y acer"
        r"(.+)\s*vs\s*(.+)",                            # "hp vs dell"
        r"recomienda(?:s)?\s*(.+)\s*o\s*(.+)",          # "recomiendas hp o dell"
        r"elijo\s*(.+)\s*o\s*(.+)",                     # "elijo asus o hp"
        r"prefiere(?:s)?\s*(.+)\s*o\s*(.+)"             # "prefieres lenovo o acer"
    ]
    
    # Patrones para preguntas de recomendación general
    RECOMMENDATION_QUERY_PATTERNS = [
        r"qu[eé]\s+(?:laptop|pc|computadora|equipo)\s+es\s+mejor",      # "que laptop es mejor"
        r"cu[aá]l\s+(?:laptop|pc|computadora|equipo)\s+es\s+mejor",     # "cual laptop es mejor"  
        r"qu[eé]\s+me\s+recomien(?:da|das)",                           # "que me recomiendas"
        r"cu[aá]l\s+me\s+recomien(?:da|das)",                          # "cual me recomiendas"
        r"cu[aá]l\s+recomien(?:da|das)",                               # "cual recomiendas"
        r"mejor\s+(?:laptop|pc|computadora|equipo|marca)",             # "mejor laptop", "mejor marca"
        r"(?:laptop|pc|computadora|equipo)\s+recomenda(?:da|do)",      # "laptop recomendada"
    ]
    
    COMPARISON_ATTRIBUTE_PATTERNS = {
        "precio": [r"precio", r"costo", r"cu[aá]nto cuesta"],
        "bateria": [r"bater[ií]a", r"duraci[oó]n de bater[ií]a", r"autonom[ií]a"],
        "pantalla": [r"pantalla", r"display", r"resoluci[oó]n"],
        "rendimiento": [r"rendimiento", r"performance", r"potencia", r"velocidad"],
        "camara": [r"c[aá]mara", r"fotos", r"v[ií]deo"],
        "almacenamiento": [r"almacenamiento", r"capacidad", r"disco duro", r"ssd", r"gb de disco"],
        "ram": [r"ram", r"memoria ram", r"gb de ram"],
        "procesador": [r"procesador", r"cpu", r"chip"],
        "tarjeta grafica": [r"tarjeta gr[aá]fica", r"gpu", r"video"],
        "peso": [r"peso", r"cu[aá]nto pesa", r"ligero"],
        "dimensiones": [r"dimensiones", r"tama[ñn]o", r"medidas"],
        "marca": [r"marca", r"fabricante"],
        "caracteristicas": [r"caracter[ií]sticas", r"especificaciones", r"specs", r"detalles generales", r"todo"]
    }
