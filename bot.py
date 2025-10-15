
import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Log ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token'ı
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

# /start komutu
def start(update, context):
    user = update.message.from_user
    update.message.reply_text(
        f'Merhaba {user.first_name}! 👋\n'
        f'Ben Render.com üzerinde çalışan bir botum!\n\n'
        f'🎉 **Bot başarıyla çalışıyor!**\n\n'
        f'🤖 Kullanılabilir Komutlar:\n'
        f'/start - Botu başlat\n'
        f'/help - Yardım\n'
        f'/info - Bot bilgileri'
    )

# /help komutu
def help_command(update, context):
    update.message.reply_text(
        '🤖 **Kullanılabilir Komutlar:**\n'
        '/start - Botu başlat\n'
        '/help - Yardım mesajı\n'
        '/info - Bot bilgileri\n\n'
        'Ben basit bir Telegram botuyum!'
    )

# /info komutu
def info(update, context):
    user = update.message.from_user
    username = user.username if user.username else "yok"
    update.message.reply_text(
        f'📊 **Bot Bilgileri:**\n'
        f'• Kullanıcı ID: {user.id}\n'
        f'• Ad: {user.first_name}\n'
        f'• Kullanıcı Adı: @{username}\n'
        f'• Host: Render.com\n'
        f'• Durum: 🟢 Çalışıyor'
    )

# Normal mesajlara cevap
def handle_message(update, context):
    text = update.message.text.lower()
    
    if 'merhaba' in text or 'selam' in text:
        update.message.reply_text('Merhaba! Nasılsın? 😊')
    elif 'teşekkür' in text or 'sağol' in text:
        update.message.reply_text('Rica ederim! 🤗')
    elif 'görüşürüz' in text or 'bye' in text:
        update.message.reply_text('Görüşürüz! 👋')
    else:
        update.message.reply_text('Mesajını aldım! 🎯')

# Hata yönetimi
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    try:
        # Updater oluştur
        updater = Updater(TOKEN, use_context=True)
        
        # Dispatcher'ı al
        dp = updater.dispatcher

        # Handler'ları ekle
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help_command))
        dp.add_handler(CommandHandler("info", info))
        dp.add_handler(MessageHandler(Filters.text, handle_message))
        
        # Hata handler
        dp.add_error_handler(error)

        # Botu başlat
        logger.info("🤖 Bot başlatılıyor...")
        print("Bot polling başlatıldı!")
        
        # Polling başlat
        updater.start_polling()
        
        # Botu çalışır durumda tut
        updater.idle()
        
    except Exception as e:
        logger.error(f"Bot başlatılamadı: {e}")
        print(f"Bot başlatılamadı: {e}")

if __name__ == '__main__':
    main()
    
