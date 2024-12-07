import sqlite3

# Conexão com o banco de dados
def connect_to_db():
    return sqlite3.connect("superbot.db")
