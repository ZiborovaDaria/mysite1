from django.http import HttpResponse
import telebot

API_TOKEN="7042570168:AAHxnGmR1YIyaYglS6yCB__j8FbdYtrtoYs"

# bot = telebot.TeleBot(API_TOKEN)

# def startbot(request):
#     # bot.set_webhook('https://9e93-83-242-179-137.eu.ngrok.io/')
#     if request.method == "POST":
#         update = telebot.types.Update.de_json(request.body.decode('utf-8'))
#         bot.process_new_updates([update])

#     return HttpResponse('<h1>Ты подключился!</h1>')

# @bot.message_handler(commands=['start'])
# def start(message: telebot.types.Message):
#     name = ''
#     if message.from_user.last_name is None:
#         name = f'{message.from_user.first_name}'
#     else:
#         name = f'{message.from_user.first_name} {message.from_user.last_name}'
#     bot.send_message(message.chat.id, f'Привет! {name}\n'
#                                       f'Я бот, который будет спамить вам беседу :)\n\n'
#                                       f'Чтобы узнать больше команд, напишите /help')
