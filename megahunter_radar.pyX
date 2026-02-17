XTOKEN = "8549561316:AAFsRdEnCFCROAOZ_-X4OKGPfjbk_4W4Vtk"
CANAL_ID = "@MegaHunter-Radar100IV"

# ZONA FIJA
ZONA_PERMITIDA = "lanzarote"
from telegram import Update
from telegram.ext import ContextTypes

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if len(args) < 5:
        await update.message.reply_text(
            "❌ Formato:\n"
            "/report Pokémon IV PC LAT LON\n"
            "Ejemplo:\n"
            "/report Kangaskhan 100 2217 28.9630 -13.5476"
        )
        return

    pokemon = args[0]
    iv = args[1]
    pc = args[2]
    lat = args[3]
    lon = args[4]

    usuario = update.effective_user.first_name
    coords = f"{lat},{lon}"
    maps_url = f"https://maps.google.com/?q={coords}"

    mensaje = (
        "📡 **RADAR MeGaHunter — Lanzarote**\n\n"
        f"🧬 Pokémon: **{pokemon}**\n"
        f"⭐ IV: **{iv}%**\n"
        f"⚡ PC: **{pc}**\n"
        f"📍 Coord: `{coords}`\n"
        f"🏝 Zona: **Lanzarote**\n\n"
        f"👤 Reportado por: {usuario}\n"
        "⚔️ Clan MeGaHunter"
    )

    teclado = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🗺 Abrir Maps", url=maps_url),
            InlineKeyboardButton("📍 Coordenadas", callback_data="coords")
        ]
    ])

    await context.bot.send_message(
        chat_id=CANAL_ID,
        text=mensaje,
        parse_mode="Markdown",
        reply_markup=teclado
    )

    await update.message.reply_text("✅ Reporte Lanzarote enviado")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("report", report))

print("🟢 Radar MeGaHunter Lanzarote ACTIVO")
app.run_polling()
