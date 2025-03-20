# API RESTful - Imobiliária

API RESTful para gerenciamento de imóveis, desenvolvida com Flask e MySQL (Aiven), seguindo os princípios de TDD e atingindo o nível 3 de maturidade de Richardson.

## Índice

- [Funcionalidades](#funcionalidades)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Endpoints da API](#endpoints-da-api)
- [Testes](#testes)
- [Deploy na AWS](#deploy-na-aws)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Nível 3 de Maturidade de Richardson](#nível-3-de-maturidade-de-richardson)

## Funcionalidades

- Lista todos os imóveis
- Obtém detalhes de um imóvel específico
- Cria novo imóvel
- Atualiza imóvel existente
- Remove imóvel
- Filtra imóveis por tipo
- Filtra imóveis por cidade
- HATEOAS (Hypermedia as the Engine of Application State)
- Códigos HTTP apropriados
- Testes automatizados

## Requisitos

- Python 3.9+
- MySQL (hospedado no Aiven)
- Demais dependências listadas em `requirements.txt`

## Instalação

1. Clone o repositório:
```
git clone https://github.com/seu-usuario/imobiliaria-api.git
cd imobiliaria-api
```

2. Crie e ative um ambiente virtual:
```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```
pip install -r requirements.txt
```

## Configuração

1. Copie o arquivo `.env.example` para `.env`:
```
cp .env.example .env
```

2. Edite o arquivo `.env` com suas configurações:
```
# Configurações do Flask
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=sua-chave-secreta-aqui

# Configurações do Banco de Dados
DATABASE_URL=mysql://usuario:senha@host:porta/nome_banco
```

3. Configure o banco de dados e crie as tabelas:
```
flask create-tables
```

## Uso

Para iniciar o servidor em modo de desenvolvimento:
```
flask run
```

Para produção, recomenda-se usar o Gunicorn:
```
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | /api/imoveis | Lista todos os imóveis |
| GET | /api/imoveis/:id | Obtém um imóvel específico pelo ID |
| POST | /api/imoveis | Cria um novo imóvel |
| PUT | /api/imoveis/:id | Atualiza um imóvel existente |
| DELETE | /api/imoveis/:id | Remove um imóvel |
| GET | /api/imoveis/tipo/:tipo | Lista imóveis por tipo |
| GET | /api/imoveis/cidade/:cidade | Lista imóveis por cidade |

## Testes

Execute os testes com:
```
pytest
```

Para gerar relatório de cobertura:
```
pytest --cov=app tests/
```

## Deploy na AWS

A API está hospedada em uma instância EC2 da AWS e pode ser acessada em:
[http://ec2-XX-XX-XX-XX.us-east-2.compute.amazonaws.com](http://ec2-XX-XX-XX-XX.us-east-2.compute.amazonaws.com)

### Passos para Deploy

1. Crie uma instância EC2
2. Configure o grupo de segurança para permitir tráfego HTTP/HTTPS
3. Conecte-se via SSH
4. Clone o repositório
5. Configure o ambiente
6. Configure o Nginx e o Gunicorn
7. Configure o Supervisor para manter o aplicativo em execução

## Estrutura do Projeto

```
imobiliaria_api/
│
├── app/                          # Pacote principal da aplicação
│   ├── __init__.py               # Configuração e inicialização da aplicação
│   ├── config.py                 # Configurações da aplicação
│   ├── extensions.py             # Extensões Flask (SQLAlchemy, Migrate, etc.)
│   │
│   ├── api/                      # Módulo para API RESTful
│   │   ├── __init__.py
│   │   ├── resources/
│   │   ├── schemas/
│   │   └── utils/
│   │
│   └── models/                   # Modelos de dados
│
├── tests/                        # Testes automatizados
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   ├── integration/
│   └── functional/
│
├── .env.example                  # Exemplo de variáveis de ambiente
├── requirements.txt              # Dependências do projeto
└── run.py                        # Ponto de entrada da aplicação
```

## Nível 3 de Maturidade de Richardson

A API implementa todos os níveis do Modelo de Maturidade de Richardson:

1. **Recursos**: Utilizamos URIs para identificar recursos específicos (imóveis)
2. **Verbos HTTP**: Utilizamos os métodos HTTP apropriados para cada operação (GET, POST, PUT, DELETE)
3. **Hypermedia**: Implementamos HATEOAS, incluindo links relacionados nas respostas, permitindo a navegação pela API

Exemplo de resposta com HATEOAS:
```json
{
    "id": 1,
    "tipo": "casa",
    "logradouro": "Rua das Flores",
    "cidade": "São Paulo",
    "estado": "SP",
    "valor": 500000.0,
    "_links": {
        "self": {
            "href": "http://localhost:5000/api/imoveis/1",
            "method": "GET"
        },
        "update": {
            "href": "http://localhost:5000/api/imoveis/1",
            "method": "PUT"
        },
        "delete": {
            "href": "http://localhost:5000/api/imoveis/1",
            "method": "DELETE"
        },
        "collection": {
            "href": "http://localhost:5000/api/imoveis",
            "method": "GET"
        }
    }
}
```
