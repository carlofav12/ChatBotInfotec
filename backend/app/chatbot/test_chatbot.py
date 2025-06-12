"""
Test de funcionalidades del chatbot - GRUPO INFOTEC
Este script permite probar las diferentes funcionalidades del chatbot
"""
import os
import sys
import logging
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

# Agregar directorio padre al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Importar los módulos necesarios
from app.database import SessionLocal
from app.chatbot.core.enhanced_chatbot_v4_fixed import EnhancedInfotecChatbotV4
from app.chatbot.services.intent_classifier import IntentClassifier

# Obtener la API key de las variables de entorno
API_KEY = os.getenv("GEMINI_API_KEY")

# Función para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Obtener una instancia de la sesión de base de datos
db = next(get_db())

# Crear instancia del chatbot
chatbot = EnhancedInfotecChatbotV4(API_KEY)

# Crear instancia del clasificador de intenciones
intent_classifier = IntentClassifier(API_KEY)

def test_intent_classification(message):
    """Probar la clasificación de intenciones"""
    print(f"\n{'='*50}")
    print(f"PRUEBA DE CLASIFICACIÓN DE INTENCIONES: '{message}'")
    print(f"{'='*50}")
    
    # Clasificar la intención
    intent_result = intent_classifier.classify_intent(message)
    
    # Mostrar el resultado
    print(f"Intención detectada: {intent_result['intent']}")
    print(f"Confianza: {intent_result['confidence']}")
    print(f"Razonamiento: {intent_result.get('reasoning', 'No proporcionado')}")
    print(f"Mostrar productos: {intent_result['should_show_products']}")
    print(f"Entidades: {intent_result.get('entities', {})}")
    
    return intent_result

def test_chatbot_response(message, user_id=1, session_id="test_session"):
    """Probar la respuesta completa del chatbot"""
    print(f"\n{'='*50}")
    print(f"PRUEBA DE RESPUESTA DEL CHATBOT: '{message}'")
    print(f"{'='*50}")
    
    # Procesar el mensaje
    response = chatbot.process_message(message, db, user_id, session_id)
    
    # Mostrar el resultado
    print(f"Respuesta: {response['response']}")
    print(f"Intención: {response['intent']}")
    print(f"Entidades: {response['entities']}")
    print(f"Productos encontrados: {len(response['products'])}")
    
    # Mostrar nombres de productos encontrados
    if response['products']:
        print("\nProductos encontrados:")
        for i, product in enumerate(response['products'], 1):
            if hasattr(product, 'name'):
                print(f"{i}. {product.name}")
            elif isinstance(product, dict) and 'name' in product:
                print(f"{i}. {product['name']}")
            else:
                print(f"{i}. {product}")
    
    return response

def test_contextual_reference(session_id="test_session"):
    """Probar referencias contextuales a productos previos"""
    print(f"\n{'='*50}")
    print(f"PRUEBA DE REFERENCIAS CONTEXTUALES")
    print(f"{'='*50}")
    
    # Primero mostrar productos
    print("1. Mostrando productos:")
    response1 = chatbot.process_message("muéstrame laptops gaming", db, 1, session_id)
    print(f"Productos encontrados: {len(response1['products'])}")
    
    # Ahora pedir detalles del segundo producto
    print("\n2. Solicitando especificaciones del segundo producto:")
    response2 = chatbot.process_message("muéstrame las especificaciones de la segunda", db, 1, session_id)
    print(f"Respuesta: {response2['response']}")
    
    return response1, response2

def test_best_product_query(session_id="test_session"):
    """Probar consulta de mejor producto"""
    print(f"\n{'='*50}")
    print(f"PRUEBA DE CONSULTA 'MEJOR PRODUCTO'")
    print(f"{'='*50}")
    
    # Probar con diferentes frases
    queries = [
        "¿Cuál es la mejor laptop que tienes?",
        "Dame la mejor PC de escritorio",
        "Necesito la mejor laptop para gaming",
        "¿Cuál es la mejor?"
    ]
    
    results = []
    for query in queries:
        print(f"\nProbando: '{query}'")
        response = chatbot.process_message(query, db, 1, session_id)
        print(f"Intención: {response['intent']}")
        print(f"Productos encontrados: {len(response['products'])}")
        results.append(response)
    
    return results

def test_similar_products(session_id="test_session"):
    """Probar búsqueda de productos similares"""
    print(f"\n{'='*50}")
    print(f"PRUEBA DE BÚSQUEDA DE PRODUCTOS SIMILARES")
    print(f"{'='*50}")
    
    # Crear un nombre de producto que probablemente no exista exactamente
    test_cases = [
        "laptop dell gaming i7 16gb",
        "pc hp de oficina con intel",
        "monitor samsung 24 pulgadas",
        "Lenovo ThinkPad X1 Carbon"
    ]
    
    results = []
    for test_case in test_cases:
        print(f"\nBuscando productos similares a: '{test_case}'")
        similar_products = chatbot.product_service.find_similar_products(db, test_case, limit=3)
        
        print(f"Productos similares encontrados: {len(similar_products)}")
        for i, product in enumerate(similar_products, 1):
            print(f"{i}. {product.name}")
        
        results.append(similar_products)
    
    return results

def test_tech_questions(session_id="test_session"):
    """Probar preguntas tecnológicas vs búsqueda de productos"""
    print(f"\n{'='*50}")
    print(f"PRUEBA DE PREGUNTAS TECNOLÓGICAS VS BÚSQUEDA DE PRODUCTOS")
    print(f"{'='*50}")
    
    tech_questions = [
        "¿Qué es mejor AMD o Intel?",
        "¿Cuál es la diferencia entre SSD y HDD?",
        "¿Qué procesador es más rápido?",
        "¿Intel o AMD para gaming?"
    ]
    
    product_questions = [
        "¿Qué laptop es mejor para programación?",
        "¿Cuál es la mejor laptop que tienes?",
        "Necesito una PC para diseño gráfico",
        "¿Tienes laptops con AMD?"
    ]
    
    results = []
    
    print("\nPROBANDO PREGUNTAS TECNOLÓGICAS:")
    for question in tech_questions:
        intent = test_intent_classification(question)
        results.append(intent)
    
    print("\nPROBANDO PREGUNTAS DE PRODUCTOS:")
    for question in product_questions:
        intent = test_intent_classification(question)
        results.append(intent)
    
    return results

if __name__ == "__main__":
    # Menú de pruebas
    while True:
        print("\n")
        print("=" * 50)
        print("SISTEMA DE PRUEBAS DEL CHATBOT - GRUPO INFOTEC")
        print("=" * 50)
        print("1. Probar clasificación de intenciones")
        print("2. Probar respuesta completa del chatbot")
        print("3. Probar referencias contextuales")
        print("4. Probar consulta de mejor producto")
        print("5. Probar búsqueda de productos similares")
        print("6. Probar preguntas tecnológicas vs búsqueda de productos")
        print("0. Salir")
        
        option = input("\nSeleccione una opción: ")
        
        if option == "1":
            message = input("Ingrese un mensaje para clasificar: ")
            test_intent_classification(message)
        
        elif option == "2":
            message = input("Ingrese un mensaje para procesar: ")
            test_chatbot_response(message)
        
        elif option == "3":
            test_contextual_reference()
        
        elif option == "4":
            test_best_product_query()
        
        elif option == "5":
            test_similar_products()
        
        elif option == "6":
            test_tech_questions()
        
        elif option == "0":
            print("\n¡Hasta pronto!")
            sys.exit(0)
        
        else:
            print("\nOpción no válida. Intente nuevamente.")
        
        input("\nPresione Enter para continuar...")
