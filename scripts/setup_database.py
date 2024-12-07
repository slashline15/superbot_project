import sqlite3

# Conectar ao banco
conn = sqlite3.connect("superbot.db")
cursor = conn.cursor()

# Lista de comandos SQL
sql_commands = [
    """
    CREATE TABLE users (
        id_user INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_message TIMESTAMP,
        FOREIGN KEY(last_message) REFERENCES message(timestamp) ON DELETE SET NULL
    )
    """,
    """
    CREATE TABLE message (
        id_message INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        message TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        type TEXT CHECK (type IN ('texto', 'imagem', 'pdf', 'audio')) NOT NULL,
        file_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id_user) ON DELETE CASCADE,
        FOREIGN KEY(file_id) REFERENCES files(id) ON DELETE SET NULL
    )
    """,
    """
    CREATE TABLE files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        url TEXT NOT NULL UNIQUE
    )
    """,
    """
    CREATE TABLE obra (
        id_obra INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        responsavel_id INTEGER NOT NULL,
        FOREIGN KEY(responsavel_id) REFERENCES users(id_user) ON DELETE SET NULL
    )
    """,
    """
    CREATE TABLE tabela_insumos (
        id_insumo INTEGER PRIMARY KEY AUTOINCREMENT,
        obra_id INTEGER NOT NULL,
        cod_insumo TEXT NOT NULL,
        descricao TEXT NOT NULL,
        categoria TEXT,
        valor_total NUMERIC(10, 2),
        FOREIGN KEY(obra_id) REFERENCES obra(id_obra) ON DELETE CASCADE,
        CONSTRAINT insumo_unico_por_obra UNIQUE (obra_id, cod_insumo)
    )
    """,
    """
    CREATE TABLE meta (
        id_meta INTEGER PRIMARY KEY AUTOINCREMENT,
        obra_id INTEGER NOT NULL,
        insumo_id INTEGER NOT NULL,
        descricao TEXT NOT NULL,
        qtd NUMERIC(10, 3) NOT NULL,
        unitario NUMERIC(10, 2) NOT NULL,
        total NUMERIC(10, 2),
        FOREIGN KEY(obra_id) REFERENCES obra(id_obra) ON DELETE CASCADE,
        FOREIGN KEY(insumo_id) REFERENCES tabela_insumos(id_insumo) ON DELETE CASCADE
    )
    """,
    """
    CREATE TABLE pedidos_de_compra (
        id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
        obra_id INTEGER NOT NULL,
        data_emissao DATE NOT NULL,
        valor NUMERIC(10, 2) NOT NULL,
        insumo_id INTEGER NOT NULL,
        fornecedor_id INTEGER NOT NULL,
        file_id INTEGER,
        descricao TEXT NOT NULL,
        FOREIGN KEY(obra_id) REFERENCES obra(id_obra) ON DELETE CASCADE,
        FOREIGN KEY(insumo_id) REFERENCES tabela_insumos(id_insumo) ON DELETE CASCADE,
        FOREIGN KEY(fornecedor_id) REFERENCES fornecedores(id) ON DELETE CASCADE,
        FOREIGN KEY(file_id) REFERENCES files(id) ON DELETE SET NULL
    )
    """,
    """
    CREATE TABLE pedidos_filhotes (
        id_pedido_filho INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_pai_id INTEGER NOT NULL,
        obra_id INTEGER NOT NULL,
        descricao TEXT NOT NULL,
        valor NUMERIC(10, 2) NOT NULL,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(pedido_pai_id) REFERENCES pedidos_de_compra(id_pedido) ON DELETE CASCADE,
        FOREIGN KEY(obra_id) REFERENCES obra(id_obra) ON DELETE CASCADE
    )
    """,
    """
    CREATE TABLE notas_fiscais (
        id_nota INTEGER PRIMARY KEY AUTOINCREMENT,
        obra_id INTEGER NOT NULL,
        pedido_compra_id INTEGER NOT NULL,
        fornecedor_id INTEGER NOT NULL,
        tipo TEXT NOT NULL CHECK (tipo IN ('entrada', 'saida', 'medicao', 'outros')),
        numero TEXT NOT NULL UNIQUE,
        valor NUMERIC(10, 2) NOT NULL,
        data_emissao DATE NOT NULL,
        data_vencimento DATE NOT NULL,
        descricao TEXT,
        file_id INTEGER,
        FOREIGN KEY(obra_id) REFERENCES obra(id_obra) ON DELETE CASCADE,
        FOREIGN KEY(pedido_compra_id) REFERENCES pedidos_de_compra(id_pedido) ON DELETE CASCADE,
        FOREIGN KEY(fornecedor_id) REFERENCES fornecedores(id) ON DELETE CASCADE,
        FOREIGN KEY(file_id) REFERENCES files(id) ON DELETE SET NULL
    )
    """,
    """
    CREATE TABLE fornecedores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        cnpj TEXT NOT NULL UNIQUE
    )
    """,
    """
    CREATE TABLE prestadores_servico (
        id_prestador INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cnpj TEXT NOT NULL UNIQUE,
        contato TEXT
    )
    """,
    """
    CREATE TABLE medicao (
        id_medicao INTEGER PRIMARY KEY AUTOINCREMENT,
        prestador_id INTEGER NOT NULL,
        obra_id INTEGER NOT NULL,
        descricao TEXT NOT NULL,
        valor NUMERIC(10, 2) NOT NULL,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(prestador_id) REFERENCES prestadores_servico(id_prestador) ON DELETE CASCADE,
        FOREIGN KEY(obra_id) REFERENCES obra(id_obra) ON DELETE CASCADE
    )
    """
]

# Executar os comandos
for command in sql_commands:
    cursor.execute(command)

conn.commit()
conn.close()
print("Tabelas criadas com sucesso!")
