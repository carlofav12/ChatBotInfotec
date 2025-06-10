# InfoBot GRUPO INFOTEC 🤖💻

Chatbot inteligente desarrollado en base de la empresa GRUPO INFOTEC - Empresa de Tecnología y Servicios.

## 🚀 Tecnologías Utilizadas

### Backend
- **FastAPI** - Framework web moderno para APIs
- **Google Gemini AI** - Modelo de inteligencia artificial generativa
- **Python 3.8+** - Lenguaje de programación
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