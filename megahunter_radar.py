
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler
)

TOKEN = "8549561316:AAGoQ84co7UH6EXqPCaGoyntL_sVbYrAYDs"
CANAL_ID = "-1003845355658"
ZONA_PERMITIDA = "lanzarote"

# Solo dejamos esta lista para coordenadas
reportes_recientes=[]
reportes_guardados = {}
TIEMPO_BLOQUEO = 1800 # 30 minutos en segundos

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    ahora = time.time()
    args = context.args

    # 1. Verificamos si el comando tiene los datos
    if len(args) < 4:
        await update.message.reply_text(
            "Uso: /report Nombre IV PC Coordenadas"
        )
        return

    # 2. Guardamos la coordenada
    coord = args[3]

    # 3. Filtro de duplicados
    if coord in reportes_recientes:
        await update.message.reply_text(
            "⚠️ Ese Pokémon ya fue reportado recientemente."
        )
        return

    # 4. Añadimos a la lista
    reportes_recientes.append(coord)

    # 5. Limpiamos lista si supera 20
    if len(reportes_recientes) > 20:
        reportes_recientes.pop(0)

    nombre = args[0]
    iv = args[1]
    pc = args[2]

    maps_url = f"https://www.google.com/maps?q={coord}"



    if user_id in reportes_guardados:
        tiempo_pasado = ahora - reportes_guardados[user_id]
        if tiempo_pasado < TIEMPO_BLOQUEO:
            minutos_restantes = int((TIEMPO_BLOQUEO - tiempo_pasado) / 60)
            await update.message.reply_text(
                f"⏳ ¡Cálmate Hunter! Debes esperar {minutos_restantes} minutos para otro reporte.")
            return

    args = context.args
    if len(args) < 4:
        await update.message.reply_text(
            "❌ Formato:\n/report Pokémon IV PC LAT,LON"
        )
        return

    # 2. SI PASA EL FILTRO, GUARDAMOS EL TIEMPO ACTUAL
    reportes_guardados[user_id] = ahora

    pokemon, iv, pc, coords = args[0], args[1], args[2], args[3]
    usuario = update.effective_user.first_name
    maps_url = "https://www.google.com/maps?q={coords}"

    mensaje = (
        f"💯 {pokemon} {iv} IV\n⚡ PC: {pc}\n📍 Ubicación: Lanzarote\n"
        f"🗺 Google Maps:\n{maps_url}\n\nReportado por: {usuario}"
    )

    teclado = [[
        InlineKeyboardButton("⭐ Shiny", callback_data="shiny"),
        InlineKeyboardButton("🚶 Voy", callback_data="voy")
    ]]

    await context.bot.send_message(
        chat_id=CANAL_ID,
        text=mensaje,
        reply_markup=InlineKeyboardMarkup(teclado)
    )

async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "shiny":
        await query.message.reply_text(f"⭐ ¡{update.effective_user.first_name} marcó como shiny!")
    elif query.data == "voy":
        await query.message.reply_text(f"🚶 ¡{update.effective_user.first_name} va en camino,!")
if __name__ == '__main__':
 app=ApplicationBuilder().token(TOKEN).build()
 app.add_handler(CommandHandler("report",
report))
 app.add_handler(CallbackQueryHandler(botones))
 print("🟢Radar ACTIVO")
 app.run_polling(
      poll_interval=2.0,
      timeout=30,
      allowed_updates=None,
      drop_pending_updates=True
)











