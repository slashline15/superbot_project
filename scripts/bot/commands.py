from telegram import Update
from .database import connect_to_db

# Comando /start
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

# Comando /notas
async def listar_notas(update: Update, context):
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT numero, valor, data_emissao, descricao
    FROM notas_fiscais
    """)
    notas = cursor.fetchall()

    resposta = "📑 *Notas Fiscais Registradas:*\n\n" if notas else "❌ Nenhuma nota fiscal registrada no momento."
    for nota in notas:
        resposta += (
            f"📌 *Número:* {nota[0]}\n"
            f"💰 *Valor:* R${nota[1]:,.2f}\n"
            f"📅 *Data:* {nota[2]}\n"
            f"📝 *Descrição:* {nota[3]}\n\n"
        )

    conn.close()
    await update.message.reply_text(resposta, parse_mode="Markdown")
