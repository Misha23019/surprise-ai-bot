from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Пример кнопок для меню (можно расширять)
def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("🎁 Сюрприз", callback_data="surprise")],
        [InlineKeyboardButton("⚙ Настройки", callback_data="settings")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Обработчик команды /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}! Добро пожаловать в Surprise Me! Бот.",
        reply_markup=get_main_keyboard()
    )

# Обработчик текстовых сообщений
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    await update.message.reply_text(f"Ты написал: {text}")

# Обработчик нажатий кнопок
async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Подтверждаем, чтобы убрать часики
    data = query.data
    if data == "surprise":
        await query.edit_message_text("🎁 Вот твой сюрприз!")
    elif data == "settings":
        await query.edit_message_text("⚙ Здесь будут настройки...")

# Создаем и возвращаем объект Application (бота)
def create_application(token: str):
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(CallbackQueryHandler(handle_callback_query))

    return application
