from flask import Blueprint
from flask_restful import Api
from .resources import (
    ImovelResource,
    ImoveisResource,
    ImovelTipoResource,
    ImovelCidadeResource
)

# Criar um Blueprint para a API
api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)

# Registrar os endpoints
api.add_resource(ImoveisResource, '/imoveis', endpoint='list_imoveis')
api.add_resource(ImovelResource, '/imoveis/<int:id>', 
                 endpoint='get_imovel',
                 resource_class_kwargs={'endpoint': 'get_imovel'})
api.add_resource(ImovelResource, '/imoveis/<int:id>', 
                 endpoint='update_imovel',
                 resource_class_kwargs={'endpoint': 'update_imovel'})
api.add_resource(ImovelResource, '/imoveis/<int:id>', 
                 endpoint='delete_imovel',
                 resource_class_kwargs={'endpoint': 'delete_imovel'})
api.add_resource(ImovelTipoResource, '/imoveis/tipo/<string:tipo>', endpoint='list_imoveis_by_tipo')
api.add_resource(ImovelCidadeResource, '/imoveis/cidade/<string:cidade>', endpoint='list_imoveis_by_cidade')

def init_app(app):
    """Inicializa a API com a aplicação Flask."""
    app.register_blueprint(api_bp)
    return app
