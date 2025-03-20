import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Imprimir o valor atual da DATABASE_URL
print(f"Valor atual de DATABASE_URL: {os.environ.get('DATABASE_URL')}")

# Definir nova URL para SQLite
new_url = "sqlite:///imobiliaria.db"

# Atualizar o arquivo .env
with open('.env', 'r') as file:
    lines = file.readlines()

with open('.env', 'w') as file:
    for line in lines:
        if line.startswith('DATABASE_URL='):
            file.write(f'DATABASE_URL={new_url}\n')
        else:
            file.write(line)

print(f"Arquivo .env atualizado. Nova URL: {new_url}") 