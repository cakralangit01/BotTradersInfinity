from telegram.ext import Application, MessageHandler
from telegram.ext.filters import PHOTO, VIDEO, TEXT, COMMAND, Document
from datetime import datetime, time
import asyncio
import pytz

# Masukkan token API dari BotFather
TOKEN = "TOKEN_KAMU"
CHANNEL_ID = "@Traders_Infinity"  # Ganti dengan username channel kamu

# Tentukan zona waktu WIB
WIB = pytz.timezone("Asia/Jakarta")

# Fungsi untuk mengecek jam operasional
async def check_operating_hours(application):
    while True:
        now = datetime.now(WIB).time()  # Dapatkan waktu saat ini dalam zona WIB
        start_time = time(9, 0)  # 09:00 WIB
        end_time = time(0, 0)  # 24:00 WIB (tengah malam)

        # Jika di luar jam operasional, bot akan berhenti
        if not (start_time <= now or now < end_time):
            print("Di luar jam operasional (WIB). Bot akan berhenti.")
            await application.shutdown()  # Shutdown aplikasi bot
            return  # Keluar dari fungsi
        await asyncio.sleep(60)  # Cek setiap 60 detik

# Fungsi untuk meneruskan pesan teks ke channel
async def forward_text(update, context):
    try:
        message = update.message.text
        await context.bot.send_message(chat_id=CHANNEL_ID, text=message)
        print(f"Teks diteruskan ke channel: {message}")
    except Exception as e:
        print(f"Error mengirim teks: {e}")

# Fungsi untuk meneruskan media (gambar, video, dokumen)
async def forward_media(update, context):
    try:
        if update.message.photo:
            photo_file = update.message.photo[-1].file_id
            caption = update.message.caption or ""
            await context.bot.send_photo(chat_id=CHANNEL_ID, photo=photo_file, caption=caption)
            print("Gambar diteruskan ke channel.")
        elif update.message.video:
            video_file = update.message.video.file_id
            caption = update.message.caption or ""
            await context.bot.send_video(chat_id=CHANNEL_ID, video=video_file, caption=caption)
            print("Video diteruskan ke channel.")
        elif update.message.document:
            document_file = update.message.document.file_id
            caption = update.message.caption or ""
            await context.bot.send_document(chat_id=CHANNEL_ID, document=document_file, caption=caption)
            print("Dokumen diteruskan ke channel.")
    except Exception as e:
        print(f"Error mengirim media: {e}")

# Fungsi utama untuk menjalankan bot
async def run_bot():
    application = Application.builder().token(TOKEN).build()

    # Tambahkan handler untuk teks
    application.add_handler(MessageHandler(TEXT & ~COMMAND, forward_text))

    # Tambahkan handler untuk media
    media_filter = PHOTO | VIDEO | Document.ALL
    application.add_handler(MessageHandler(media_filter, forward_media))

    # Jalankan pengecekan jam operasional secara paralel
    asyncio.create_task(check_operating_hours(application))

    print("Bot sedang berjalan...")
    await application.run_polling()

# Fungsi utama untuk inisialisasi
async def main():
    await run_bot()

if __name__ == "__main__":
    asyncio.run(main())
