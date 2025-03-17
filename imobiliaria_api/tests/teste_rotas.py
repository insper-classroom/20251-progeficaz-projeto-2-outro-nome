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

@patch('app.routes.Imovel.query')
@patch('app.routes.db.session')
def test_atualizar_imovel(mock_session, mock_query, client):
    # Criar mock do imóvel
    mock_imovel = MagicMock()
    mock_imovel.to_dict.return_value = {
        'id': 1,
        'logradouro': 'Rua Velha',
        'tipo_logradouro': 'Rua',
        'bairro': 'Savassi',  # Já com o valor atualizado
        'cidade': 'Belo Horizonte',
        'cep': '30000-000',
        'tipo': 'casa',
        'valor': 500000.0,  # Já com o valor atualizado
        'data_aquisicao': '2023-01-20'
    }
    
    # Configurar mock para simular o imóvel encontrado
    mock_query.get_or_404.return_value = mock_imovel
    
    # Dados para atualização
    dados_atualizados = {
        'valor': 500000.0,
        'bairro': 'Savassi'
    }
    
    # Fazer a requisição PUT
    response = client.put(
        '/api/imoveis/1',
        data=json.dumps(dados_atualizados),
        content_type='application/json'
    )
    data = json.loads(response.data)
    
    # Verificar se a função commit foi chamada
    mock_session.commit.assert_called_once()
    
    # Verificações da resposta
    assert response.status_code == 200
    assert data['imovel']['bairro'] == 'Savassi'
    assert data['imovel']['valor'] == 500000.0

@patch('app.routes.Imovel.query')
@patch('app.routes.db.session')
def test_deletar_imovel(mock_session, mock_query, client):
    # Criar mock do imóvel
    mock_imovel = MagicMock()
    
    # Configurar mock para simular o imóvel encontrado
    mock_query.get_or_404.return_value = mock_imovel
    
    # Fazer a requisição DELETE
    response = client.delete('/api/imoveis/1')
    
    # Verificar se o imóvel foi deletado e o commit foi chamado
    mock_session.delete.assert_called_once_with(mock_imovel)
    mock_session.commit.assert_called_once()
    
    # Verificações da resposta
    assert response.status_code == 204

    
    
        
