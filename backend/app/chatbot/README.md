# 🤖 Chatbot Modularizado - GRUPO INFOTEC

## 📋 Descripción General

Este proyecto contiene el chatbot inteligente de GRUPO INFOTEC completamente modularizado y refactorizado desde `enhanced_chatbot_v3.py` para mejorar la mantenibilidad, escalabilidad y organización del código.

## 🏗️ Estructura de Archivos Modularizada

```
backend/app/chatbot/
├── 📁 __init__.py                      # Punto de entrada principal del módulo
├── 📁 core/                            # Núcleo del sistema
│   ├── __init__.py                     # Exports del módulo core
│   ├── config.py                       # ⚙️ Configuraciones y constantes
│   └── enhanced_chatbot_v4.py          # 🧠 Chatbot principal (orquestador)
├── 📁 services/                        # Servicios de negocio
│   ├── __init__.py                     # Exports del módulo services
│   ├── product_service.py              # 🛍️ Manejo de productos y carrito
│   └── ai_response_generator.py        # 🤖 Generación de respuestas con IA
└── 📁 utils/                           # Utilidades y herramientas
    ├── __init__.py                     # Exports del módulo utils
    ├── entity_extractor.py             # 🔍 Extracción de entidades
    ├── response_formatter.py           # 📝 Formateo de respuestas
    └── conversation_manager.py         # 💬 Manejo de conversaciones
```

---

## 📁 Descripción Detallada de Cada Módulo

### 🏛️ **Core (Núcleo)**

#### `core/config.py` - Configuración Central
```python
class ChatbotConfig:
    COMPANY_INFO = {...}           # Información de GRUPO INFOTEC
    PREPARED_RESPONSES = {...}     # Respuestas preparadas (envío, garantía, etc.)
    PRODUCT_PATTERNS = {...}       # Patrones regex para productos
    BRANDS = [...]                 # Lista de marcas soportadas
    USE_CASES = {...}              # Casos de uso (gaming, universidad, etc.)
```

**🎯 Responsabilidades:**
- ⚙️ Almacenar toda la configuración estática
- 📊 Definir patrones de reconocimiento
- 🏢 Información corporativa de GRUPO INFOTEC
- 💬 Respuestas predefinidas para consultas comunes

#### `core/enhanced_chatbot_v4.py` - Orquestador Principal
```python
class EnhancedInfotecChatbotV4:
    def process_message(self, message, db, user_id, session_id) -> Dict[str, Any]
    def _handle_product_request(self, entities, conversation_history, db, user_id, session_id)
    def _handle_general_conversation(self, message, conversation_history)
```

**🎯 Responsabilidades:**
- 🧠 Coordinar todos los módulos del sistema
- 🔄 Manejar el flujo principal de procesamiento
- ⚡ Decidir qué tipo de respuesta generar
- 🎭 Orquestar la interacción entre componentes

---

### 🛠️ **Services (Servicios)**

#### `services/product_service.py` - Gestión de Productos
```python
class ProductService:
    def search_products(self, db, search_query, max_price) -> List[ProductModel]
    def find_product_by_name(self, db, product_name) -> Optional[ProductModel]
    def add_to_cart(self, db, product_id, quantity, user_id, session_id) -> bool
```

**🎯 Responsabilidades:**
- 🔍 Búsqueda inteligente de productos
- 📦 Gestión de inventario y stock
- 🛒 Operaciones del carrito de compras
- 💰 Validación de precios y disponibilidad

#### `services/ai_response_generator.py` - IA Conversacional
```python
class AIResponseGenerator:
    def generate_general_response(self, message, context_str) -> str
    def _build_ai_prompt(self, message, context_str) -> str
```

**🎯 Responsabilidades:**
- 🤖 Generar respuestas usando Gemini AI
- 💭 Manejar conversaciones naturales
- 🎨 Personalizar el tono según GRUPO INFOTEC
- 📚 Incorporar contexto conversacional

---

### 🔧 **Utils (Utilidades)**

#### `utils/entity_extractor.py` - Análisis de Mensajes
```python
class EntityExtractor:
    def extract_entities(self, message, conversation_history) -> Dict[str, Any]
    def should_show_products(self, entities, conversation_history) -> bool
    def get_search_query_from_context(self, entities, conversation_history) -> str
```

