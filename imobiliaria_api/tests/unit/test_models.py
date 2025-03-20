import pytest
from app.models.imovel import Imovel
from datetime import datetime

def test_modelo_imovel_instancia():
    """Teste se o modelo de Imovel pode ser instanciado corretamente."""
    imovel = Imovel(
        tipo='casa',
        logradouro='Rua de Teste',
        tipo_logradouro='Rua',
        numero='123',
        complemento='Apto 101',
        bairro='Centro',
        cidade='São Paulo',
        estado='SP',
        cep='01001-000',
        valor=500000.00
    )
    
    assert imovel.tipo == 'casa'
    assert imovel.logradouro == 'Rua de Teste'
    assert imovel.cidade == 'São Paulo'
    assert imovel.estado == 'SP'
    assert imovel.valor == 500000.00
    assert imovel.id is None  # ID ainda não atribuído, pois não foi salvo no banco
    
def test_modelo_imovel_repr():
    """Teste da representação string do modelo."""
    imovel = Imovel(id=1, tipo='casa', cidade='São Paulo')
    
    assert repr(imovel) == '<Imovel 1: casa em São Paulo>'
    
def test_modelo_imovel_data_criacao():
    """Teste se a data de criação é gerada automaticamente."""
    imovel = Imovel(
        tipo='casa',
        logradouro='Rua de Teste',
        cidade='São Paulo',
        estado='SP',
        valor=500000.00
    )
    
    assert isinstance(imovel.data_criacao, datetime)
    assert isinstance(imovel.data_aquisicao, datetime) 