import os
from app import create_app
from app.extensions import db

# Criar aplicação com a configuração apropriada
app = create_app(os.environ.get('FLASK_ENV', 'default'))

@app.cli.command("create-tables")
def create_tables():
    """Cria todas as tabelas no banco de dados."""
    db.create_all()
    print("Tabelas criadas no banco de dados!")

@app.cli.command("drop-tables")
def drop_tables():
    """Remove todas as tabelas do banco de dados."""
    db.drop_all()
    print("Tabelas removidas do banco de dados!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
