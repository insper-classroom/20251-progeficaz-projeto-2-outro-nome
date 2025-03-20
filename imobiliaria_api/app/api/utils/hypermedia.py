from flask import url_for, request

class HypermediaBuilder:
    """
    Classe utilitária para adicionar links HATEOAS (Hypermedia as the Engine of Application State)
    às respostas da API.
    """
    
    @staticmethod
    def add_links(resource, resource_id=None, resource_type=None):
        """
        Adiciona links relacionados ao recurso.
        
        Args:
            resource (dict): O recurso a ser enriquecido com links
            resource_id (int, optional): ID do recurso
            resource_type (str, optional): Tipo do recurso ('imoveis', 'usuarios', etc.)
            
        Returns:
            dict: O recurso com links HATEOAS adicionados
        """
        if not resource_type:
            return resource
            
        # Adicionar _links ao recurso
        if '_links' not in resource:
            resource['_links'] = {}
            
        # Adicionar link self
        if resource_id:
            resource['_links']['self'] = {
                'href': url_for('api.get_imovel', id=resource_id, _external=True),
                'method': 'GET'
            }
            
        # Adicionar outros links específicos por tipo de recurso
        if resource_type == 'imoveis':
            if resource_id:
                # Links para o próprio recurso
                resource['_links']['update'] = {
                    'href': url_for('api.update_imovel', id=resource_id, _external=True),
                    'method': 'PUT'
                }
                resource['_links']['delete'] = {
                    'href': url_for('api.delete_imovel', id=resource_id, _external=True),
                    'method': 'DELETE'
                }
            
            # Links relacionados à coleção
            resource['_links']['collection'] = {
                'href': url_for('api.list_imoveis', _external=True),
                'method': 'GET'
            }
            
            if resource_id is None:  # É uma coleção
                resource['_links']['create'] = {
                    'href': url_for('api.create_imovel', _external=True),
                    'method': 'POST'
                }
            
            # Adicionar links para filtragem
            if 'tipo' in resource:
                resource['_links']['filtrar_por_tipo'] = {
                    'href': url_for('api.list_imoveis_by_tipo', tipo=resource['tipo'], _external=True),
                    'method': 'GET'
                }
            if 'cidade' in resource:
                resource['_links']['filtrar_por_cidade'] = {
                    'href': url_for('api.list_imoveis_by_cidade', cidade=resource['cidade'], _external=True),
                    'method': 'GET'
                }
                
        return resource
        
    @staticmethod
    def add_pagination_links(collection, endpoint, page, per_page, total):
        """
        Adiciona links de paginação à coleção.
        
        Args:
            collection (dict): A coleção a ser enriquecida com links
            endpoint (str): O endpoint base
            page (int): Página atual
            per_page (int): Itens por página
            total (int): Total de itens
            
        Returns:
            dict: A coleção com links de paginação adicionados
        """
        # Inicializar links se não existir
        if '_links' not in collection:
            collection['_links'] = {}
            
        # Adicionar links de paginação
        total_pages = (total // per_page) + (1 if total % per_page > 0 else 0)
        
        # Link para a página atual
        collection['_links']['self'] = {
            'href': url_for(endpoint, page=page, per_page=per_page, _external=True),
            'method': 'GET'
        }
        
        # Link para a primeira página
        collection['_links']['first'] = {
            'href': url_for(endpoint, page=1, per_page=per_page, _external=True),
            'method': 'GET'
        }
        
        # Link para a última página
        collection['_links']['last'] = {
            'href': url_for(endpoint, page=total_pages, per_page=per_page, _external=True),
            'method': 'GET'
        }
        
        # Link para a próxima página
        if page < total_pages:
            collection['_links']['next'] = {
                'href': url_for(endpoint, page=page+1, per_page=per_page, _external=True),
                'method': 'GET'
            }
            
        # Link para a página anterior
        if page > 1:
            collection['_links']['prev'] = {
                'href': url_for(endpoint, page=page-1, per_page=per_page, _external=True),
                'method': 'GET'
            }
            
        return collection 