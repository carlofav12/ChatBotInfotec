# CRUD operations for e-commerce
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
from app.database import User, Product, Category, Cart, Order, OrderItem, cart_items
from app.models import UserCreate, ProductCreate, CategoryCreate, OrderCreate
from datetime import datetime
import uuid

# User CRUD
def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

# Product CRUD
def create_product(db: Session, product: ProductCreate) -> Product:
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: int) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100, category_id: Optional[int] = None) -> List[Product]:
    query = db.query(Product).filter(Product.is_active == True)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    return query.offset(skip).limit(limit).all()

def search_products(db: Session, search_term: str, limit: int = 10) -> List[Product]:
    return db.query(Product).filter(
        Product.is_active == True,
        (Product.name.ilike(f"%{search_term}%") | 
         Product.description.ilike(f"%{search_term}%") |
         Product.brand.ilike(f"%{search_term}%"))
    ).limit(limit).all()

def get_featured_products(db: Session, limit: int = 8) -> List[Product]:
    return db.query(Product).filter(
        Product.is_active == True,
        Product.is_featured == True
    ).order_by(Product.rating.desc()).limit(limit).all()

def get_new_products(db: Session, limit: int = 8) -> List[Product]:
    return db.query(Product).filter(
        Product.is_active == True,
        Product.is_new == True
    ).order_by(Product.created_at.desc()).limit(limit).all()

# Category CRUD
def create_category(db: Session, category: CategoryCreate) -> Category:
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session) -> List[Category]:
    return db.query(Category).filter(Category.is_active == True).all()

def get_category(db: Session, category_id: int) -> Optional[Category]:
    return db.query(Category).filter(Category.id == category_id).first()

# Cart CRUD
def get_or_create_cart(db: Session, user_id: Optional[int] = None, session_id: Optional[str] = None) -> Cart:
    cart = None
    if user_id:
        cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    elif session_id:
        cart = db.query(Cart).filter(Cart.session_id == session_id).first()
    
    if not cart:
        cart = Cart(
            user_id=user_id,
            session_id=session_id,
            total_amount=0.0
        )
        db.add(cart)
        db.commit()
        db.refresh(cart)
    
    return cart

def get_cart_total(db: Session, user_id: int) -> float:
    """Get total amount for user's cart"""
    from sqlalchemy import text
    result = db.execute(text("SELECT total_amount FROM carts WHERE user_id = :user_id"), {"user_id": user_id}).first()
    return float(result[0]) if result else 0.0

def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int = 1):
    """Add product to cart - wrapper function for main.py"""
    cart = get_or_create_cart(db, user_id=user_id)
    # Get cart ID using safe query
    from sqlalchemy import text
    cart_id_result = db.execute(text("SELECT id FROM carts WHERE user_id = :user_id"), {"user_id": user_id}).first()
    cart_id = cart_id_result[0] if cart_id_result else None
    
    if cart_id:
        success = add_item_to_cart(db, cart_id, product_id, quantity)
        if success:
            # Return a mock object with id for compatibility
            class MockCartItem:
                def __init__(self, cart_id: int, product_id: int):
                    self.id = f"{cart_id}_{product_id}"
            return MockCartItem(cart_id, product_id)
    return None

def update_cart_item(db: Session, item_id: str, quantity: int):
    """Update cart item quantity - item_id is in format 'cart_id_product_id'"""
    try:
        cart_id, product_id = item_id.split('_')
        cart_id, product_id = int(cart_id), int(product_id)
        
        # Get current item
        from sqlalchemy import and_
        existing_item = db.execute(
            cart_items.select().where(
                and_(
                    cart_items.c.cart_id == cart_id,
                    cart_items.c.product_id == product_id
                )
            )
        ).first()
        
        if existing_item:
            # Get product price using safe query
            from sqlalchemy import text
            product_price_result = db.execute(text("SELECT price FROM products WHERE id = :product_id"), {"product_id": product_id}).first()
            if not product_price_result:
                return None
            
            # Calculate price difference
            old_quantity = existing_item.quantity
            product_price = float(product_price_result[0])
            price_diff = product_price * (quantity - old_quantity)
            
            # Update quantity
            db.execute(
                cart_items.update().where(
                    and_(
                        cart_items.c.cart_id == cart_id,
                        cart_items.c.product_id == product_id
                    )
                ).values(quantity=quantity)
            )
            
            # Update cart total using safe query
            db.execute(text("UPDATE carts SET total_amount = total_amount + :price_diff, updated_at = NOW() WHERE id = :cart_id"), 
                      {"price_diff": price_diff, "cart_id": cart_id})
            
            db.commit()
            return True
        return None
    except Exception as e:
        db.rollback()
        return None

