from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo .env
load_dotenv()

# Obter a chave do Telegram
telegram_api_key = os.getenv("TELEGRAM_API_KEY")
print(f"Chave do Telegram: {telegram_api_key}")
