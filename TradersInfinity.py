from telegram.ext import Application, MessageHandler, filters
from datetime import datetime, time
import asyncio
import sys

# Masukkan token API dari BotFather
TOKEN = "7277874066:AAF5qxzfX3fYRVaHl6vKpPVdD9GSg1nBZlU"
CHANNEL_ID = "@Traders_Infinity"  # Ganti dengan username channel kamu

# Fungsi untuk mengecek jam operasional
async def check_operating_hours(application):
    while True:
        now = datetime.now().time()
        start_time = time(9, 0)  # 09:00
        end_time = time(0, 0)    # 00:00

        # Cek apakah di luar jam operasional
        if not (start_time <= now or now < end_time):
            print("Di luar jam operasional. Bot akan berhenti.")
            await application.shutdown()  # Shutdown aplikasi bot
            sys.exit()  # Keluar dari program
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
async def main():
    application = Application.builder().token(TOKEN).build()

    # Tambahkan handler untuk teks
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_text))

    # Tambahkan handler untuk media
    application.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO | filters.ATTACHMENT, forward_media))

    # Jalankan pengecekan jam operasional secara paralel
    asyncio.create_task(check_operating_hours(application))

    print("Bot sedang berjalan...")
    await application.run_polling()

# Eksekusi fungsi utama
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        print(f"RuntimeError: {e}")
