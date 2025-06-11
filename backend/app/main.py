from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import logging
import os
from dotenv import load_dotenv
from typing import List, Optional

# Cargar variables de entorno
load_dotenv()

# Importar nuestros módulos
from app.models import (
    ChatMessage, ChatResponse, HealthCheck,
    ProductResponse, CategoryResponse, CartResponse, OrderResponse,
    ProductCreate, CategoryCreate, CartItemCreate, OrderCreate
)
from app.chatbot import EnhancedInfotecChatbotV4  # Usar la nueva versión modularizada V4
from app.database import get_db, create_tables
from app import crud
from sqlalchemy.orm import Session

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear instancia de FastAPI
app = FastAPI(
    title="InfoBot GRUPO INFOTEC E-commerce API",
    description="API REST para el chatbot inteligente con capacidades de e-commerce - GRUPO INFOTEC",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS para permitir el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Instancia global del chatbot
enhanced_chatbot_instance = None

def get_enhanced_chatbot() -> EnhancedInfotecChatbotV4:
    """Dependency injection para el chatbot mejorado V3"""
    global enhanced_chatbot_instance
    if enhanced_chatbot_instance is None:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="Google API Key no configurada")
        enhanced_chatbot_instance = EnhancedInfotecChatbotV4(api_key)
    return enhanced_chatbot_instance

@app.on_event("startup")
async def startup_event():
    """Evento de inicio: inicializar base de datos y chatbot"""
    logger.info("🚀 Iniciando InfoBot E-commerce API...")
    try:
        # Crear tablas de base de datos
        create_tables()
        logger.info("✅ Base de datos PostgreSQL inicializada correctamente")
        
        # Verificar API key
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            logger.error("❌ GOOGLE_API_KEY no encontrada en variables de entorno")
            raise Exception("API Key no configurada")
            
        logger.info("✅ API iniciada correctamente")
        logger.info("🌐 API disponible en http://localhost:8000")
        logger.info("📚 Documentación en http://localhost:8000/docs")
        logger.info("🗄️ Base de datos PostgreSQL conectada")
        
    except Exception as e:
        logger.error(f"❌ Error en startup: {e}")
        raise

# =======================
# ENDPOINTS DE SALUD
# =======================

@app.get("/", response_model=HealthCheck)
async def read_root():
    """Endpoint raíz con información básica de la API"""
    return HealthCheck(
        status="healthy - InfoBot GRUPO INFOTEC E-commerce Ready",
        timestamp=datetime.now(),
        version="2.0.0"
    )

