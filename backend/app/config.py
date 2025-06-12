# filepath: d:\USMP\ChatBotInfotec\backend\app\config.py
"""
Configuración de la aplicación
Incluye configuración de base de datos PostgreSQL en la nube
"""
import os
from typing import Optional

class Config:
    """Configuración base de la aplicación"""
    
    # Configuración de base de datos PostgreSQL
    # IMPORTANTE: Configura estas variables según tu instancia de PostgreSQL en la nube
    DATABASE_HOST = os.environ.get('DATABASE_HOST', 'localhost')
    DATABASE_PORT = os.environ.get('DATABASE_PORT', '5432')
    DATABASE_NAME = os.environ.get('DATABASE_NAME', 'infotec_chatbot')
    DATABASE_USER = os.environ.get('DATABASE_USER', 'postgres')
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD', '')
    
    # URL de conexión a PostgreSQL
    @classmethod
    def get_database_url(cls) -> str:
        """Construir URL de conexión a PostgreSQL"""
        return f"postgresql://{cls.DATABASE_USER}:{cls.DATABASE_PASSWORD}@{cls.DATABASE_HOST}:{cls.DATABASE_PORT}/{cls.DATABASE_NAME}"
    
    # Configuración de Gemini AI
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
    
    # Configuración de logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    # Configuración de sesión
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Configuración de CORS (para desarrollo)
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000,http://localhost:8080').split(',')

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False

# Configuración por defecto
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config() -> Config:
    """Obtener configuración basada en el entorno"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])