import os
from telegram import Update
from .database import connect_to_db

# Comando1 /start - Registrar usuário
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
