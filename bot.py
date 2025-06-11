# from aiogram import Dispatcher, types, Bot
# from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram import F
# from aiogram.filters.command import Command
# import asyncio

# API_TOKEN="7042570168:AAHxnGmR1YIyaYglS6yCB__j8FbdYtrtoYs"

# bot=Bot(token=API_TOKEN)
# dp = Dispatcher(storage=MemoryStorage())

# @dp.message(Command('start'))
# async def send_welcome(message: types.Message):
#     kb = [
#         [types.KeyboardButton(text="Часто задаваемые вопросы")],
#         [types.KeyboardButton(text="Контакты")],
#         [types.KeyboardButton(text="Оставить отзыв")]
#     ]
#     keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите операцию")

#     await message.reply("Вас приветствует компания ЕМЕХ-авто!\n" \
#                          "Здесь вы можете узнать ответы на большинство часто задаваемых вопросов.",
#                          reply_markup=keyboard)

# # Функция для обработки команды /faq
# @dp.message((lambda message: message.text == "Часто задаваемые вопросы"))
# async def send_faq(message: types.Message):
#     faq_text = (
#         "Часто задаваемые вопросы:\n"
#         "1. Как оформить заказ?\n"
#         "2. Как отменить заказ?\n"
#         "3. Как получить возврат?\n"
#         "4. Где я могу найти информацию о доставке?\n"
#         "Если у вас есть другие вопросы, не стесняйтесь спрашивать!"
#     )
#     await message.reply(faq_text)

# # Функция для обработки команды /contact
# @dp.message((lambda message: message.text == "Контакты"))
# async def send_contact_info(message: types.Message):
#     contact_info = (
#         "Контакты нашей компании:\n"
#         "Телефон: +1 (234) 567-8901\n"
#         "Электронная почта: support@company.com\n"
#         "Адрес: 123 Main St, City, Country"
#     )
#     await message.reply(contact_info)

# # Функция для обработки команды /rate
# @dp.message((lambda message: message.text == "Оставить отзыв"))
# async def rate_product(message: types.Message):
#     await message.reply("Пожалуйста, оцените наш продукт от 1 до 5 (где 1 - плохо, 5 - отлично).")

#     # Ожидание ответа пользователя
#     @dp.message(lambda message: message.text.isdigit() and 1 <= int(message.text) <= 5)
#     async def get_rating(rating_message: types.Message):
#         rating = int(rating_message.text)
#         await rating_message.reply(f"Спасибо за вашу оценку: {rating} из 5!")
    
#     # Обработка неправильного ввода
#     @dp.message(lambda message: not message.text.isdigit() or not (1 <= int(message.text) <= 5), state='*')
#     async def invalid_rating(rating_message: types.Message):
#         await rating_message.reply("Пожалуйста, введите число от 1 до 5.")


# async def main():
#     await dp.start_polling(bot)

# if __name__ == '__main__':
#     asyncio.run(main())