**🎯 Responsabilidades:**
- 🔍 Extraer entidades de mensajes (productos, marcas, precios)
- 🎯 Detectar intenciones del usuario
- 🧩 Analizar contexto conversacional
- ⚡ Determinar acciones a ejecutar

#### `utils/response_formatter.py` - Formateo de Respuestas
```python
class ResponseFormatter:
    def generate_product_response(self, products, use_case) -> str
    def generate_product_specifications(self, product) -> str
    def check_prepared_response(self, message) -> Optional[str]
```

**🎯 Responsabilidades:**
- 📝 Formatear respuestas de productos
- 📋 Generar especificaciones técnicas
- 🎨 Aplicar estilos y emojis consistentes
- 💡 Crear mensajes atractivos y útiles

#### `utils/conversation_manager.py` - Gestión de Contexto
```python
class ConversationManager:
    def get_conversation_history(self, session_id) -> List[Dict[str, Any]]
    def save_conversation(self, session_id, user_message, bot_response, ...)
    def get_session_stats(self, session_id) -> Dict[str, Any]
```

**🎯 Responsabilidades:**
- 💾 Mantener historial de conversaciones
- 🔄 Gestionar contexto entre mensajes
- 📊 Generar estadísticas de uso
- 🧹 Limpiar sesiones obsoletas

---

## 🚀 Cómo Usar el Chatbot

### Importación y Uso Básico
```python
from app.chatbot import EnhancedInfotecChatbotV4

# Inicializar el chatbot
chatbot = EnhancedInfotecChatbotV4(api_key="tu-google-api-key")

# Procesar un mensaje
response = chatbot.process_message(
    message="Busco una laptop gaming",
    db=session,
    user_id=123,
    session_id="user-abc123"
)

print(response["response"])  # Respuesta del chatbot
print(response["products"])  # Productos encontrados
```

### Estructura de Respuesta
```python
{
    "response": "¡Encontré laptops gaming perfectas para ti!...",
    "intent": "buscar_producto",
    "entities": {
        "producto": "laptop",
        "uso": "gaming",
        "presupuesto": 3000
    },
    "products": [
        {
            "id": 1,
            "name": "ASUS ROG Strix G15",
            "price": 2999.00,
            "stock_quantity": 5
        }
    ],
    "conversation_id": "user-abc123"
}
```

---

## 🔄 Flujo de Funcionamiento

```mermaid
graph TD
    A[Usuario envía mensaje] --> B[EnhancedInfotecChatbotV4]
    B --> C[EntityExtractor: Analizar mensaje]
    C --> D{¿Busca productos?}
    D -->|Sí| E[ProductService: Buscar productos]
    D -->|No| F[AIResponseGenerator: Respuesta general]
    E --> G[ResponseFormatter: Formatear productos]
    F --> G
    G --> H[ConversationManager: Guardar contexto]
    H --> I[Retornar respuesta al usuario]
```

---

## ✅ Beneficios de la Modularización

### 🧩 **Separación de Responsabilidades**
- Cada módulo tiene una función específica y bien definida
- Fácil localizar funcionalidades específicas

### 🔧 **Mantenibilidad Mejorada**
- Cambios en un módulo no afectan otros
- Código más limpio y organizado

### 🧪 **Facilidad de Testing**
- Cada módulo se puede probar independientemente
- Tests más específicos y eficientes

### 📈 **Escalabilidad**
- Fácil agregar nuevas funcionalidades
- Estructura preparada para crecimiento

### 🔄 **Reutilización**
- Módulos pueden usarse en otros proyectos
- Componentes independientes y modulares

### 🐛 **Debugging Simplificado**
- Errores más fáciles de localizar
- Logs más específicos por módulo

---

## 🛠️ Configuración y Dependencias

### Variables de Entorno Requeridas
```bash
GOOGLE_API_KEY=tu-google-gemini-api-key
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

### Dependencias Python
```bash
pip install google-generativeai sqlalchemy pydantic fastapi
```

---

## 📊 Métricas y Estadísticas

El chatbot incluye endpoints para monitoreo:

### Limpiar Historial
```http
POST /api/clear-history
{
    "session_id": "opcional"
}
```

### Obtener Estadísticas
```http
GET /api/conversation-stats?session_id=opcional
```

**Respuesta:**
```json
{
    "total_sessions": 5,
    "total_messages": 147,
    "active_sessions": ["user-1", "user-2", "user-3"]
}
```

---