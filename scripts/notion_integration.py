from notion_client import Client
from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo .env
load_dotenv()

# Inicializar cliente Notion
notion = Client(auth=os.getenv("NOTION_API_KEY"))

# Função para listar bancos de dados
def list_databases():
    print("Buscando bancos de dados...")
    databases = notion.search(filter={"property": "object", "value": "database"})
    for db in databases["results"]:
        title = db.get("title", [])
        title_text = title[0]["text"]["content"] if title else "Sem título"
        print(f"Database: {title_text}, ID: {db['id']}")

# Executar função
if __name__ == "__main__":
    list_databases()
