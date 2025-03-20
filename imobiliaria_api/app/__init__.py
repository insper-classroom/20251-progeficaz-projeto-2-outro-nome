from flask import Flask
from .config import config
from . import extensions, api, models

def create_app(config_name='default'):
    """
    Função de fábrica para criar a aplicação Flask.
    
    Args:
        config_name (str): Nome da configuração a ser usada
        
    Returns:
        Flask: Aplicação Flask configurada
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Inicializar extensões
    extensions.init_app(app)
    
    # Registrar blueprints
    api.init_app(app)
    
    # Configurar tratamento de erros
    configure_error_handlers(app)
    
    return app
    
def configure_error_handlers(app):
    """
    Configura os manipuladores de erro para a aplicação.
    
    Args:
        app (Flask): Aplicação Flask
    """
    @app.errorhandler(404)
    def not_found(error):
        return {
            'error': 'Not Found',
            'message': 'O recurso solicitado não foi encontrado',
            'status': 404
        }, 404
        
    @app.errorhandler(400)
    def bad_request(error):
        return {
            'error': 'Bad Request',
            'message': 'Os dados fornecidos são inválidos ou incompletos',
            'status': 400
        }, 400
        
    @app.errorhandler(500)
    def internal_server_error(error):
        return {
            'error': 'Internal Server Error',
            'message': 'Ocorreu um erro interno no servidor',
            'status': 500
        }, 500
