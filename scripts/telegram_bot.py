from telegram import Update
from database import connect
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")

# Comando inicial do bot
async def start(update: Update, context):
    user = update.effective_user
    conn = connect()
    cursor = conn.cursor()
    
    # Registrar usuáriono comando start
    cursor.execute("""
    INSERT OR IGNORE INTO usuarios (id, username, first_name, last_name)
    VALUES (?, ?, ?, ?)
    """, (user.id, user.username, user.first_name, user.last_name))

    conn.commit()
    
    await update.message.reply_text(f"Olá, {user.first_name}! Você foi registrado no sistema.")

async def echo(update: Update, context):
    user = update.effective_user
    conn = connect()
    cursor = conn.cursor()
    
    # Registrar usuário, se não existir
    cursor.execute("""
    INSERT OR IGNORE INTO usuarios (id, username, first_name, last_name)
    VALUES (?, ?, ?, ?)
    """, (
        user.id,
        user.username or "Desconhecido",
        user.first_name or "Sem nome",
        user.last_name or "Sem sobrenome"
    ))

    conn.commit()

    await update.message.reply_text(f"Olá, {user.first_name}! Você foi registrado no sistema.")

# Responder mensagens
async def echo(update: Update, context):
    text = update.message.text
    user_id = update.effective_user.id
    conn = connect()
    cursor = conn.cursor()

    # Salvar mensagem no banco de dados
    cursor.execute("""
    INSERT INTO mensagens (user_id, text) VALUES (?, ?)
    """, (user_id, text))
    conn.commit()
    conn.close()

    await update.message.reply_text(f"Você disse: {text}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_API_KEY).build()

    # Handlers de comandos e mensagens
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Iniciar o bot
    print("Bot está rodando...")
    app.run_polling()
