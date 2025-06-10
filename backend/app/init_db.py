# Script para inicializar la base de datos con datos de ejemplo
import os
import sys
from sqlalchemy.orm import Session
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, SessionLocal, Base, create_tables
from app.crud import create_category, create_product, create_user
from app.models import CategoryCreate, ProductCreate, UserCreate

def init_database():
    """Inicializar base de datos con datos de ejemplo"""
    print("🚀 Inicializando base de datos...")
    
    # Crear tablas
    create_tables()
    print("✅ Tablas creadas")
    
    # Crear sesión
    db = SessionLocal()
    
    try:
        # Crear categorías
        categories_data = [
            {"name": "Laptops", "description": "Laptops y notebooks", "slug": "laptops"},
            {"name": "PC Gaming", "description": "Computadoras de alto rendimiento para gaming", "slug": "pc-gaming"},
            {"name": "Monitores", "description": "Monitores y pantallas", "slug": "monitores"},
            {"name": "Periféricos", "description": "Teclados, ratones y accesorios", "slug": "perifericos"},
            {"name": "Componentes", "description": "Procesadores, memorias, tarjetas gráficas", "slug": "componentes"},
            {"name": "Oficina", "description": "Equipos para oficina y trabajo", "slug": "oficina"}
        ]
        
        print("📁 Creando categorías...")
        categories = {}
        for cat_data in categories_data:
            category = create_category(db, CategoryCreate(**cat_data))
            categories[cat_data["slug"]] = category.id
            print(f"   ✓ {cat_data['name']}")
        
        # Crear productos de ejemplo
        products_data = [
            # Laptops
            {
                "name": "Laptop HP Pavilion Gaming 15.6\" Intel Core i5 16GB RAM 512GB SSD",
                "description": "Laptop gaming con procesador Intel Core i5, 16GB RAM, 512GB SSD, tarjeta gráfica dedicada. Ideal para gaming y trabajo.",
                "price": 3299.00,
                "original_price": 3899.00,
                "sku": "HP-PAV-I5-16-512",
                "stock_quantity": 15,
                "brand": "HP",
                "model": "Pavilion Gaming 15",
                "specifications": '{"processor": "Intel Core i5-11400H", "ram": "16GB DDR4", "storage": "512GB SSD", "graphics": "GTX 1650", "display": "15.6\\" FHD"}',
                "image_url": "/api/placeholder/300/200",
                "rating": 4.5,
                "review_count": 24,
                "is_featured": True,
                "is_new": True,
                "category_id": categories["laptops"]
            },
            {
                "name": "Laptop ASUS ROG Strix G15 AMD Ryzen 7 RTX 4060 16GB",
                "description": "Laptop gaming de alta gama con AMD Ryzen 7, RTX 4060, 16GB RAM. Perfecto para gaming profesional.",
                "price": 5499.00,
                "original_price": 5999.00,
                "sku": "ASUS-ROG-R7-4060",
                "stock_quantity": 8,
                "brand": "ASUS",
                "model": "ROG Strix G15",
                "specifications": '{"processor": "AMD Ryzen 7 6800H", "ram": "16GB DDR5", "storage": "1TB SSD", "graphics": "RTX 4060", "display": "15.6\\" FHD 144Hz"}',
                "image_url": "/api/placeholder/300/200",
                "rating": 4.8,
                "review_count": 28,
                "is_featured": True,
                "is_new": True,
                "category_id": categories["laptops"]
            },
            
            # PC Gaming
            {
                "name": "PC Gamer AMD Ryzen 5 RTX 4060 16GB RAM 1TB SSD",
                "description": "PC gaming completo con Ryzen 5, RTX 4060, 16GB RAM, 1TB SSD. Rendimiento excepcional para gaming 1080p.",
                "price": 4599.00,
                "original_price": 5199.00,
                "sku": "PC-R5-4060-16GB",
                "stock_quantity": 12,
                "brand": "INFOTEC",
                "model": "Gaming Pro",
                "specifications": '{"processor": "AMD Ryzen 5 5600X", "ram": "16GB DDR4", "storage": "1TB NVMe SSD", "graphics": "RTX 4060", "motherboard": "B450M", "psu": "650W 80+"}',
                "image_url": "/api/placeholder/300/200",
                "rating": 4.7,
                "review_count": 18,
                "is_featured": True,
                "is_new": True,
                "category_id": categories["pc-gaming"]
            },
            
            # Monitores
            {
                "name": "Monitor Gamer Asus 24\" 144Hz 1ms FHD",
                "description": "Monitor gaming de 24 pulgadas, 144Hz, 1ms de respuesta, Full HD. Perfecto para competitivo.",
                "price": 899.00,
                "original_price": 1099.00,
                "sku": "ASUS-24-144HZ",
                "stock_quantity": 25,
                "brand": "ASUS",
                "model": "VG248QG",
                "specifications": '{"size": "24\\"", "resolution": "1920x1080", "refresh_rate": "144Hz", "response_time": "1ms", "panel": "TN"}',
                "image_url": "/api/placeholder/300/200",
                "rating": 4.6,
                "review_count": 32,
                "is_featured": True,
                "is_new": True,
                "category_id": categories["monitores"]
            },
            
            # Periféricos
            {
                "name": "Teclado Mecánico RGB Gamer Logitech G915",
                "description": "Teclado mecánico inalámbrico con switches táctiles, iluminación RGB personalizable.",
                "price": 649.00,
                "sku": "LOG-G915-RGB",
                "stock_quantity": 20,
                "brand": "Logitech",
                "model": "G915",
                "specifications": '{"type": "Mecánico", "connectivity": "Inalámbrico/USB", "switches": "GL Tactile", "lighting": "RGB", "battery": "40h"}',
                "image_url": "/api/placeholder/300/200",
                "rating": 4.4,
                "review_count": 15,
                "category_id": categories["perifericos"]
            },
            
            # Componentes
            {
                "name": "Procesador AMD Ryzen 7 5800X",
                "description": "Procesador de 8 núcleos y 16 hilos, ideal para gaming y creación de contenido.",
                "price": 1299.00,
                "original_price": 1499.00,
                "sku": "AMD-R7-5800X",
                "stock_quantity": 30,
                "brand": "AMD",
                "model": "Ryzen 7 5800X",
                "specifications": '{"cores": 8, "threads": 16, "base_clock": "3.8GHz", "boost_clock": "4.7GHz", "cache": "32MB L3", "tdp": "105W"}',
                "image_url": "/api/placeholder/300/200",
                "rating": 4.9,
                "review_count": 45,
                "is_featured": True,
                "category_id": categories["componentes"]
            },
            
            # Oficina
            {
                "name": "PC Oficina Intel Core i3 8GB RAM 256GB SSD",
                "description": "PC para oficina con Intel Core i3, 8GB RAM, 256GB SSD. Ideal para tareas administrativas.",
                "price": 1899.00,
                "sku": "PC-I3-8GB-256",
                "stock_quantity": 18,
                "brand": "INFOTEC",
                "model": "Office Essential",
                "specifications": '{"processor": "Intel Core i3-12100", "ram": "8GB DDR4", "storage": "256GB SSD", "graphics": "Integrada", "connectivity": "WiFi + Ethernet"}',
                "image_url": "/api/placeholder/300/200",
                "rating": 4.2,
                "review_count": 22,
                "category_id": categories["oficina"]
            },
            
            # Más productos para variedad
            {
                "name": "Laptop Lenovo Legion 5 AMD Ryzen 7 RTX 4070 32GB",
                "description": "Laptop gaming premium con Ryzen 7, RTX 4070, 32GB RAM. El máximo rendimiento.",
                "price": 6899.00,
                "original_price": 7499.00,
                "sku": "LEN-LEG5-R7-4070",
                "stock_quantity": 5,
                "brand": "Lenovo",
                "model": "Legion 5",
                "specifications": '{"processor": "AMD Ryzen 7 6800H", "ram": "32GB DDR5", "storage": "1TB SSD", "graphics": "RTX 4070", "display": "15.6\\" QHD 165Hz"}',
                "image_url": "/api/placeholder/300/200",
                "rating": 4.9,
                "review_count": 22,
                "is_featured": True,
                "category_id": categories["laptops"]
            }
        ]
        
        print("🛍️ Creando productos...")
        for product_data in products_data:
            product = create_product(db, ProductCreate(**product_data))
            print(f"   ✓ {product_data['name'][:50]}...")
        
        # Crear usuario de ejemplo
        user_data = {
            "username": "cliente_ejemplo",
            "email": "cliente@ejemplo.com",
            "full_name": "Cliente Ejemplo",
            "phone": "+51 999 888 777",
            "address": "Av. Ejemplo 123, Lima, Perú"
        }
        
        print("👤 Creando usuario de ejemplo...")
        user = create_user(db, UserCreate(**user_data))
        print(f"   ✓ Usuario: {user.full_name}")
        
        print("🎉 ¡Base de datos inicializada correctamente!")
        print(f"📊 Creadas {len(categories_data)} categorías y {len(products_data)} productos")
        
    except Exception as e:
        print(f"❌ Error inicializando base de datos: {e}")
        db.rollback()
    finally:
        db.close()

