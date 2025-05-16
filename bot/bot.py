# from aiogram import Bot, Dispatcher, types
# from aiogram.filters.command import Command
# import asyncio


# API_TOKEN="7042570168:AAHxnGmR1YIyaYglS6yCB__j8FbdYtrtoYs"

# bot=Bot(token=API_TOKEN)
# dp=Dispatcher()


# @dp.message(Command("start"))
# async def send_welcome(message: types.Message):

#     kb=[
#         [types.KeyboardButton(text="Часто задаваемые вопросы")],
#         [types.KeyboardButton(text="Контакты")],
#         [types.KeyboardButton(text="Оставить отзыв")]
#     ]
#     keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите операцию")

#     await message.reply("Вас приветствует компания ЕМЕХ-авто!\n" \
#     "Здесь вы можете узнать ответы на большинство часто задаваемых вопросов.",
#     reply_markup=keyboard)


# async def main():
#     await dp.start_polling(bot)

# if __name__ == '__main__':
#     asyncio.run(main())


from django.core.management.base import BaseCommand
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, Updater, CallbackQueryHandler


API_TOKEN="7042570168:AAHxnGmR1YIyaYglS6yCB__j8FbdYtrtoYs"


class Command(BaseCommand):
    help = 'Starts the Telegram bot'

    def handle(self, *args, **kwargs):
        updater = Updater(token=API_TOKEN, use_context=True)
        dispatcher = updater.dispatcher

        def start(update: Update, context: CallbackContext):
            keyboard = [
                [InlineKeyboardButton("Часто задаваемые вопросы", callback_data='faq')],
                [InlineKeyboardButton("Как оформить заказ?", callback_data='order')],
                [InlineKeyboardButton("Как вернуть товар?", callback_data='return')],
                [InlineKeyboardButton("Связаться с поддержкой", callback_data='support')],
                [InlineKeyboardButton("Контакты", callback_data='contact')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text('Здравствуйте! Я здесь, чтобы помочь вам. Выберите опцию:', reply_markup=reply_markup)

        def button(update: Update, context: CallbackContext):
            query = update.callback_query
            query.answer()

            if query.data == 'faq':
                query.edit_message_text(text='Вот список часто задаваемых вопросов:\n1) Как оформить заказ?\n2) Как вернуть товар?\n3) Как связаться с поддержкой?')
            elif query.data == 'order':
                query.edit_message_text(text='Чтобы оформить заказ, пожалуйста, перейдите на наш сайт и следуйте инструкциям.')
            elif query.data == 'return':
                query.edit_message_text(text='Для возврата товара, пожалуйста, заполните форму на нашем сайте в разделе "Возврат".')
            elif query.data == 'support':
                query.edit_message_text(text='Я не могу ответить на ваш вопрос. Позвольте мне соединить вас с нашим оператором.')
            elif query.data == 'contact':
                query.edit_message_text(text='Вы можете связаться с нами по телефону +7 (XXX) XXX-XX-XX или по электронной почте support@example.com.')

        start_handler = CommandHandler('start', start)
        button_handler = CallbackQueryHandler(button)

        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(button_handler)

        updater.start_polling()
        updater.idle()