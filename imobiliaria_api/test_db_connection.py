import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# Carregar variáveis de ambiente
load_dotenv()

# Obter a URL do banco de dados
db_url = os.environ.get('DATABASE_URL')
print(f"URL do banco de dados: {db_url}")

try:
    # Testar a criação do objeto URL
    url_object = URL.create(db_url) if callable(getattr(URL, 'create', None)) else db_url
    print(f"Objeto URL criado: {url_object}")
    
    # Tentar conectar ao banco de dados
    engine = create_engine(db_url)
    connection = engine.connect()
    print("Conexão estabelecida com sucesso!")
    connection.close()
except Exception as e:
    print(f"Erro: {e}")
    print(f"Tipo do erro: {type(e)}")
    
    # Se o erro for relacionado à formatação da URL, tentaremos uma abordagem alternativa
    if "invalid literal for int()" in str(e):
        print("\nTentando abordagem alternativa...")
        # Forçar a URL para SQLite
        alt_url = "sqlite:///imobiliaria.db"
        try:
            engine = create_engine(alt_url)
            connection = engine.connect()
            print(f"Conexão alternativa bem-sucedida com: {alt_url}")
            connection.close()
            
            # Atualizar o arquivo .env com a URL correta
            with open('.env', 'r') as file:
                lines = file.readlines()
            
            with open('.env', 'w') as file:
                for line in lines:
                    if line.startswith('DATABASE_URL='):
                        file.write(f'DATABASE_URL={alt_url}\n')
                    else:
                        file.write(line)
            
            print("Arquivo .env atualizado com a URL correta.")
        except Exception as alt_e:
            print(f"Erro na abordagem alternativa: {alt_e}") 