def remove_from_cart(db: Session, item_id: str) -> bool:
    """Remove item from cart - item_id is in format 'cart_id_product_id'"""
    try:
        cart_id, product_id = item_id.split('_')
        cart_id, product_id = int(cart_id), int(product_id)
        return remove_item_from_cart(db, cart_id, product_id)
    except Exception:
        return False

def add_item_to_cart(db: Session, cart_id: int, product_id: int, quantity: int = 1) -> bool:
    try:
        # Verificar que el producto existe y tiene stock
        from sqlalchemy import text
        product_result = db.execute(text("SELECT id, price, stock_quantity FROM products WHERE id = :product_id"), 
                                  {"product_id": product_id}).first()
        if not product_result or product_result[2] < quantity:  # stock_quantity < quantity
            return False
        
        product_price = float(product_result[1])
        
        # Verificar si ya existe el item en el carrito
        from sqlalchemy import and_
        existing_item = db.execute(
            cart_items.select().where(
                and_(
                    cart_items.c.cart_id == cart_id,
                    cart_items.c.product_id == product_id
                )
            )
        ).first()
        
        if existing_item:
            # Actualizar cantidad
            new_quantity = existing_item.quantity + quantity
            db.execute(
                cart_items.update().where(
                    and_(
                        cart_items.c.cart_id == cart_id,
                        cart_items.c.product_id == product_id
                    )
                ).values(quantity=new_quantity)
            )
        else:
            # Crear nuevo item
            db.execute(
                cart_items.insert().values(
                    cart_id=cart_id,
                    product_id=product_id,
                    quantity=quantity
                )
            )
        
        # Actualizar total del carrito usando SQL directo
        db.execute(text("UPDATE carts SET total_amount = total_amount + :amount, updated_at = NOW() WHERE id = :cart_id"), 
                  {"amount": product_price * quantity, "cart_id": cart_id})
        
        db.commit()
        return True
        
    except Exception as e:
        db.rollback()
        return False

def remove_item_from_cart(db: Session, cart_id: int, product_id: int) -> bool:
    try:
        # Get product price and existing item info
        from sqlalchemy import text, and_
        product_result = db.execute(text("SELECT price FROM products WHERE id = :product_id"), 
                                  {"product_id": product_id}).first()
        if not product_result:
            return False
        
        product_price = float(product_result[0])
        
        # Obtener cantidad actual
        existing_item = db.execute(
            cart_items.select().where(
                and_(
                    cart_items.c.cart_id == cart_id,
                    cart_items.c.product_id == product_id
                )
            )
        ).first()
        
        if existing_item:
            item_quantity = existing_item.quantity
            
            # Eliminar item
            db.execute(
                cart_items.delete().where(
                    and_(
                        cart_items.c.cart_id == cart_id,
                        cart_items.c.product_id == product_id
                    )
                )
            )
            
            # Actualizar total del carrito usando SQL directo
            total_reduction = product_price * item_quantity
            db.execute(text("UPDATE carts SET total_amount = total_amount - :amount, updated_at = NOW() WHERE id = :cart_id"), 
                      {"amount": total_reduction, "cart_id": cart_id})
            
            db.commit()
            return True
        
        return False
        
    except Exception as e:
        db.rollback()
        return False

def get_cart_items(db: Session, cart_id: int):
    return db.execute(
        cart_items.select().where(cart_items.c.cart_id == cart_id)
    ).fetchall()

def clear_cart(db: Session, cart_id: int) -> bool:
    try:
        from sqlalchemy import text
        db.execute(cart_items.delete().where(cart_items.c.cart_id == cart_id))
        
        # Update cart total using SQL directo
        db.execute(text("UPDATE carts SET total_amount = 0.0, updated_at = NOW() WHERE id = :cart_id"), 
                  {"cart_id": cart_id})
        
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        return False

