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

