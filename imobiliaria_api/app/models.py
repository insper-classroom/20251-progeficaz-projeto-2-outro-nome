from datetime import datetime
from ... import db

class Imovel(db.Model):
    __tablename__ = 'imoveis'
    
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)  # casa, apartamento, etc.
    logradouro = db.Column(db.String(100), nullable=False)
    tipo_logradouro = db.Column(db.String(20))  # Rua, Avenida, etc.
    numero = db.Column(db.String(10))
    complemento = db.Column(db.String(50))
    bairro = db.Column(db.String(50))
    cidade = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    cep = db.Column(db.String(10))
    valor = db.Column(db.Float, nullable=False)
    data_aquisicao = db.Column(db.Date, default=datetime.utcnow)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'tipo': self.tipo,
            'logradouro': self.logradouro,
            'tipo_logradouro': self.tipo_logradouro,
            'numero': self.numero,
            'complemento': self.complemento,
            'bairro': self.bairro,
            'cidade': self.cidade,
            'estado': self.estado,
            'cep': self.cep,
            'valor': self.valor,
            'data_aquisicao': self.data_aquisicao.strftime('%Y-%m-%d') if self.data_aquisicao else None,
            'data_criacao': self.data_criacao.strftime('%Y-%m-%d %H:%M:%S') if self.data_criacao else None
        }