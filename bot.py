import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Log ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token'ı
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

# /start komutu
def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    update.message.reply_text(
        f'Merhaba {user.first_name}! 👋\n'
        f'Ben Render.com üzerinde çalışan bir botum!\n\n'
        f'🤖 **Kullanılabilir Komutlar:**\n'
        f'/start - Botu başlat\n'
        f'/help - Yardım\n'
        f'/echo [mesaj] - Mesajını tekrar ederim\n'
        f'/info - Bot bilgileri'
    )

# /help komutu
def help_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        '🤖 **Kullanılabilir Komutlar:**\n'
        '/start - Botu başlat\n'
        '/help - Yardım mesajı\n'
        '/echo [mesaj] - Yazdığını tekrar eder\n'
        '/info - Bot bilgileri\n\n'
        'Ayrıca normal mesajlarını da cevaplarım!'
    )

# /echo komutu
def echo(update: Update, context: CallbackContext):
    if context.args:
        text = ' '.join(context.args)
        update.message.reply_text(f'🔁 Sen: {text}')
    else:
        update.message.reply_text('ℹ️ Kullanım: /echo [mesajınız]')

# /info komutu
def info(update: Update, context: CallbackContext):
    user = update.message.from_user
    update.message.reply_text(
        f'📊 **Bot Bilgileri:**\n'
        f'• Kullanıcı ID: {user.id}\n'
        f'• Ad: {user.first_name}\n'
        f'• Kullanıcı Adı: @{user.username if user.username else "yok"}\n'
        f'• Host: Render.com\n'
        f'• Durum: 🟢 Çalışıyor'
    )

# Normal mesajlara cevap
def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.lower()
    
    if 'merhaba' in text or 'selam' in text:
        update.message.reply_text('Merhaba! Nasılsın? 😊')
    elif 'teşekkür' in text or 'sağol' in text:
        update.message.reply_text('Rica ederim! 🤗')
    elif 'görüşürüz' in text or 'bye' in text:
        update.message.reply_text('Görüşürüz! 👋')
    else:
        update.message.reply_text(f'🤖 "{update.message.text}" mesajını aldım!')

# Hata yönetimi
def error(update: Update, context: CallbackContext):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    try:
        # Updater oluştur
        updater = Updater(TOKEN)
        
        # Dispatcher'ı al
        dp = updater.dispatcher

        # Handler'ları ekle
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help_command))
        dp.add_handler(CommandHandler("echo", echo))
        dp.add_handler(CommandHandler("info", info))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
        
        # Hata handler
        dp.add_error_handler(error)

        # Botu başlat
        print("🤖 Bot polling başlatılıyor...")
        logger.info("Bot başlatıldı!")
        
        # Polling başlat
        updater.start_polling()
        
        # Botu çalışır durumda tut
        updater.idle()
        
    except Exception as e:
        logger.error(f"Bot başlatılamadı: {e}")

if __name__ == '__main__':
    main()
