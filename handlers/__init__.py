from telegram.ext import CommandHandler, MessageHandler, filters, Application

def setup_handlers(application: Application) -> None:
    application.add_handler(CommandHandler("start", start_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

async def start_command(update, context):
    await update.message.reply_text("你好！ Добро пожаловать в HanziLearner!")

async def handle_message(update, context):
    text = update.message.text
    await update.message.reply_text(f"You said: {text}")