# Order CRUD
def create_order(db: Session, order_data: OrderCreate, user_id: int, cart_id: int) -> Optional[Order]:
    try:
        # Generar número de orden único
        order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
        
        # Obtener items del carrito
        cart_items_data = get_cart_items(db, cart_id)
        if not cart_items_data:
            return None
        
        # Calcular total
        total_amount = 0.0
        order_items_data = []
        
        for item in cart_items_data:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if product:
                item_total = product.price * item.quantity
                total_amount += item_total
                
                order_items_data.append({
                    "product_id": product.id,
                    "quantity": item.quantity,
                    "unit_price": product.price,
                    "total_price": item_total
                })
        
        # Crear orden
        db_order = Order(
            order_number=order_number,
            user_id=user_id,
            total_amount=total_amount,
            shipping_address=order_data.shipping_address,
            payment_method=order_data.payment_method,
            status="pending",
            payment_status="pending"
        )
        
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        
        # Crear items de la orden
        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=db_order.id,
                **item_data
            )
            db.add(order_item)
        
        # Limpiar carrito
        clear_cart(db, cart_id)
        
        db.commit()
        return db_order
        
    except Exception as e:
        db.rollback()
        return None

def get_user_orders(db: Session, user_id: int) -> List[Order]:
    return db.query(Order).filter(Order.user_id == user_id).order_by(Order.created_at.desc()).all()

def get_order(db: Session, order_id: int) -> Optional[Order]:
    return db.query(Order).filter(Order.id == order_id).first()

def update_order_status(db: Session, order_id: int, status: str) -> bool:
    try:
        from sqlalchemy import text
        # Update order status using SQL directo
        db.execute(text("UPDATE orders SET status = :status, updated_at = NOW() WHERE id = :order_id"), 
                   {"status": status, "order_id": order_id})
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        return False
    
def get_products_by_names_or_brands_for_comparison(
    db: Session, 
    product_names: List[str] = None, 
    brand_names: List[str] = None, 
    limit_per_item: int = 2
) -> List[Product]:
    """
    Recupera productos para comparación.
    Busca por nombres de producto exactos/parciales o por nombres de marca.
    Intenta obtener 'limit_per_item' para cada nombre/marca.
    """
    if not product_names and not brand_names:
        return []

    all_found_products_dict: Dict[int, Product] = {} # Usar dict para evitar duplicados por ID

    if product_names:
        for name_query in product_names:
            # Limpiar y dividir el nombre en palabras clave para una búsqueda más flexible
            keywords = [f"%{keyword.strip()}%" for keyword in name_query.split() if keyword.strip()]
            if not keywords:
                continue

            query = db.query(Product)
            # Aplicar un filtro AND para cada palabra clave dentro de un name_query
            # Ejemplo: "asus rog strix" -> name LIKE %asus% AND name LIKE %rog% AND name LIKE %strix%
            # También buscar por coincidencia parcial del nombre completo
            name_filters = [Product.name.ilike(kw) for kw in keywords]
            name_filters.append(Product.name.ilike(f"%{name_query.strip()}%")) # Coincidencia del nombre completo

            query = query.filter(or_(*name_filters))
            
            # Añadir filtro para no incluir productos ya encontrados
            if all_found_products_dict:
                query = query.filter(Product.id.notin_(list(all_found_products_dict.keys())))

            products_for_name = query.order_by(Product.rating.desc().nullslast(), Product.price.asc()).limit(limit_per_item).all()
            for p in products_for_name:
                if p.id not in all_found_products_dict:
                    all_found_products_dict[p.id] = p
    
    if brand_names:
        for brand_name in brand_names:
            # Asumimos que el nombre de la marca está en Product.name o en un campo/relación de marca.
            # Por ahora, buscamos en Product.name.
            # Si Product tiene un campo brand_id o brand.name (a través de una relación):
            # from app.models import Brand # Suponiendo que existe
            # query = db.query(Product).join(Brand).filter(Brand.name.ilike(f"%{brand_name}%"))
            query = db.query(Product).filter(Product.name.ilike(f"%{brand_name.strip()}%"))
            
            if all_found_products_dict:
                query = query.filter(Product.id.notin_(list(all_found_products_dict.keys())))
            
            products_for_brand = query.order_by(Product.rating.desc().nullslast(), Product.price.asc()).limit(limit_per_item).all()
            for p in products_for_brand:
                 if p.id not in all_found_products_dict:
                    all_found_products_dict[p.id] = p
                    
    return list(all_found_products_dict.values())