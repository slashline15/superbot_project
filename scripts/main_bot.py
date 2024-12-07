from telegram.ext import ApplicationBuilder, CommandHandler
from bot.commands import start, listar_notas
from bot.handlers import addnota_handler
from dotenv import load_dotenv
import os

# Carregar variáveis do .env
load_dotenv()
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_API_KEY).build()

    # Adicionar handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("notas", listar_notas))
    app.add_handler(addnota_handler)

    print("🤖 Bot está rodando...")
    app.run_polling()
