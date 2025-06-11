# filepath: backend/app/chatbot/services/product_service_improved.py
"""
Servicio mejorado para búsqueda y manejo de productos
Maneja las operaciones relacionadas con búsqueda, especificaciones y carrito
"""
import logging
from typing import List, Optional, Dict, Any
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
    
    def get_comparison_data(
        self, 
        db: Session, 
        product_names: List[str], 
        brand_names: List[str], 
        attributes: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Obtiene datos de productos para comparación.
        product_names: Lista de nombres de productos.
        brand_names: Lista de nombres de marcas.
        attributes: Lista de atributos a extraer (ej: ["precio", "bateria"]).
                    Si "caracteristicas" está en attributes, se devuelven todos los datos relevantes.        """
        
        # Import the missing function
        from app.crud import get_products_by_names_or_brands_for_comparison
        
        db_products = get_products_by_names_or_brands_for_comparison(
            db, 
            product_names=product_names, 
            brand_names=brand_names, 
            limit_per_item=2 # Obtener hasta 2 productos por nombre/marca para dar opciones
        )

        if not db_products:
            return []

        comparison_results = []
        for product_db in db_products:
            try:
                product_model = ProductModel.from_orm(product_db)
            except Exception as e:
                logger.warning(f"Error convirtiendo producto DB a Pydantic model: {product_db.name}, error: {e}")
                continue

            product_data = {}
            
            # Siempre incluir nombre, id y precio base para identificación
            product_data["id"] = product_model.id
            product_data["name"] = product_model.name
            product_data["price"] = product_model.price # Precio base siempre

            # Mapeo de atributos solicitados a campos del modelo o lógica especial
            attribute_map = {
                "precio": "price",
                "bateria": "battery_life", # Asumiendo que existe un campo battery_life
                "pantalla": "screen_specifications", # Asumiendo campo
                "rendimiento": "performance_score", # Asumiendo campo
                "camara": "camera_specifications", # Asumiendo campo
                "almacenamiento": "storage_capacity", # Asumiendo campo
                "ram": "ram_amount", # Asumiendo campo
                "procesador": "processor_model", # Asumiendo campo
                "tarjeta grafica": "graphics_card_model", # Asumiendo campo                "peso": "weight_kg", # Asumiendo campo
                "dimensiones": "dimensions_cm", # Asumiendo campo
                "marca": "brand_name", # Asumiendo que se puede extraer o ya existe
                # "caracteristicas" se maneja especialmente
            }
            
            if "caracteristicas" in attributes or not attributes:
                # Devolver un conjunto razonable de datos.
                product_data["stock_quantity"] = product_model.stock_quantity
                product_data["description"] = product_model.description if hasattr(product_model, 'description') else "N/A"
                product_data["category_id"] = getattr(product_model, 'category_id', "N/A")
                product_data["rating"] = getattr(product_model, 'rating', "N/A")
                # Añadir más campos relevantes si existen en ProductModel
                if hasattr(product_model, 'specifications') and product_model.specifications:
                     if isinstance(product_model.specifications, dict):
                        product_data.update(product_model.specifications)
                     else:
                        product_data['other_specifications'] = str(product_model.specifications)

                # Incluir atributos mapeados si no están ya
                for req_attr, model_attr_name in attribute_map.items():
                    if req_attr not in product_data and hasattr(product_model, model_attr_name):
                        product_data[req_attr] = getattr(product_model, model_attr_name, "N/A")
            else:
                for req_attr in attributes:
                    if req_attr == "precio": # Ya incluido
                        continue
                    model_attr_key = attribute_map.get(req_attr)
                    if model_attr_key and hasattr(product_model, model_attr_key):
                        product_data[req_attr] = getattr(product_model, model_attr_key, "N/A")
                    elif hasattr(product_model, req_attr): # Intento directo
                         product_data[req_attr] = getattr(product_model, req_attr, "N/A")
                    else:
                        # Si el atributo no se encuentra directamente o mapeado,
                        # podríamos intentar buscarlo en un campo genérico de especificaciones si existe
                        if hasattr(product_model, 'specifications') and isinstance(product_model.specifications, dict):
                            product_data[req_attr] = product_model.specifications.get(req_attr, "N/A")
                        else:
                            product_data[req_attr] = "N/A (no especificado)"
            
            # Intentar obtener la marca si no está ya
            if "marca" not in product_data or product_data["marca"] == "N/A":
                extracted_brand = "Desconocida"
                for brand_config in self.config.BRANDS: # Usar self.config de EntityExtractor
                    if brand_config.lower() in product_model.name.lower():
                        extracted_brand = brand_config.capitalize()
                        break
                product_data["marca"] = extracted_brand

            comparison_results.append(product_data)
            
        return comparison_results

    def add_to_cart(self, db: Session, product_id: int, quantity: int = 1, 
                    user_id: Optional[int] = None, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Agregar producto al carrito - Versión mejorada con mejor respuesta"""
        try:
            # Verificar que el producto existe y tiene stock
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                logger.warning(f"Producto {product_id} no encontrado")
                return {
                    "success": False,
                    "message": "❌ Producto no encontrado en nuestro inventario",
                    "product": None
                }
            
            # Convertir a modelo Pydantic para evitar errores de tipado
            try:
                product_model = ProductModel.from_orm(product)
                # Verificar stock disponible
                if product_model.stock_quantity < quantity:
                    logger.warning(f"Stock insuficiente. Disponible: {product_model.stock_quantity}, Solicitado: {quantity}")
                    return {
                        "success": False,
                        "message": f"⚠️ Stock insuficiente. Solo quedan **{product_model.stock_quantity}** unidades disponibles",
                        "product": product_model,
                        "available_stock": product_model.stock_quantity
                    }
            except Exception as model_error:
                logger.error(f"Error convirtiendo producto a modelo: {model_error}")
                return {
                    "success": False,
                    "message": "❌ Error procesando el producto. Inténtalo nuevamente.",
                    "product": None
                }
            
            logger.info(f"Agregando producto {product_id} al carrito (cantidad: {quantity})")
            
            # Usar CRUD para agregar al carrito
            from app.crud import add_to_cart as crud_add_to_cart
            
            # Si no hay user_id, usar un user_id temporal (1) para pruebas
            effective_user_id = user_id if user_id else 1
            
            try:
                cart_item = crud_add_to_cart(
                    db=db,
                    user_id=effective_user_id,
                    product_id=product_id,
                    quantity=quantity
                )
                
                # Hacer commit explícito para asegurar que se guarde
                db.commit()
                
                if cart_item:
                    logger.info(f"Producto {product_id} agregado exitosamente al carrito")
                    
                    # Calcular total del carrito actualizado
                    from app.crud import get_cart_total
                    cart_total = get_cart_total(db, effective_user_id)
                    
                    return {
                        "success": True,
                        "message": "✅ Producto agregado exitosamente al carrito",
                        "product": product_model,
                        "quantity": quantity,
                        "cart_item_id": cart_item.id,
                        "cart_total": cart_total,
                        "user_id": effective_user_id,
                        "item_subtotal": product_model.price * quantity
                    }
                else:
                    logger.warning(f"No se pudo agregar producto {product_id} al carrito")
                    return {
                        "success": False,
                        "message": "❌ No se pudo agregar el producto al carrito. Inténtalo nuevamente.",
                        "product": product_model
                    }
                    
            except Exception as db_error:
                logger.error(f"Error de base de datos al agregar al carrito: {db_error}")
                db.rollback()
                return {
                    "success": False,
                    "message": "❌ Error de conexión con la base de datos. Inténtalo nuevamente.",
                    "product": product_model
                }
                
        except Exception as e:
            logger.error(f"Error general agregando al carrito: {e}")
            return {
                "success": False,
                "message": "❌ Error interno del sistema. Contacta al soporte técnico de GRUPO INFOTEC.",
                "product": None
            }