def init_sample_data(db: Session):
    """Initialize database with sample data using provided session"""
    try:
        from app.crud import create_category, create_product, create_user
        from app.models import CategoryCreate, ProductCreate, UserCreate
        
        # Create categories
        categories_data = [
            {"name": "Laptops", "description": "Laptops y notebooks", "slug": "laptops"},
            {"name": "PC Gaming", "description": "Computadoras de alto rendimiento para gaming", "slug": "pc-gaming"},
            {"name": "Monitores", "description": "Monitores y pantallas", "slug": "monitores"},
            {"name": "Periféricos", "description": "Teclados, ratones y accesorios", "slug": "perifericos"},
            {"name": "Componentes", "description": "Procesadores, memorias, tarjetas gráficas", "slug": "componentes"},
            {"name": "Oficina", "description": "Equipos para oficina y trabajo", "slug": "oficina"}
        ]
        
        categories = {}
        for cat_data in categories_data:
            category = create_category(db, CategoryCreate(**cat_data))
            categories[cat_data["slug"]] = category.id
        
        # Create sample products
        products_data = [
            {
                "name": "Laptop HP Pavilion Gaming 15.6\" Intel Core i5 16GB RAM 512GB SSD",
                "description": "Laptop gaming con procesador Intel Core i5, 16GB RAM, 512GB SSD, tarjeta gráfica dedicada.",
                "price": 3299.00,
                "original_price": 3899.00,
                "sku": "HP-PAV-I5-16-512",
                "stock_quantity": 15,
                "brand": "HP",
                "model": "Pavilion Gaming 15",
                "specifications": '{"processor": "Intel Core i5-11400H", "ram": "16GB DDR4", "storage": "512GB SSD"}',
                "image_url": "/api/placeholder/300/200",
                "rating": 4.5,
                "review_count": 24,
                "is_featured": True,
                "is_new": True,
                "category_id": categories["laptops"]
            },
            {
                "name": "PC Gamer AMD Ryzen 5 RTX 4060 16GB RAM 1TB SSD",
                "description": "PC gaming completo con Ryzen 5, RTX 4060, 16GB RAM, 1TB SSD.",
                "price": 4599.00,
                "original_price": 5199.00,
                "sku": "PC-R5-4060-16GB",
                "stock_quantity": 12,
                "brand": "INFOTEC",
                "model": "Gaming Pro",
                "specifications": '{"processor": "AMD Ryzen 5 5600X", "ram": "16GB DDR4", "storage": "1TB SSD"}',
                "image_url": "/api/placeholder/300/200",
                "rating": 4.7,
                "review_count": 18,
                "is_featured": True,
                "category_id": categories["pc-gaming"]
            }
        ]
        
        for product_data in products_data:
            create_product(db, ProductCreate(**product_data))
        
        # Create sample user
        user_data = {
            "username": "cliente_ejemplo",
            "email": "cliente@ejemplo.com",
            "full_name": "Cliente Ejemplo",
            "phone": "+51 999 888 777",
            "address": "Av. Ejemplo 123, Lima, Perú"
        }
        
        create_user(db, UserCreate(**user_data))
        
    except Exception as e:
        print(f"Error initializing sample data: {e}")
        db.rollback()
        raise

if __name__ == "__main__":
    init_database()
