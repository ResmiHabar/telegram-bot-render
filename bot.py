import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Log ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token'ı - Render environment variable'dan al
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

# /start komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text(
        f'Merhaba {user.first_name}! 👋\n'
        f'Ben Render.com üzerinde çalışan bir botum!\n\n'
        f'🎉 **Bot başarıyla çalışıyor!**\n\n'
        f'🤖 Kullanılabilir Komutlar:\n'
        f'/start - Botu başlat\n'
        f'/help - Yardım\n'
        f'/info - Bot bilgileri'
    )

# /help komutu
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '🤖 **Kullanılabilir Komutlar:**\n'
        '/start - Botu başlat\n'
        '/help - Yardım mesajı\n'
        '/info - Bot bilgileri\n\n'
        'Ben basit bir Telegram botuyum!'
    )

# /info komutu
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text(
        f'📊 **Bot Bilgileri:**\n'
        f'• Kullanıcı ID: {user.id}\n'
        f'• Ad: {user.first_name}\n'
        f'• Kullanıcı Adı: @{user.username if user.username else "yok"}\n'
        f'• Host: Render.com\n'
        f'• Durum: 🟢 Çalışıyor'
    )

# Normal mesajlara cevap
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    
    if 'merhaba' in text or 'selam' in text:
        await update.message.reply_text('Merhaba! Nasılsın? 😊')
    elif 'teşekkür' in text or 'sağol' in text:
        await update.message.reply_text('Rica ederim! 🤗')
    elif 'görüşürüz' in text or 'bye' in text:
        await update.message.reply_text('Görüşürüz! 👋')
    else:
        await update.message.reply_text('Mesajını aldım! 🎯')

# Hata yönetimi
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f'Exception while handling an update: {context.error}')

def main():
    try:
        # Bot uygulamasını oluştur
        application = Application.builder().token(TOKEN).build()

        # Handler'ları ekle
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("info", info))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Hata handler
        application.add_error_handler(error_handler)

        # Botu başlat
        logger.info("🤖 Bot başlatılıyor...")
        print("Bot polling başlatıldı!")
        
        # Polling başlat
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Bot başlatılamadı: {e}")
        print(f"Bot başlatılamadı: {e}")

if __name__ == '__main__':
    main()
