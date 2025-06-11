# InfoBot GRUPO INFOTEC 🤖💻

Chatbot inteligente modularizado desarrollado para GRUPO INFOTEC - Empresa líder en Tecnología y Servicios Informáticos en Perú.

## ✨ Características Principales

- 🧠 **IA Conversacional Avanzada** - Powered by Google Gemini AI
- 🛍️ **E-commerce Integrado** - Búsqueda y venta de productos
- 🏗️ **Arquitectura Modular** - Código organizado y escalable
- 💬 **Contexto Conversacional** - Memoria de conversaciones
- 📱 **Interfaz Moderna** - UI/UX optimizada
- 🚀 **Alto Rendimiento** - APIs rápidas y eficientes

## 🏗️ Arquitectura Modularizada

El chatbot ha sido completamente refactorizado en una arquitectura modular:

```
backend/app/chatbot/
├── core/                    # Núcleo del sistema
│   ├── config.py           # Configuraciones centrales
│   └── enhanced_chatbot_v4.py  # Orquestador principal
├── services/               # Servicios de negocio
│   ├── product_service.py  # Gestión de productos
│   └── ai_response_generator.py  # IA conversacional
└── utils/                  # Utilidades especializadas
    ├── entity_extractor.py # Análisis de mensajes
    ├── response_formatter.py # Formateo de respuestas
    └── conversation_manager.py # Gestión de contexto
```

## 🚀 Tecnologías Utilizadas

### Backend
- **FastAPI** - Framework web moderno para APIs
- **Google Gemini AI** - Modelo de inteligencia artificial generativa
- **Python 3.11+** - Lenguaje de programación
- **PostgreSQL** - Base de datos relacional
- **SQLAlchemy** - ORM para Python
- **Uvicorn** - Servidor ASGI de alto rendimiento

### Frontend
- **React 19** - Biblioteca de JavaScript para interfaces de usuario
- **TypeScript** - Superset de JavaScript con tipado estático
- **TanStack Query** - Manejo de estado del servidor
- **Tailwind CSS** - Framework de CSS utilitario
- **Lucide React** - Iconos modernos

## 📦 Instalación y Configuración

### Prerrequisitos
- Python 3.8 o superior
- Node.js 16 o superior
- npm o yarn
- API Key de Google Gemini

## Ejecución

### Iniciar el Backend
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Iniciar el Frontend
```bash
cd frontend
npm start
```

## 🌐 URLs de Acceso

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs
- **Redoc**: http://localhost:8000/redoc

## 🔧 Configuración del Chatbot

El chatbot está configurado específicamente para GRUPO INFOTEC con:

## 📁 Estructura del Proyecto

```
chatbot-web-fullstack/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # Aplicación principal FastAPI
│   │   ├── chatbot.py       # Lógica del chatbot con Gemini
│   │   ├── models.py        # Modelos de datos Pydantic
│   │   └── config.py        # Configuración de la aplicación
│   ├── requirements.txt     # Dependencias de Python
│   └── .env                 # Variables de entorno
├── frontend/
│   ├── src/
│   │   ├── components/      # Componentes React
│   │   ├── hooks/          # Hooks personalizados
│   │   ├── services/       # Servicios de API
│   │   └── App.tsx         # Componente principal
│   ├── package.json        # Dependencias de Node.js
│   └── public/             # Archivos estáticos
└── README.md               # Este archivo
```

## 🔑 Variables de Entorno

Crear un archivo `.env` en el directorio `backend/` con:

```env
GOOGLE_API_KEY=tu_api_key_de_google_gemini
```

## 🛠️ API Endpoints

### Principales
- `POST /api/chat` - Enviar mensaje al chatbot
- `GET /api/history` - Obtener historial de conversación
- `POST /api/clear-history` - Limpiar historial
- `GET /api/stats` - Obtener estadísticas de uso

### Utilidad
- `GET /health` - Verificación de salud del servicio
- `GET /` - Información básica de la API