from flask import request, current_app
from flask_restful import Resource
from marshmallow import ValidationError
from ...extensions import db
from ...models.imovel import Imovel
from ..schemas.imovel_schema import ImovelSchema
from ..utils.hypermedia import HypermediaBuilder

# Instanciar schemas
imovel_schema = ImovelSchema()
imoveis_schema = ImovelSchema(many=True)

class ImovelResource(Resource):
    """Recurso para operações em um imóvel específico."""
    
    def __init__(self, **kwargs):
        """Inicializa o recurso com parâmetros opcionais."""
        self.endpoint = kwargs.get('endpoint', None)
    
    def get(self, id):
        """Obter um imóvel pelo ID."""
        imovel = Imovel.query.get_or_404(id)
        result = imovel_schema.dump(imovel)
        
        # Adicionar links HATEOAS
        result = HypermediaBuilder.add_links(result, id, 'imoveis')
        
        return result, 200
    
    def put(self, id):
        """Atualizar um imóvel existente."""
        imovel = Imovel.query.get_or_404(id)
        json_data = request.get_json() or {}
        
        try:
            # Validar dados com marshmallow
            data = imovel_schema.load(json_data, partial=True, instance=imovel)
            
            # Salvar imóvel atualizado
            db.session.add(data)
            db.session.commit()
            
            result = imovel_schema.dump(data)
            
            # Adicionar links HATEOAS
            result = HypermediaBuilder.add_links(result, id, 'imoveis')
            
            return result, 200
            
        except ValidationError as err:
            return {"message": "Erro de validação", "errors": err.messages}, 400
    
    def delete(self, id):
        """Remover um imóvel."""
        imovel = Imovel.query.get_or_404(id)
        
        db.session.delete(imovel)
        db.session.commit()
        
        return "", 204

class ImoveisResource(Resource):
    """Recurso para operações na coleção de imóveis."""
    
    def get(self):
        """Listar todos os imóveis."""
        imoveis = Imovel.query.all()
        result = imoveis_schema.dump(imoveis)
        
        # Adicionar links HATEOAS para cada imóvel
        for item in result:
            item = HypermediaBuilder.add_links(item, item['id'], 'imoveis')
        
        # Adicionar links para a coleção
        collection = {
            "count": len(result),
            "items": result,
            "_links": {
                "self": {
                    "href": request.url,
                    "method": "GET"
                },
                "create": {
                    "href": request.url,
                    "method": "POST"
                }
            }
        }
        
        return collection, 200
    
    def post(self):
        """Criar um novo imóvel."""
        json_data = request.get_json() or {}
        
        try:
            # Validar dados com marshmallow
            imovel = imovel_schema.load(json_data)
            
            # Salvar novo imóvel
            db.session.add(imovel)
            db.session.commit()
            
            result = imovel_schema.dump(imovel)
            
            # Adicionar links HATEOAS
            result = HypermediaBuilder.add_links(result, imovel.id, 'imoveis')
            
            return result, 201
            
        except ValidationError as err:
            return {"message": "Erro de validação", "errors": err.messages}, 400

class ImovelTipoResource(Resource):
    """Recurso para filtrar imóveis por tipo."""
    
    def get(self, tipo):
        """Listar imóveis por tipo."""
        imoveis = Imovel.query.filter_by(tipo=tipo).all()
        result = imoveis_schema.dump(imoveis)
        
        # Adicionar links HATEOAS para cada imóvel
        for item in result:
            item = HypermediaBuilder.add_links(item, item['id'], 'imoveis')
        
        # Adicionar links para a coleção
        collection = {
            "count": len(result),
            "items": result,
            "_links": {
                "self": {
                    "href": request.url,
                    "method": "GET"
                },
                "all": {
                    "href": request.url_root + "api/imoveis",
                    "method": "GET"
                }
            }
        }
        
        return collection, 200

class ImovelCidadeResource(Resource):
    """Recurso para filtrar imóveis por cidade."""
    
    def get(self, cidade):
        """Listar imóveis por cidade."""
        imoveis = Imovel.query.filter_by(cidade=cidade).all()
        result = imoveis_schema.dump(imoveis)
        
        # Adicionar links HATEOAS para cada imóvel
        for item in result:
            item = HypermediaBuilder.add_links(item, item['id'], 'imoveis')
        
        # Adicionar links para a coleção
        collection = {
            "count": len(result),
            "items": result,
            "_links": {
                "self": {
                    "href": request.url,
                    "method": "GET"
                },
                "all": {
                    "href": request.url_root + "api/imoveis",
                    "method": "GET"
                }
            }
        }
        
        return collection, 200 