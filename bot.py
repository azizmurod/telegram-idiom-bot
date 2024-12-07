import json
import random
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters, CallbackQueryHandler


def load_idioms(filename='idioms.json'):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print("Идиомы загружены успешно.")
            if "idioms" in data:
                return data["idioms"]
            else:
                print("Ошибка: в JSON нет ключа 'idioms'.")
                return []
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return []


idioms = load_idioms()

def get_main_keyboard():
    return ReplyKeyboardMarkup([
        ['Получить идиому', 'Помощь']
    ], resize_keyboard=True)


def get_inline_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton('Получить идиому', callback_data='get_idiom')]
    ])


async def start(update: Update, context: CallbackContext) -> None:
    message = (
        "👋 Привет! Я помогу тебе изучать английские идиомы.\n"
        "👉 Нажми 'Получить идиому', чтобы получить случайную идиому с переводом и примером.\n"
        "💡 Для справки нажми 'Помощь'."
    )

    await update.message.reply_text(message, reply_markup=get_main_keyboard())


async def get_idiom(update: Update, context: CallbackContext) -> None:
    idiom = random.choice(idioms)
    message = (
        f"🔤 **Идиома:** {idiom['idiom']}\n"
        f"📝 **Перевод:** {idiom['translation']}\n"
        f"📖 **Пример:** {idiom['example']}"
    )
    await update.message.reply_text(message, parse_mode="Markdown", reply_markup=get_inline_keyboard())


async def help_command(update: Update, context: CallbackContext) -> None:
    message = (
        "📘 Список доступных команд:\n"
        "👉 Нажми 'Получить идиому' — чтобы получить случайную идиому с переводом и примером.\n"
        "👉 Нажми 'Помощь' — чтобы получить список команд."
    )
    await update.message.reply_text(message, reply_markup=get_main_keyboard())


async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    if query.data == 'get_idiom':

        idiom = random.choice(idioms)
        message = (
            f"🔤 **Идиома:** {idiom['idiom']}\n"
            f"📝 **Перевод:** {idiom['translation']}\n"
            f"📖 **Пример:** {idiom['example']}"
        )
        await query.edit_message_text(message, parse_mode="Markdown", reply_markup=get_inline_keyboard())


def main() -> None:
    application = Application.builder().token("7787551431:AAGFoI8foA52p304FTY1e0t2kzVMG87_ma4").build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Обработчик inline кнопок
    application.add_handler(MessageHandler(filters.Regex('^Получить идиому$'), get_idiom))
    application.add_handler(MessageHandler(filters.Regex('^Помощь$'), help_command))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()


if __name__ == "__main__":
    main()
