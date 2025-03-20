from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

# Inicializar extensões
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def init_app(app):
    """Inicializa as extensões com a aplicação Flask."""
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    
    return app
