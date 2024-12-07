from notion_client import Client
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Autenticar no Notion
notion = Client(auth=os.getenv("NOTION_API_KEY"))

# Listar bancos de dados
def list_databases():
    databases = notion.search(filter={"property": "object", "value": "database"})
    for db in databases["results"]:
        print(f"Database: {db['title'][0]['text']['content']}, ID: {db['id']}")

if __name__ == "__main__":
    list_databases()
