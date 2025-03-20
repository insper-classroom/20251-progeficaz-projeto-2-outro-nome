from flask import Blueprint, jsonify, request
from .models import Imovel
from ... import db

api_bp = Blueprint('api', __name__)

@api_bp.route('/imoveis', methods=['GET'])
def listar_imoveis():
    imoveis = Imovel.query.all()
    return jsonify([imovel.to_dict() for imovel in imoveis])

@api_bp.route('/imoveis/<int:id>', methods=['GET'])
def obter_imovel(id):
    imovel = Imovel.query.get_or_404(id)
    return jsonify(imovel.to_dict())

@api_bp.route('/imoveis', methods=['POST'])
def criar_imovel():
    dados = request.json
    
    # Validação básica
    campos_obrigatorios = ['tipo', 'logradouro', 'cidade', 'estado', 'valor']
    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({'erro': f'Campo obrigatório ausente: {campo}'}), 400
    
    novo_imovel = Imovel(
        tipo=dados['tipo'],
        logradouro=dados['logradouro'],
        tipo_logradouro=dados.get('tipo_logradouro'),
        numero=dados.get('numero'),
        complemento=dados.get('complemento'),
        bairro=dados.get('bairro'),
        cidade=dados['cidade'],
        estado=dados['estado'],
        cep=dados.get('cep'),
        valor=dados['valor'],
        data_aquisicao=dados.get('data_aquisicao')
    )
    
    db.session.add(novo_imovel)
    db.session.commit()
    
    return jsonify({'mensagem': 'Imóvel criado com sucesso', 'imovel': novo_imovel.to_dict()}), 201

@api_bp.route('/imoveis/<int:id>', methods=['PUT'])
def atualizar_imovel(id):
    imovel = Imovel.query.get_or_404(id)
    dados = request.json
    
    # Atualizar campos
    campos_atualizaveis = ['tipo', 'logradouro', 'tipo_logradouro', 'numero', 
                        'complemento', 'bairro', 'cidade', 'estado', 'cep', 
                        'valor', 'data_aquisicao']
    
    for campo in campos_atualizaveis:
        if campo in dados:
            setattr(imovel, campo, dados[campo])
    
    db.session.commit()
    
    return jsonify({'mensagem': 'Imóvel atualizado com sucesso', 'imovel': imovel.to_dict()})

@api_bp.route('/imoveis/<int:id>', methods=['DELETE'])
def deletar_imovel(id):
    imovel = Imovel.query.get_or_404(id)
    db.session.delete(imovel)
    db.session.commit()
    
    return '', 204

@api_bp.route('/imoveis/tipo/<string:tipo>', methods=['GET'])
def listar_imoveis_por_tipo(tipo):
    imoveis = Imovel.query.filter_by(tipo=tipo).all()
    return jsonify([imovel.to_dict() for imovel in imoveis])

@api_bp.route('/imoveis/cidade/<string:cidade>', methods=['GET'])
def listar_imoveis_por_cidade(cidade):
    imoveis = Imovel.query.filter_by(cidade=cidade).all()
    return jsonify([imovel.to_dict() for imovel in imoveis])