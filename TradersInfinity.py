from telegram.ext import Application, MessageHandler
from telegram.ext.filters import PHOTO, VIDEO, TEXT, COMMAND, DOCUMENT
from datetime import datetime, time
import pytz
import asyncio

TOKEN = "TOKEN_KAMU"
CHANNEL_ID = "@Traders_Infinity"
WIB = pytz.timezone("Asia/Jakarta")

# Fungsi cek jam operasional
async def check_operating_hours(application):
    while True:
        now = datetime.now(WIB).time()
        start_time = time(9, 0)
        end_time = time(0, 0)
        if not (start_time <= now or now < end_time):
            print("Di luar jam operasional. Bot berhenti.")
            await application.shutdown()  # Gunakan await untuk menunggu shutdown
            break  # Keluar dari loop setelah shutdown
        await asyncio.sleep(60)

# Fungsi untuk forward pesan teks
async def forward_text(update, context):
    try:
        message = update.message.text
        await context.bot.send_message(chat_id=CHANNEL_ID, text=message)
        print(f"Teks diteruskan: {message}")
    except Exception as e:
        print(f"Error kirim teks: {e}")

# Fungsi untuk forward media
async def forward_media(update, context):
    try:
        if update.message.photo:
            photo_file = update.message.photo[-1].file_id
            caption = update.message.caption or ""
            await context.bot.send_photo(chat_id=CHANNEL_ID, photo=photo_file, caption=caption)
            print("Gambar diteruskan.")
        elif update.message.video:
            video_file = update.message.video.file_id
            caption = update.message.caption or ""
            await context.bot.send_video(chat_id=CHANNEL_ID, video=video_file, caption=caption)
            print("Video diteruskan.")
        elif update.message.document:
            document_file = update.message.document.file_id
            caption = update.message.caption or ""
            await context.bot.send_document(chat_id=CHANNEL_ID, document=document_file, caption=caption)
            print("Dokumen diteruskan.")
    except Exception as e:
        print(f"Error kirim media: {e}")

# Fungsi utama
async def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(TEXT & ~COMMAND, forward_text))
    application.add_handler(MessageHandler(PHOTO | VIDEO | DOCUMENT, forward_media))
    
    # Jalankan pengecekan jam operasional di task terpisah
    asyncio.create_task(check_operating_hours(application))
    
    print("Bot sedang berjalan...")
    
    # Menjalankan bot dalam polling
    await application.run_polling()

# Fungsi utama untuk inisialisasi
async def main():
    try:
        await run_bot()  # Jangan gunakan asyncio.run() di dalam async function
    except RuntimeError as e:
        print(f"RuntimeError: {e}")

if __name__ == "__main__":
    asyncio.run(main())  # Memanggil main() menggunakan asyncio.run() untuk menjalankan semuanya
