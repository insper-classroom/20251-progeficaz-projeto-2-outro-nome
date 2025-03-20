import pytest
from app import create_app
from app.extensions import db
from app.models.imovel import Imovel

@pytest.fixture
def app():
    """Criar instância da aplicação para testes."""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Criar cliente de teste."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Criar runner para comandos CLI."""
    return app.test_cli_runner()

@pytest.fixture
def imovel_teste():
    """Dados de um imóvel para testes."""
    return {
        'tipo': 'casa',
        'logradouro': 'Rua de Teste',
        'tipo_logradouro': 'Rua',
        'numero': '123',
        'complemento': 'Apto 101',
        'bairro': 'Centro',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'cep': '01001-000',
        'valor': 500000.00
    }

@pytest.fixture
def imovel_teste2():
    """Dados de um segundo imóvel para testes."""
    return {
        'tipo': 'apartamento',
        'logradouro': 'Avenida de Teste',
        'tipo_logradouro': 'Avenida',
        'numero': '456',
        'complemento': 'Bloco B',
        'bairro': 'Jardins',
        'cidade': 'Rio de Janeiro',
        'estado': 'RJ',
        'cep': '22000-000',
        'valor': 750000.00
    }

@pytest.fixture
def imovel_db(app, imovel_teste):
    """Criar um imóvel no banco de dados para testes e retornar seu ID."""
    with app.app_context():
        imovel = Imovel(**imovel_teste)
        db.session.add(imovel)
        db.session.commit()
        imovel_id = imovel.id
        return imovel_id
