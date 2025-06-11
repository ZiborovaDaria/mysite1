from aiogram import F, Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from django.conf import settings
from aiogram.filters.command import Command

def setup_bot():
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрация обработчиков (импорты внутри функции)
    from .handlers import (
        cmd_start, cmd_faq, cmd_contacts,
        start_feedback, process_feedback_type, process_product_name,
        process_rating, process_feedback_text, forward_to_operator,
        process_operator_message, cancel_handler,
        process_city, process_store, process_product_choice
    )
    from .states import FeedbackStates

    dp.message.register(cmd_start, Command("start"))
    dp.message.register(cmd_faq, F.text == "Часто задаваемые вопросы")
    dp.message.register(cmd_contacts, F.text == "Контакты")
    dp.message.register(start_feedback, F.text == "Оставить отзыв")
    dp.message.register(forward_to_operator, F.text == "Связаться с оператором")
    dp.message.register(cancel_handler, F.text == "Отмена")

    dp.message.register(process_feedback_type, FeedbackStates.choosing_type)
    dp.message.register(process_city, FeedbackStates.choosing_city)
    dp.message.register(process_store, FeedbackStates.choosing_store)
    dp.message.register(process_product_name, FeedbackStates.entering_product_name)
    dp.message.register(process_product_choice, FeedbackStates.choosing_product)
    dp.message.register(process_rating, FeedbackStates.choosing_rating)
    dp.message.register(process_feedback_text, FeedbackStates.writing_text)
    dp.message.register(process_operator_message, FeedbackStates.forwarding_to_operator)

    return bot, dp

bot, dp = setup_bot()

async def start_bot():
    await dp.start_polling(bot)