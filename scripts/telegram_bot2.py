import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os
from telegram.ext import ConversationHandler

# Carregar variáveis do .env
load_dotenv()
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")

# Conectar ao banco de dados
def connect_to_db():
    return sqlite3.connect("superbot.db")

# Comando /start - Registrar usuário
async def start(update: Update, context):
    user = update.effective_user
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO users (id_user, username, first_name, last_name)
    VALUES (?, ?, ?, ?)
    """, (
        user.id,
        user.username or "Desconhecido",
        user.first_name or "Sem nome",
        user.last_name or "Sem sobrenome"
    ))
    conn.commit()
    conn.close()

    await update.message.reply_text(f"Olá, {user.first_name}! Você foi registrado no sistema.")

# Responder mensagens e registrar no banco
async def echo(update: Update, context):
    text = update.message.text
    user_id = update.effective_user.id
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO message (user_id, message, type)
    VALUES (?, ?, ?)
    """, (user_id, text, 'texto'))
    conn.commit()
    conn.close()

    await update.message.reply_text(f"Você disse: {text}")

# Comando /notas - Listar notas fiscais
async def listar_notas(update: Update, context):
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT numero, valor, data_emissao, descricao
    FROM notas_fiscais
    """)
    notas = cursor.fetchall()

    if notas:
        resposta = "📑 *Notas Fiscais Registradas:*\n\n"
        for nota in notas:
            resposta += (
                f"📌 *Número:* {nota[0]}\n"
                f"💰 *Valor:* R${nota[1]:,.2f}\n"
                f"📅 *Data:* {nota[2]}\n"
                f"📝 *Descrição:* {nota[3]}\n\n"
            )
    else:
        resposta = "❌ Nenhuma nota fiscal registrada no momento."

    conn.close()
    await update.message.reply_text(resposta, parse_mode="Markdown")

# Estados do ConversationHandler
ESPERANDO_NUMERO, ESPERANDO_VALOR, ESPERANDO_DATA, ESPERANDO_DESCRICAO = range(4)

# Iniciar o registro de nota fiscal
async def iniciar_addnota(update: Update, context):
    await update.message.reply_text("Por favor, envie o número da nota fiscal:")
    return ESPERANDO_NUMERO

# Receber o número da nota
async def receber_numero(update: Update, context):
    context.user_data["numero"] = update.message.text
    await update.message.reply_text("Qual o valor da nota fiscal? (Exemplo: 1000.50)")
    return ESPERANDO_VALOR

# Receber o valor da nota
async def receber_valor(update: Update, context):
    try:
        context.user_data["valor"] = float(update.message.text.replace(",", "."))
        await update.message.reply_text("Qual a data de emissão? (Formato: AAAA-MM-DD)")
        return ESPERANDO_DATA
    except ValueError:
        await update.message.reply_text("Valor inválido. Por favor, insira novamente:")
        return ESPERANDO_VALOR

# Receber a data de emissão
async def receber_data(update: Update, context):
    context.user_data["data_emissao"] = update.message.text
    await update.message.reply_text("Por favor, insira uma descrição para a nota fiscal:")
    return ESPERANDO_DESCRICAO

# Receber a descrição e salvar no banco
async def salvar_nota(update: Update, context):
    context.user_data["descricao"] = update.message.text

    # Conectar ao banco e salvar os dados
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO notas_fiscais (numero, valor, data_emissao, descricao, obra_id, fornecedor_id, pedido_compra_id, tipo, data_vencimento)
        VALUES (?, ?, ?, ?, NULL, NULL, NULL, 'entrada', DATE('now', '+30 days'))
        """, (
            context.user_data["numero"],
            context.user_data["valor"],
            context.user_data["data_emissao"],
            context.user_data["descricao"]
        ))
        conn.commit()
        await update.message.reply_text("✅ Nota fiscal registrada com sucesso!")
    except Exception as e:
        await update.message.reply_text(f"❌ Ocorreu um erro ao registrar a nota fiscal: {e}")
    finally:
        conn.close()

    return ConversationHandler.END

# Cancelar o registro
async def cancelar(update: Update, context):
    await update.message.reply_text("🚫 Registro de nota fiscal cancelado.")
    return ConversationHandler.END

# Adicionar ConversationHandler para o comando /addnota
addnota_handler = ConversationHandler(
    entry_points=[CommandHandler("addnota", iniciar_addnota)],
    states={
        ESPERANDO_NUMERO: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_numero)],
        ESPERANDO_VALOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_valor)],
        ESPERANDO_DATA: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_data)],
        ESPERANDO_DESCRICAO: [MessageHandler(filters.TEXT & ~filters.COMMAND, salvar_nota)],
    },
    fallbacks=[CommandHandler("cancelar", cancelar)],
)

# Configuração do bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_API_KEY).build()

    # Handlers para comandos e mensagens
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("notas", listar_notas))
    # Adicionando o handler para /addnota
    app.add_handler(addnota_handler)

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    # Iniciar o bot
    print("🤖 Bot está rodando...")
    app.run_polling()
