import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    """Configuração base para todas as configurações."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-secreta-padrao'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Definir a URL do banco de dados de forma segura
    db_url = os.environ.get('DATABASE_URL')
    if db_url and db_url.startswith('sqlite:'):
        # SQLite
        SQLALCHEMY_DATABASE_URI = db_url
    else:
        # Fallback para SQLite se a URL não for válida
        SQLALCHEMY_DATABASE_URI = 'sqlite:///imobiliaria.db'
    
    API_TITLE = os.environ.get('API_TITLE', 'Imobiliaria API')
    API_VERSION = os.environ.get('API_VERSION', '1.0')
    API_DESCRIPTION = os.environ.get('API_DESCRIPTION', 'API RESTful para gerenciamento de imóveis')

class DevelopmentConfig(Config):
    """Configuração para ambiente de desenvolvimento."""
    DEBUG = True

class TestingConfig(Config):
    """Configuração para ambiente de testes."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Usar banco de dados em memória para testes

class ProductionConfig(Config):
    """Configuração para ambiente de produção."""
    DEBUG = False
    TESTING = False

# Dicionário de configurações disponíveis
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