@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Endpoint de verificación de salud"""
    return HealthCheck(
        status="healthy",
        timestamp=datetime.now(),
        version="2.0.0"
    )

# =======================
# ENDPOINTS DE CHAT
# =======================

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(
        message: ChatMessage,
    db: Session = Depends(get_db),
    chatbot: EnhancedInfotecChatbotV4 = Depends(get_enhanced_chatbot)
):
    """Endpoint principal para chatear con InfoBot V3 mejorado"""
    try:
        logger.info(f"💬 Nueva consulta: {message.message[:50]}...")
        
        # Validar mensaje
        if not message.message or not message.message.strip():
            return ChatResponse(
                response="¡Hola! Soy InfoBot de GRUPO INFOTEC 🤖. ¿En qué puedo ayudarte hoy?",
                timestamp=datetime.now(),
                intent="saludo",
                entities={},
                products=[]
            )
        
        if len(message.message) > 1000:
            raise HTTPException(status_code=400, detail="El mensaje es demasiado largo (máximo 1000 caracteres)")
        
        # Generar respuesta con el chatbot V3 mejorado
        response_data = chatbot.process_message(
            message=message.message.strip(), 
            db=db,
            user_id=None,
            session_id=message.session_id or "default"
        )
        
        # Crear respuesta estructurada
        response = ChatResponse(
            response=response_data.get("response", "Lo siento, no pude procesar tu solicitud."),
            timestamp=datetime.now(),
            tokens_used=None,
            intent=response_data.get("intent", "general"),
            entities=response_data.get("entities", {}),
            products=response_data.get("products", []),
            cart_total=response_data.get("cart_total")        )
        logger.info(f"✅ Respuesta V3 generada exitosamente - Intent: {response.intent}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error en chat endpoint V3: {e}")
        # Respuesta de fallback amigable
        return ChatResponse(
            response="Disculpa, tuve un problema técnico momentáneo. ¿Podrías repetir tu mensaje? Estoy aquí para ayudarte 🤖",
            timestamp=datetime.now(),
            intent="error",
            entities={},
            products=[]
        )

# =======================
# ENDPOINTS DE PRODUCTOS
# =======================

@app.get("/api/products", response_model=List[ProductResponse])
async def get_products(
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,  # Aumentado a 100 por defecto
    db: Session = Depends(get_db)
):
    """Obtener lista de productos"""
    try:
        if search:
            products = crud.search_products(db, search, limit)
        elif category_id:
            products = crud.get_products(db, skip, limit, category_id)
        else:
            products = crud.get_products(db, skip, limit)
        
        return [ProductResponse.from_orm(p) for p in products]
    except Exception as e:
        logger.error(f"Error obteniendo productos: {e}")
        raise HTTPException(status_code=500, detail="Error obteniendo productos")

@app.get("/api/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Obtener un producto específico"""
    try:
        product = crud.get_product(db, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return ProductResponse.from_orm(product)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo producto: {e}")
        raise HTTPException(status_code=500, detail="Error obteniendo producto")

@app.get("/api/categories", response_model=List[CategoryResponse])
async def get_categories(db: Session = Depends(get_db)):
    """Obtener lista de categorías"""
    try:
        categories = crud.get_categories(db)
        return [CategoryResponse.from_orm(c) for c in categories]
    except Exception as e:
        logger.error(f"Error obteniendo categorías: {e}")
        raise HTTPException(status_code=500, detail="Error obteniendo categorías")

# =======================
# ENDPOINTS DE CARRITO
# =======================

@app.get("/api/cart/{user_id}", response_model=CartResponse)
async def get_cart(user_id: int, db: Session = Depends(get_db)):
    """Obtener carrito de usuario"""
    try:
        cart = crud.get_or_create_cart(db, user_id=user_id)
        # Get cart ID safely 
        from sqlalchemy import text
        cart_id_result = db.execute(text("SELECT id FROM carts WHERE user_id = :user_id"), {"user_id": user_id}).first()
        cart_id = cart_id_result[0] if cart_id_result else None
        
        if cart_id:
            cart_items_data = crud.get_cart_items(db, cart_id)
            cart_total = crud.get_cart_total(db, user_id)
            
            return CartResponse(
                items=[],  # TODO: Convertir items correctamente 
                total=cart_total,
                item_count=len(cart_items_data) if cart_items_data else 0
            )
        else:
            return CartResponse(items=[], total=0.0, item_count=0)
    except Exception as e:
        logger.error(f"Error obteniendo carrito: {e}")
        raise HTTPException(status_code=500, detail="Error obteniendo carrito")

@app.post("/api/cart")
async def add_to_cart(
    item: CartItemCreate,
    db: Session = Depends(get_db)
):
    """Agregar producto al carrito"""
    try:
        cart_item = crud.add_to_cart(db, item.user_id, item.product_id, item.quantity)
        if cart_item:
            return {"message": "Producto agregado al carrito", "item_id": cart_item.id}
        else:
            raise HTTPException(status_code=400, detail="No se pudo agregar el producto al carrito")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error agregando al carrito: {e}")
        raise HTTPException(status_code=500, detail="Error agregando al carrito")

@app.put("/api/cart/{item_id}")
async def update_cart_item(
    item_id: str,  # Changed to str to match CRUD function
    quantity: int,
    db: Session = Depends(get_db)
):
    """Actualizar cantidad en carrito"""
    try:
        updated_item = crud.update_cart_item(db, item_id, quantity)
        if not updated_item:
            raise HTTPException(status_code=404, detail="Item de carrito no encontrado")
        return {"message": "Carrito actualizado"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error actualizando carrito: {e}")
        raise HTTPException(status_code=500, detail="Error actualizando carrito")

@app.delete("/api/cart/{item_id}")
async def remove_from_cart(item_id: str, db: Session = Depends(get_db)):  # Changed to str
    """Eliminar producto del carrito"""
    try:
        success = crud.remove_from_cart(db, item_id)
        if not success:
            raise HTTPException(status_code=404, detail="Item de carrito no encontrado")
        return {"message": "Producto eliminado del carrito"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error eliminando del carrito: {e}")
        raise HTTPException(status_code=500, detail="Error eliminando del carrito")

# =======================
# ENDPOINTS DE ÓRDENES
# =======================

@app.post("/api/orders", response_model=OrderResponse)
async def create_order(
    order: OrderCreate,
    user_id: int,  # Add user_id parameter
    db: Session = Depends(get_db)
):
    """Crear nueva orden"""
    try:
        # Get user's cart
        cart = crud.get_or_create_cart(db, user_id=user_id)
        from sqlalchemy import text
        cart_id_result = db.execute(text("SELECT id FROM carts WHERE user_id = :user_id"), {"user_id": user_id}).first()
        cart_id = cart_id_result[0] if cart_id_result else None
        
        if not cart_id:
            raise HTTPException(status_code=400, detail="No se encontró carrito para el usuario")
        
        new_order = crud.create_order(db, order, user_id, cart_id)
        if not new_order:
            raise HTTPException(status_code=400, detail="Error creando orden")
        return OrderResponse.from_orm(new_order)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creando orden: {e}")
        raise HTTPException(status_code=500, detail="Error creando orden")

@app.get("/api/orders/{user_id}", response_model=List[OrderResponse])
async def get_user_orders(user_id: int, db: Session = Depends(get_db)):
    """Obtener órdenes de usuario"""
    try:
        orders = crud.get_user_orders(db, user_id)
        return [OrderResponse.from_orm(o) for o in orders]
    except Exception as e:
        logger.error(f"Error obteniendo órdenes: {e}")
        raise HTTPException(status_code=500, detail="Error obteniendo órdenes")

# =======================
# ENDPOINTS DE INICIALIZACIÓN
# =======================

@app.post("/api/init-db")
async def initialize_database(db: Session = Depends(get_db)):
    """Inicializar base de datos con datos de muestra"""
    try:
        # Importar y ejecutar script de inicialización
        from app.init_db import init_sample_data
        init_sample_data(db)
        return {"message": "Base de datos inicializada con datos de muestra"}
    except Exception as e:
        logger.error(f"Error inicializando base de datos: {e}")
        raise HTTPException(status_code=500, detail="Error inicializando base de datos")

# =======================
# MANEJADOR DE EXCEPCIONES
# =======================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Manejador global de excepciones"""
    logger.error(f"Error no manejado: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor"}
    )

@app.post("/api/clear-history")
async def clear_conversation_history(
    session_id: Optional[str] = None,
    chatbot: EnhancedInfotecChatbotV4 = Depends(get_enhanced_chatbot)
):
    """Limpiar historial de conversación para una sesión específica"""
    try:
        if session_id:
            chatbot.clear_session(session_id)
            logger.info(f"🗑️ Historial limpiado para sesión: {session_id}")
        else:
            # Limpiar todas las sesiones
            active_sessions = chatbot.conversation_manager.get_active_sessions()
            for session in active_sessions:
                chatbot.clear_session(session)
            logger.info("🗑️ Todos los historiales limpiados")
        
        return {"status": "success", "message": "Historial limpiado correctamente"}
        
    except Exception as e:
        logger.error(f"❌ Error limpiando historial: {e}")
        raise HTTPException(status_code=500, detail="Error limpiando historial")

@app.get("/api/conversation-stats")
async def get_conversation_stats(
    session_id: Optional[str] = None,
    chatbot: EnhancedInfotecChatbotV4 = Depends(get_enhanced_chatbot)
):
    """Obtener estadísticas de conversación"""
    try:
        if session_id:
            stats = chatbot.conversation_manager.get_session_stats(session_id)
            return {
                "session_id": session_id,
                **stats
            }
        else:
            active_sessions = chatbot.conversation_manager.get_active_sessions()
            total_sessions = len(active_sessions)
            total_messages = sum(
                len(chatbot.conversation_manager.get_conversation_history(session)) 
                for session in active_sessions
            )
            return {
                "total_sessions": total_sessions,
                "total_messages": total_messages,
                "active_sessions": active_sessions
            }
            
    except Exception as e:
        logger.error(f"❌ Error obteniendo estadísticas: {e}")
        raise HTTPException(status_code=500, detail="Error obteniendo estadísticas")

# =====================
# ENDPOINTS DE PRODUCTOS
# =====================