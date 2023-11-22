import logging

from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
from django.conf import settings
from telegram.ext import CallbackQueryHandler, MessageHandler, filters
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from weather.models import BotUser, Message
from weather.services import WeatherService


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


@sync_to_async
def get_or_create_bot_user(update):
    return BotUser.objects.get_or_create(
        user_id=update.message.chat_id,
        defaults={
            'name': update.message.from_user.username,
        }
    )


@sync_to_async
def create_msg(bot_user: BotUser, input_text: str, response_msg: str) -> None:
    Message(
        bot_user=bot_user,
        request_msg=input_text,
        response_msg=response_msg,
    ).save()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    await get_or_create_bot_user(update)

    keyboard = [[InlineKeyboardButton("Узнать погоду", callback_data='weather')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Телеграм бот для получения информации о погоде:", reply_markup=reply_markup)


async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    await query.answer()

    await query.edit_message_text(text=f"Введите название города")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input_text = update.message.text
    if 'Узнать погоду' in input_text:
        response_msg = "Введите название города"
    else:
        weather_service = WeatherService()
        try:
            weather_data = weather_service.get_weather_data(input_text)
            response_msg = (f'Погода в городе {input_text}:\n\n'
                            f'Температура: {weather_data.temperature}\n'
                            f'Давление: {weather_data.pressure}\n'
                            f'Скорость ветра: {weather_data.wind_speed}')
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            response_msg = "Не удалось получить данные о погоде. Попробуйте еще раз."

    await update.message.reply_text(response_msg)

    bot_user, _ = await get_or_create_bot_user(update)

    await create_msg(bot_user, input_text, response_msg)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Use /start to test this bot.")


class Command(BaseCommand):

    def handle(self, *args, **options):
        app = ApplicationBuilder().token(settings.TOKEN).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(button_click, pattern='weather'))
        app.add_handler(CommandHandler("help", help_command))

        app.add_handler(MessageHandler(filters.TEXT, handle_message))

        app.run_polling()
