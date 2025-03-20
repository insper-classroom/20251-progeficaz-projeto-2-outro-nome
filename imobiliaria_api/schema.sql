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
);

-- Script adaptado para SQLite 