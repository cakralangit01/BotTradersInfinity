from telegram.ext import Application, MessageHandler, filters
from datetime import datetime
import asyncio
import sys

# Masukkan token API dari BotFather
TOKEN = "7277874066:AAF5qxzfX3fYRVaHl6vKpPVdD9GSg1nBZlU"
CHANNEL_ID = "@Traders_Infinity"  # Ganti dengan username channel kamu

# Fungsi untuk mengecek jam operasional
async def check_operating_hours(application):
    while True:
        current_time = datetime.now().time()  # Ambil waktu sekarang
        start_time = datetime.strptime("09:00", "%H:%M").time()
        end_time = datetime.strptime("00:00", "%H:%M").time()

        # Cek apakah bot di luar jam operasional
        if not (start_time <= current_time or current_time < end_time):
            print("Di luar jam operasional. Bot akan berhenti.")
            application.stop()  # Hentikan aplikasi bot
            sys.exit()  # Keluar dari program
        await asyncio.sleep(60)  # Cek setiap 60 detik

# Fungsi untuk meneruskan pesan teks ke channel
async def forward_text(update, context):
    try:
        message = update.message.text  # Ambil teks dari pesan pengguna
        await context.bot.send_message(chat_id=CHANNEL_ID, text=message)  # Kirim teks ke channel
        print(f"Teks diteruskan ke channel: {message}")
    except Exception as e:
        print(f"Error mengirim teks: {e}")

# Fungsi untuk meneruskan gambar, video, atau file ke channel
async def forward_media(update, context):
    try:
        # Jika ada foto
        if update.message.photo:
            photo_file = update.message.photo[-1].file_id  # Ambil foto resolusi tertinggi
            caption = update.message.caption or ""  # Ambil caption jika ada
            await context.bot.send_photo(chat_id=CHANNEL_ID, photo=photo_file, caption=caption)
            print("Gambar diteruskan ke channel.")
        
        # Jika ada video
        elif update.message.video:
            video_file = update.message.video.file_id
            caption = update.message.caption or ""
            await context.bot.send_video(chat_id=CHANNEL_ID, video=video_file, caption=caption)
            print("Video diteruskan ke channel.")
        
        # Jika ada file/dokumen
        elif update.message.document:
            document_file = update.message.document.file_id
            caption = update.message.caption or ""
            await context.bot.send_document(chat_id=CHANNEL_ID, document=document_file, caption=caption)
            print("Dokumen diteruskan ke channel.")
        
    except Exception as e:
        print(f"Error mengirim media: {e}")

# Fungsi utama untuk menjalankan bot
def main():
    # Inisialisasi aplikasi bot
    application = Application.builder().token(TOKEN).build()

    # Tambahkan handler untuk teks
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_text))

    # Tambahkan handler untuk media (foto, video, file)
    application.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO | filters.ATTACHMENT, forward_media))

    # Jalankan pengecekan jam operasional secara paralel
    application.create_task(check_operating_hours(application))

    # Mulai polling untuk menerima pesan
    print("Bot sedang berjalan...")
    application.run_polling()

# Eksekusi fungsi utama jika file dijalankan langsung
if __name__ == "__main__":
    main()
