#!/usr/bin/env python3
"""
Script de prueba para verificar las mejoras del chatbot InfoBot
Prueba específicamente:
1. Reconocimiento de "que especificacion tiene la Laptop HP Pavilion Gaming"
2. Reconocimiento de "puedes agregar la Laptop HP Pavilion Gaming"
3. Búsqueda mejorada de productos específicos
"""

import requests
import json

# Configuración
BASE_URL = "http://localhost:8000"
CHAT_ENDPOINT = f"{BASE_URL}/api/chat"

def test_chat_message(message, descripcion):
    """Envía un mensaje al chatbot y muestra la respuesta"""
    print(f"\n{'='*60}")
    print(f"PRUEBA: {descripcion}")
    print(f"{'='*60}")
    print(f"👤 Usuario: {message}")
    
    try:
        response = requests.post(
            CHAT_ENDPOINT,
            json={"message": message},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"🤖 InfoBot: {data.get('response', 'Sin respuesta')}")
            
            # Mostrar productos si los hay
            if 'products' in data and data['products']:
                print(f"\n📦 Productos encontrados ({len(data['products'])}):")
                for i, product in enumerate(data['products'], 1):
                    print(f"  {i}. {product['name']} - S/{product['price']}")
            
            # Mostrar entidades detectadas
            if 'entities' in data and data['entities']:
                print(f"\n🔍 Entidades detectadas:")
                for key, value in data['entities'].items():
                    print(f"  - {key}: {value}")
                    
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor. ¿Está ejecutándose?")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def main():
    """Ejecuta todas las pruebas"""
    print("🚀 INICIANDO PRUEBAS DE MEJORAS DEL CHATBOT INFOBOT")
    print("=" * 60)
    
    # Prueba 1: Solicitud de especificaciones
    test_chat_message(
        "que especificacion tiene la Laptop HP Pavilion Gaming",
        "Solicitud de especificaciones con 'que especificacion'"
    )
    
    # Prueba 2: Solicitud de especificaciones alternativa
    test_chat_message(
        "qué especificaciones tiene la HP Pavilion Gaming",
        "Solicitud de especificaciones con 'qué especificaciones'"
    )
    
    # Prueba 3: Agregar al carrito
    test_chat_message(
        "puedes agregar la Laptop HP Pavilion Gaming",
        "Agregar producto específico con 'puedes agregar'"
    )
    
    # Prueba 4: Agregar al carrito alternativo
    test_chat_message(
        "agrega la HP Pavilion Gaming al carrito",
        "Agregar producto específico con 'agrega'"
    )
    
    # Prueba 5: Búsqueda general HP Pavilion
    test_chat_message(
        "busco una HP Pavilion Gaming",
        "Búsqueda general de HP Pavilion Gaming"
    )
    
    # Prueba 6: Búsqueda con especificaciones
    test_chat_message(
        "necesito ver las especificaciones de la HP Pavilion",
        "Búsqueda con solicitud de especificaciones"
    )
    
    # Prueba 7: Búsqueda con palabras clave adicionales
    test_chat_message(
        "quiero una laptop HP Omen para gaming",
        "Búsqueda de HP Omen para gaming"
    )
    
    print(f"\n{'='*60}")
    print("✅ PRUEBAS COMPLETADAS")
    print("💡 Verifica que las entidades se detecten correctamente")
    print("💡 Verifica que los productos se encuentren adecuadamente")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
