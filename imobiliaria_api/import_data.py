import os
import re
import sqlite3
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Obter o caminho do banco de dados SQLite da variável de ambiente
db_url = os.environ.get('DATABASE_URL')
if db_url and db_url.startswith('sqlite:///'):
    db_path = db_url.replace('sqlite:///', '')
else:
    db_path = 'imobiliaria.db'

# Conectar ao banco de dados SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print(f"Conectado ao banco de dados: {db_path}")

# Criar a tabela se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS imoveis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    logradouro TEXT NOT NULL,   
    tipo_logradouro TEXT,
    bairro TEXT,
    cidade TEXT NOT NULL,
    cep TEXT,
    tipo TEXT,
    valor REAL,
    data_aquisicao TEXT
)
''')

# Verificar se a tabela já contém dados
cursor.execute("SELECT COUNT(*) FROM imoveis")
count = cursor.fetchone()[0]

if count > 0:
    print(f"A tabela já contém {count} registros. Limpando tabela para nova importação...")
    cursor.execute("DELETE FROM imoveis")
    print("Tabela limpa com sucesso.")
else:
    print("A tabela está vazia. Prosseguindo com a importação...")

# Ler o arquivo SQL e extrair os comandos INSERT
try:
    with open('../imoveis.sql', 'r') as f:
        sql_content = f.read()
except FileNotFoundError:
    # Tentar abrir o arquivo na pasta atual caso não encontre no diretório pai
    with open('imoveis.sql', 'r') as f:
        sql_content = f.read()

# Utilizar expressão regular para extrair os valores dos INSERTs
pattern = r"INSERT INTO imoveis \([^)]+\) VALUES \((.+?)\);"
matches = re.findall(pattern, sql_content)

# Contador de registros importados
imported_count = 0

# Para cada conjunto de valores encontrado
for values in matches:
    # Criar o comando INSERT para SQLite
    insert_cmd = f'''
    INSERT INTO imoveis 
    (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao)
    VALUES ({values})
    '''
    
    try:
        cursor.execute(insert_cmd)
        imported_count += 1
        if imported_count % 50 == 0:
            print(f"Importados {imported_count} registros...")
    except sqlite3.Error as e:
        print(f"Erro ao importar registro: {e}")
        print(f"Comando com erro: {insert_cmd}")

# Commit das alterações
conn.commit()

# Verificar quantos registros foram importados
cursor.execute("SELECT COUNT(*) FROM imoveis")
final_count = cursor.fetchone()[0]

print(f"\nImportação concluída! {imported_count} registros importados.")
print(f"Total de registros na tabela: {final_count}")

# Fechar conexão
conn.close() 