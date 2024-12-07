from .database import connect_to_db
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, filters
from telegram import Update

# Estados do ConversationHandler
ESPERANDO_OBRA, ESPERANDO_NUMERO, ESPERANDO_VALOR, ESPERANDO_DATA, ESPERANDO_DESCRICAO = range(5)

# Iniciar o registro de nota fiscal
async def iniciar_addnota(update: Update, context):
    await update.message.reply_text("Por favor, informe o ID da obra associada à nota fiscal:")
    return ESPERANDO_OBRA

# Receber o ID da obra
async def receber_obra(update: Update, context):
    try:
        context.user_data["obra_id"] = int(update.message.text)
        await update.message.reply_text("Agora, envie o número da nota fiscal:")
        return ESPERANDO_NUMERO
    except ValueError:
        await update.message.reply_text("ID da obra inválido. Por favor, insira um número:")
        return ESPERANDO_OBRA

# Salvar a nota no banco
async def salvar_nota(update: Update, context):
    # Restante do código para salvar a nota
    pass

# Cancelar o registro
async def cancelar(update: Update, context):
    await update.message.reply_text("🚫 Registro de nota fiscal cancelado.")
    return ConversationHandler.END

# Handler para o comando /addnota
addnota_handler = ConversationHandler(
    entry_points=[CommandHandler("addnota", iniciar_addnota)],
    states={
        ESPERANDO_OBRA: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_obra)],
        # Outras etapas...
    },
    fallbacks=[CommandHandler("cancelar", cancelar)],
)

