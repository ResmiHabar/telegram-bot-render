import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Log ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Bot token'ı
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

# /start komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text(
        f'Merhaba {user.first_name}! 👋\n'
        f'Ben Render.com üzerinde çalışan bir botum!\n\n'
        f'🤖 **Kullanılabilir Komutlar:**\n'
        f'/start - Botu başlat\n'
        f'/help - Yardım\n'
        f'/echo [mesaj] - Mesajını tekrar ederim\n'
        f'/info - Bot bilgileri'
    )

# /help komutu
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '🤖 **Kullanılabilir Komutlar:**\n'
        '/start - Botu başlat\n'
        '/help - Yardım mesajı\n'
        '/echo [mesaj] - Yazdığını tekrar eder\n'
        '/info - Bot bilgileri\n\n'
        'Ayrıca normal mesajlarını da cevaplarım!'
    )

# /echo komutu
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        text = ' '.join(context.args)
        await update.message.reply_text(f'🔁 Sen: {text}')
    else:
        await update.message.reply_text('ℹ️ Kullanım: /echo [mesajınız]')

# /info komutu
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text(
        f'📊 **Bot Bilgileri:**\n'
        f'• Kullanıcı ID: {user.id}\n'
        f'• Ad: {user.first_name}\n'
        f'• Kullanıcı Adı: @{user.username}\n'
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
    else:
        await update.message.reply_text(f'🤖 "{update.message.text}" mesajını aldım!')

# Hata yönetimi
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f'Update {update} caused error {context.error}')

def main():
    try:
        # Bot uygulamasını oluştur
        app = Application.builder().token(TOKEN).build()

        # Handler'ları ekle
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("echo", echo))
        app.add_handler(CommandHandler("info", info))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Hata handler
        app.add_error_handler(error)

        # Botu başlat
        print("🤖 Bot polling başlatılıyor...")
        logging.info("Bot başlatıldı!")
        app.run_polling()
        
    except Exception as e:
        logging.error(f"Bot başlatılamadı: {e}")

if __name__ == '__main__':
    main()
