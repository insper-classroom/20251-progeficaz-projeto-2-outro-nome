import json
import pytest
from app.models.imovel import Imovel

def test_listar_imoveis_vazio(client):
    """Teste para listar imóveis quando o banco de dados está vazio."""
    response = client.get('/api/imoveis')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['count'] == 0
    assert data['items'] == []
    assert '_links' in data

def test_listar_imoveis(client, imovel_db):
    """Teste para listar imóveis."""
    response = client.get('/api/imoveis')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['count'] == 1
    assert len(data['items']) == 1
    assert data['items'][0]['tipo'] == 'casa'
    assert data['items'][0]['cidade'] == 'São Paulo'
    assert '_links' in data
    assert '_links' in data['items'][0]

def test_obter_imovel(client, imovel_db):
    """Teste para obter um imóvel específico pelo ID."""
    imovel_id = imovel_db
    response = client.get(f'/api/imoveis/{imovel_id}')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['id'] == imovel_id
    assert data['tipo'] == 'casa'
    assert data['cidade'] == 'São Paulo'
    assert '_links' in data
    assert 'self' in data['_links']
    assert 'update' in data['_links']
    assert 'delete' in data['_links']

def test_obter_imovel_inexistente(client):
    """Teste para obter um imóvel com ID inexistente."""
    response = client.get('/api/imoveis/999')
    
    assert response.status_code == 404

def test_criar_imovel(client, imovel_teste):
    """Teste para criar um novo imóvel."""
    response = client.post(
        '/api/imoveis',
        data=json.dumps(imovel_teste),
        content_type='application/json'
    )
    data = json.loads(response.data)
    
    assert response.status_code == 201
    assert data['tipo'] == imovel_teste['tipo']
    assert data['logradouro'] == imovel_teste['logradouro']
    assert data['cidade'] == imovel_teste['cidade']
    assert '_links' in data

def test_criar_imovel_dados_invalidos(client):
    """Teste para criar um novo imóvel com dados inválidos."""
    imovel_invalido = {
        'tipo': 'casa',
        # logradouro é obrigatório
        'cidade': 'São Paulo',
        'estado': 'SP',
        'valor': 500000.00
    }
    
    response = client.post(
        '/api/imoveis',
        data=json.dumps(imovel_invalido),
        content_type='application/json'
    )
    
    assert response.status_code == 400

def test_atualizar_imovel(client, imovel_db):
    """Teste para atualizar um imóvel existente."""
    imovel_id = imovel_db
    atualização = {
        'valor': 600000.00,
        'complemento': 'Novo complemento'
    }
    
    response = client.put(
        f'/api/imoveis/{imovel_id}',
        data=json.dumps(atualização),
        content_type='application/json'
    )
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['valor'] == 600000.00
    assert data['complemento'] == 'Novo complemento'
    assert '_links' in data

def test_atualizar_imovel_inexistente(client):
    """Teste para atualizar um imóvel com ID inexistente."""
    atualização = {'valor': 600000.00}
    
    response = client.put(
        '/api/imoveis/999',
        data=json.dumps(atualização),
        content_type='application/json'
    )
    
    assert response.status_code == 404

def test_deletar_imovel(client, imovel_db):
    """Teste para deletar um imóvel."""
    imovel_id = imovel_db
    response = client.delete(f'/api/imoveis/{imovel_id}')
    
    assert response.status_code == 204
    
    # Verificar se o imóvel foi realmente deletado
    response = client.get(f'/api/imoveis/{imovel_id}')
    assert response.status_code == 404

def test_deletar_imovel_inexistente(client):
    """Teste para deletar um imóvel com ID inexistente."""
    response = client.delete('/api/imoveis/999')
    
    assert response.status_code == 404

def test_listar_imoveis_por_tipo(client, app, imovel_teste, imovel_teste2):
    """Teste para listar imóveis por tipo."""
    # Criar dois imóveis com tipos diferentes
    with app.app_context():
        imovel1 = Imovel(**imovel_teste)
        imovel2 = Imovel(**imovel_teste2)
        db = app.extensions['sqlalchemy'].db
        db.session.add_all([imovel1, imovel2])
        db.session.commit()
    
    # Filtrar por tipo 'casa'
    response = client.get('/api/imoveis/tipo/casa')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['count'] == 1
    assert data['items'][0]['tipo'] == 'casa'
    assert '_links' in data
    
    # Filtrar por tipo 'apartamento'
    response = client.get('/api/imoveis/tipo/apartamento')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['count'] == 1
    assert data['items'][0]['tipo'] == 'apartamento'
    assert '_links' in data

def test_listar_imoveis_por_cidade(client, app, imovel_teste, imovel_teste2):
    """Teste para listar imóveis por cidade."""
    # Criar dois imóveis com cidades diferentes
    with app.app_context():
        imovel1 = Imovel(**imovel_teste)
        imovel2 = Imovel(**imovel_teste2)
        db = app.extensions['sqlalchemy'].db
        db.session.add_all([imovel1, imovel2])
        db.session.commit()
    
    # Filtrar por cidade 'São Paulo'
    response = client.get('/api/imoveis/cidade/São Paulo')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['count'] == 1
    assert data['items'][0]['cidade'] == 'São Paulo'
    assert '_links' in data
    
    # Filtrar por cidade 'Rio de Janeiro'
    response = client.get('/api/imoveis/cidade/Rio de Janeiro')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['count'] == 1
    assert data['items'][0]['cidade'] == 'Rio de Janeiro'
    assert '_links' in data 