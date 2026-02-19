TOKEN = "8549561316:AAGoQ84co7UH6EXqPCaGoyntL_sVbYrAYDs"
CANAL_ID = "-1003845355658"

# ZONA FIJA
ZONA_PERMITIDA = "lanzarote"
import time

# Guardamos reportes con tiempo
reportes_guardados = {}

# Tiempo de bloqueo (30 minutos)
TIEMPO_BLOQUEO = 1800
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler
)

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if len(args) < 4:
        await update.message.reply_text(
            "❌ Formato:\n"
            "/report Pokémon IV PC LAT,LON\n"
            "Ejemplo:\n"
            "/report Dragonite 100 3792 28.9630,-13.5400"
        )
        return

    pokemon = args[0]
    iv = args[1]
    pc = args[2]
    coords = args[3]

    usuario = update.effective_user.first_name
    maps_url = f"https://maps.google.com/?q={coords}"

    mensaje = (
        f"💯 {pokemon} {iv} IV\n"
        f"⚡ PC: {pc}\n"
        f"📍 Ubicación: Lanzarote\n"
        f"🗺 Google Maps:\n{maps_url}\n\n"
        f"Reportado por: {usuario}"
    )

    teclado = [
        [
            InlineKeyboardButton("⭐ Shiny", callback_data="shiny"),
            InlineKeyboardButton("🚶 Voy", callback_data="voy")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(teclado)

    await context.bot.send_message(
        chat_id=CANAL_ID,
        text=mensaje,
        reply_markup=reply_markup
    )
async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "shiny":
        await query.message.reply_text("⭐ ¡Alguien lo marcó como shiny!")
    elif query.data == "voy":
        await query.message.reply_text("🚶 ¡Alguien va en camino!")
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("report", report)) 
app.add_handler(CallbackQueryHandler(botones))

print("🟢 Radar MeGaHunter Lanzarote ACTIVO")
app.run_polling(
        poll_interval=2.0,    
        timeout=30,           
        read_latency=30,       
        bootstrap_retries=-1
)

