import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Script para poblar la base de datos con laptops de la imagen
from app.database import SessionLocal, Product, Category
from app.models import ProductCreate

# Datos de laptops extraídos de la imagen (puedes agregar más)
laptops = [
    {
        "name": "Laptop Lenovo V15 G4 AMN Ryzen 5 7520U 8GB 256GB SSD 15.6 FHD",
        "description": "Laptop ideal para estudiantes y oficina, pantalla 15.6'' FHD, Ryzen 5, 8GB RAM, 256GB SSD.",
        "price": 1049.0,
        "original_price": 1312.0,
        "sku": "LENOVO-V15G4-R5-8-256",
        "stock_quantity": 10,
        "brand": "Lenovo",
        "model": "V15 G4 AMN",
        "specifications": "Ryzen 5 7520U, 8GB RAM, 256GB SSD, 15.6'' FHD",
        "image_url": "https://infotecperu.com.pe/img/laptops/lenovo-v15g4-r5.jpg"
    },
    {
        "name": "Laptop HP 15-fc0048la Ryzen 7 7730U 8GB 512GB SSD 15.6 FHD",
        "description": "Laptop HP para universidad y trabajo, Ryzen 7, 8GB RAM, 512GB SSD, pantalla 15.6'' FHD.",
        "price": 1549.0,
        "original_price": 1937.0,
        "sku": "HP-15FC0048LA-R7-8-512",
        "stock_quantity": 8,
        "brand": "HP",
        "model": "15-fc0048la",
        "specifications": "Ryzen 7 7730U, 8GB RAM, 512GB SSD, 15.6'' FHD",
        "image_url": "https://infotecperu.com.pe/img/laptops/hp-15fc0048la-r7.jpg"
    },
    {
        "name": "Laptop ASUS Vivobook Go 15 E1504FA N4500 8GB 256GB SSD 15.6 FHD",
        "description": "ASUS Vivobook Go, portátil ligera para estudiantes, N4500, 8GB RAM, 256GB SSD.",
        "price": 1269.0,
        "original_price": 1587.0,
        "sku": "ASUS-E1504FA-N4500-8-256",
        "stock_quantity": 12,
        "brand": "ASUS",
        "model": "Vivobook Go 15 E1504FA",
        "specifications": "Intel N4500, 8GB RAM, 256GB SSD, 15.6'' FHD",
        "image_url": "https://infotecperu.com.pe/img/laptops/asus-vivobook-e1504fa.jpg"
    },
    {
        "name": "Laptop Dell Inspiron 3520 i7 1255U 16GB 512GB SSD 15.6 FHD",
        "description": "Dell Inspiron para alto rendimiento, i7 12va gen, 16GB RAM, 512GB SSD, 15.6'' FHD.",
        "price": 2259.0,
        "original_price": 2824.0,
        "sku": "DELL-3520-I7-16-512",
        "stock_quantity": 7,
        "brand": "Dell",
        "model": "Inspiron 3520",
        "specifications": "i7-1255U, 16GB RAM, 512GB SSD, 15.6'' FHD",
        "image_url": "https://infotecperu.com.pe/img/laptops/dell-inspiron-3520-i7.jpg"
    },
    {
        "name": "Laptop Lenovo V15 G4 I3 1315U 8GB 512GB SSD 15.6 FHD",
        "description": "Laptop Lenovo V15 G4, Intel Core i3 13va gen, 8GB RAM, 512GB SSD, ideal para estudiantes.",
        "price": 1229.0,
        "original_price": 1639.0,
        "sku": "LENOVO-V15G4-I3-8-512",
        "stock_quantity": 10,
        "brand": "Lenovo",
        "model": "V15 G4 I3",
        "specifications": "Intel Core i3-1315U, 8GB RAM, 512GB SSD, 15.6'' FHD",
        "image_url": "https://infotecperu.com.pe/img/laptops/lenovo-v15g4-i3.jpg"
    },
    {
        "name": "Laptop HP 14-ep0011la Core Ultra 5 125H 16GB 512GB SSD 14 FHD",
        "description": "HP 14 pulgadas, Core Ultra 5, 16GB RAM, 512GB SSD, portátil y potente.",
        "price": 2519.0,
        "original_price": 3142.0,
        "sku": "HP-14EP0011LA-U5-16-512",
        "stock_quantity": 7,
        "brand": "HP",
        "model": "14-ep0011la",
        "specifications": "Core Ultra 5 125H, 16GB RAM, 512GB SSD, 14'' FHD",
        "image_url": "https://infotecperu.com.pe/img/laptops/hp-14ep0011la.jpg"
    },
    {
        "name": "Laptop Lenovo IdeaPad Flex 5 14ABR8 Ryzen 7 7730U 16GB 512GB SSD 14 FHD Táctil",
        "description": "Convertible Lenovo IdeaPad Flex 5, Ryzen 7, 16GB RAM, 512GB SSD, pantalla táctil.",
        "price": 2899.0,
        "original_price": 3624.0,
        "sku": "LENOVO-FLEX5-14ABR8-R7-16-512",
        "stock_quantity": 6,
        "brand": "Lenovo",
        "model": "IdeaPad Flex 5 14ABR8",
        "specifications": "Ryzen 7 7730U, 16GB RAM, 512GB SSD, 14'' FHD táctil",
        "image_url": "https://infotecperu.com.pe/img/laptops/lenovo-flex5-14abr8.jpg"
    },
    {
        "name": "Laptop ASUS Vivobook 16X K3605VA-MB1235 I7-13620H 16GB 512GB SSD 16 FHD",
        "description": "ASUS Vivobook 16X, i7 13va gen, 16GB RAM, 512GB SSD, pantalla grande 16'' FHD.",
        "price": 2929.0,
        "original_price": 3906.0,
        "sku": "ASUS-K3605VA-I7-16-512",
        "stock_quantity": 5,
        "brand": "ASUS",
        "model": "Vivobook 16X K3605VA",
        "specifications": "Intel Core i7-13620H, 16GB RAM, 512GB SSD, 16'' FHD",
        "image_url": "https://infotecperu.com.pe/img/laptops/asus-vivobook-16x.jpg"
    },
    {
        "name": "Laptop Lenovo Yoga 7 14ARB7 2EN1 Ryzen 5 7530U 16GB 512GB SSD 14 FHD Touch",
        "description": "Lenovo Yoga 7 convertible, Ryzen 5, 16GB RAM, 512GB SSD, pantalla táctil 14'' FHD.",
        "price": 2779.0,
        "original_price": 3970.0,
        "sku": "LENOVO-YOGA7-14ARB7-R5-16-512",
        "stock_quantity": 4,
        "brand": "Lenovo",
        "model": "Yoga 7 14ARB7",
        "specifications": "Ryzen 5 7530U, 16GB RAM, 512GB SSD, 14'' FHD Touch",
        "image_url": "https://infotecperu.com.pe/img/laptops/lenovo-yoga7-14arb7.jpg"
    },
    {
        "name": "Laptop HP ENVY X360 14-EU0132LA 2 EN 1 CORE I5 16GB 512GB 14 FHD TOUCH SCREEN",
        "description": "HP Envy X360 convertible, Core i5, 16GB RAM, 512GB SSD, pantalla táctil 14'' FHD.",
        "price": 2819.0,
        "original_price": 3759.0,
        "sku": "HP-ENVYX360-14EU0132LA-I5-16-512",
        "stock_quantity": 5,
        "brand": "HP",
        "model": "ENVY X360 14-EU0132LA",
        "specifications": "Core i5, 16GB RAM, 512GB SSD, 14'' FHD Touch",
        "image_url": "https://infotecperu.com.pe/img/laptops/hp-envyx360-14eu0132la.jpg"
    },
    {
        "name": "Laptop Lenovo IdeaPad Slim 3 15IRH8 I7-13620H 16GB 1TB SSD 15.6 FHD",
        "description": "Lenovo IdeaPad Slim 3, i7 13va gen, 16GB RAM, 1TB SSD, pantalla 15.6'' FHD.",
        "price": 2579.0,
        "original_price": 3432.0,
        "sku": "LENOVO-SLIM3-15IRH8-I7-16-1TB",
        "stock_quantity": 6,
        "brand": "Lenovo",
        "model": "IdeaPad Slim 3 15IRH8",
        "specifications": "Intel Core i7-13620H, 16GB RAM, 1TB SSD, 15.6'' FHD",
        "image_url": "https://infotecperu.com.pe/img/laptops/lenovo-slim3-15irh8.jpg"
    },
    {
        "name": "Laptop ASUS Vivobook 15 Flip TP3404VA-VS511 13TH I5 16GB 1TB 15.6 WUXGA TÁCTIL",
        "description": "ASUS Vivobook 15 Flip, i5 13va gen, 16GB RAM, 1TB SSD, pantalla táctil 15.6'' WUXGA.",
        "price": 2629.0,
        "original_price": 3505.0,
        "sku": "ASUS-TP3404VA-I5-16-1TB",
        "stock_quantity": 4,
        "brand": "ASUS",
        "model": "Vivobook 15 Flip TP3404VA",
        "specifications": "Intel Core i5-1335U, 16GB RAM, 1TB SSD, 15.6'' WUXGA táctil",
        "image_url": "https://infotecperu.com.pe/img/laptops/asus-vivobook-15flip.jpg"
    },
    {
        "name": "Laptop Lenovo IdeaPad Flex 5 14IAU7 I7-1255U 16GB 512GB SSD 14 FHD WINDOWS 11",
        "description": "Lenovo IdeaPad Flex 5 convertible, i7 12va gen, 16GB RAM, 512GB SSD, pantalla 14'' FHD.",
        "price": 2969.0,
        "original_price": 3959.0,
        "sku": "LENOVO-FLEX5-14IAU7-I7-16-512",
        "stock_quantity": 5,
        "brand": "Lenovo",
        "model": "IdeaPad Flex 5 14IAU7",
        "specifications": "Intel Core i7-1255U, 16GB RAM, 512GB SSD, 14'' FHD",
        "image_url": "https://infotecperu.com.pe/img/laptops/lenovo-flex5-14iau7.jpg"
    }
    # ...puedes seguir agregando más modelos si lo deseas...
]

def main():
    db = SessionLocal()
    # Buscar o crear la categoría "Laptops"
    category = db.query(Category).filter(Category.name == "Laptops").first()
    if not category:
        category = Category(name="Laptops", description="Laptops y portátiles", slug="laptops")
        db.add(category)
        db.commit()
        db.refresh(category)
    for l in laptops:
        # Evitar duplicados por SKU
        exists = db.query(Product).filter(Product.sku == l["sku"]).first()
        if exists:
            print(f"Producto ya existe: {l['sku']}")
            continue
        product = Product(
            name=l["name"],
            description=l["description"],
            price=l["price"],
            original_price=l["original_price"],
            sku=l["sku"],
            stock_quantity=l["stock_quantity"],
            brand=l["brand"],
            model=l["model"],
            specifications=l["specifications"],
            image_url=l["image_url"],
            category_id=category.id,
            is_active=True,
            is_featured=False,
            is_new=True
        )
        db.add(product)
        print(f"Agregado: {l['name']}")
    db.commit()
    db.close()

if __name__ == "__main__":
    main()
