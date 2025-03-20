from datetime import datetime
from ..extensions import db

class Imovel(db.Model):
    """Modelo para representar um imóvel no banco de dados."""
    __tablename__ = 'imoveis'
    
    id = db.Column(db.Integer, primary_key=True)
    logradouro = db.Column(db.String(100), nullable=False)
    tipo_logradouro = db.Column(db.String(20))
    bairro = db.Column(db.String(50))
    cidade = db.Column(db.String(50), nullable=False)
    cep = db.Column(db.String(10))
    tipo = db.Column(db.String(50))
    valor = db.Column(db.Float)
    data_aquisicao = db.Column(db.String(10))
    
    def __init__(self, **kwargs):
        """Inicializa o modelo com valores padrão para campos não fornecidos."""
        super(Imovel, self).__init__(**kwargs)
    
    def __repr__(self):
        return f'<Imovel {self.id}: {self.tipo} em {self.cidade}>' 