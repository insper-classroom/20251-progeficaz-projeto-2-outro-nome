from marshmallow import Schema, fields, validate, post_dump
from ...extensions import ma
from ...models.imovel import Imovel

class ImovelSchema(ma.SQLAlchemyAutoSchema):
    """Schema para serialização/deserialização de imóveis."""
    
    class Meta:
        model = Imovel
        load_instance = True
    
    # Campos explicitamente definidos para adicionar validação
    id = fields.Integer(dump_only=True)
    tipo = fields.String(validate=validate.Length(max=50))
    logradouro = fields.String(required=True, validate=validate.Length(min=3, max=100))
    tipo_logradouro = fields.String(validate=validate.Length(max=20))
    bairro = fields.String(validate=validate.Length(max=50))
    cidade = fields.String(required=True, validate=validate.Length(min=2, max=50))
    cep = fields.String(validate=validate.Length(max=10))
    valor = fields.Float(validate=validate.Range(min=0))
    data_aquisicao = fields.String(validate=validate.Length(max=10))
    
    # Campo para links HATEOAS
    _links = fields.Dict(dump_only=True) 