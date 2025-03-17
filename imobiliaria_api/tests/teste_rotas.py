import json
import pytest 
from unittest.mock import patch, MagicMock
from app import create_app
from app.models import Imovel



# FIXTURE: setar as configurações para teste 
@pytest.Fixture
def client():

    # Configurações comuns de setar:

    # Instancia no Flask para modo teste:
    app = create_app('testing')

    # Ativar TESTING (que ja vem nas config) como TRUE:
    app.config['TESTING'] = True
    
    # criar um cliente de teste (que seria um... )
    with app.test_client() as client:
        yield client # parar limpar recursos depois





@patch('app.routes.Imovel.query')
def test_listar_imoveis(mock_query, client):

    # Criar um mock de imóvel
    mock_imovel = MagicMock()
    mock_imovel.to_dict.return_value = {
        'id': 1,
        'tipo': 'casa',
        'endereco': 'Rua Teste, 123',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'valor': 500000,
    }
    
    # Configurar o mock do query para retornar nossa lista de imóveis (só uma no caso)
    mock_query.all.return_value = [mock_imovel]
    
    # Fazer a requisição GET
    response = client.get('/api/imoveis')
    data = json.loads(response.data)
    
    # Verificar se o método query.all() foi chamado
    mock_query.all.assert_called_once()
    
    # Verificações da resposta
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]['tipo'] == 'casa'
    assert data[0]['cidade'] == 'São Paulo'



    
    
        
