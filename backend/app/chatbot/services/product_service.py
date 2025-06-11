# filepath: backend/app/chatbot/services/product_service.py
"""
Servicio para búsqueda y manejo de productos
Maneja las operaciones relacionadas con búsqueda, especificaciones y carrito
"""
import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from app.database import Product
from app.models import Product as ProductModel

logger = logging.getLogger(__name__)

class ProductService:
    """Servicio para operaciones con productos"""
    
    def search_products(self, db: Session, search_query: str, max_price: Optional[int] = None) -> List[ProductModel]:
        """Buscar productos en la base de datos"""
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
                    
                    # Filtrar por stock
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
        """Buscar producto específico por nombre"""
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
            
            logger.warning(f"No se encontró producto para: '{product_name}'")
            return None
            
        except Exception as e:
            logger.error(f"Error buscando producto por nombre '{product_name}': {e}")
            return None
    
    def add_to_cart(self, db: Session, product_id: int, quantity: int = 1, 
                    user_id: Optional[int] = None, session_id: Optional[str] = None) -> bool:
        """Agregar producto al carrito"""
        try:
            # Verificar que el producto existe y tiene stock
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                logger.warning(f"Producto {product_id} no encontrado")
                return False
            
            # Convertir a modelo Pydantic para evitar errores de tipado
            try:
                product_model = ProductModel.from_orm(product)
                # Verificar stock disponible
                if product_model.stock_quantity < quantity:
                    logger.warning(f"Stock insuficiente. Disponible: {product_model.stock_quantity}, Solicitado: {quantity}")
                    return False
            except Exception as model_error:
                logger.error(f"Error convirtiendo producto a modelo: {model_error}")
                return False
            
            logger.info(f"Agregando producto {product_id} al carrito (cantidad: {quantity})")
              # Usar CRUD para agregar al carrito
            from app.crud import add_to_cart as crud_add_to_cart
            
            # Si no hay user_id, usar un user_id temporal (1) para pruebas
            effective_user_id = user_id if user_id else 1
            
            cart_item = crud_add_to_cart(
                db=db,
                user_id=effective_user_id,
                product_id=product_id,
                quantity=quantity
            )
            
            if cart_item:
                logger.info(f"Producto {product_id} agregado exitosamente al carrito")
                return True
            else:
                logger.warning(f"No se pudo agregar producto {product_id} al carrito")
                return False
                
        except Exception as e:
            logger.error(f"Error agregando al carrito: {e}")
            return False
