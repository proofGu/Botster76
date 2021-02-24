import random
import os
from datetime import datetime

import telebot
from telebot import types
# from telebot.types import Message

# from set import BOT_TOKEN, S

TOKEN = os.environ.get('BOT_TOKEN')
S = os.environ.get('S')

bot = telebot.TeleBot(TOKEN)

smiles = ['🧐', '🤓', '🙂', '😎', '😉', '😊']
invite_s = ["Ооо!!! \nТебя заждались.. \nвот координаты тебе передать просили:",
            "Без тебя не справяться выезжай!!!",
            "Физкульт привет!!! \nЖдем тебя на историческую родину!"]


@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.row('Узнать время', 'Выпустить зверя!')
    f_name = message.from_user.first_name
    bot.send_message(message.chat.id, f'Привет, {f_name}! \nИспользуй /help, о функциях', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def send_help_info(message):
    bot.send_message(message.chat.id, 'При вызове /url появиться кнопка для перехода на habr \n'
                                      'Наберите в сообщении "z=" и текст который нужно развернуть \n'
                                      'Время посмотреть нажав на кнопку \n'
                                      'Еще бот реагирует на пятницу картинки и аудиосообщениям \n' 
                                      'Ну и "Выпустьть зверя" !')


@bot.message_handler(commands=['url'])
def url(message):
    markup = types.InlineKeyboardMarkup()
    btn_my_site = types.InlineKeyboardButton(text='habr.ru', url='https://habrahabr.ru')
    markup.add(btn_my_site)
    bot.send_message(message.chat.id, "Нажми на кнопку и перейди на сайт habr.ru", reply_markup=markup)


@bot.message_handler()
def main_send(message):
    print(message.from_user)
    time1 = datetime.now().strftime('%H:%M:%S')

    if 'пятниц' in message.text.lower():
        bot.reply_to(message, "Уррра!! Урааа!! Пятница!!")
        fri = open('static/f300x214.jpg', 'rb')
        bot.send_sticker(message.chat.id, fri)
    elif message.text.lower() == 'узнать время':
        bot.send_message(message.chat.id, f'уже {time1}')
    elif message.text.lower() == 'выпустить зверя!':
        video = open('static/pafpaf', 'rb')
        bot.send_video(message.chat.id, video)
    elif 'z=' in message.text.lower():
        bot.reply_to(message, f'{message.text[::-1].upper()} \nэто твоя строка наоборот {random.choice(smiles)}')
        if message.from_user.id == S:
            bot.reply_to(message, random.choice(invite_s))
            bot.send_location(427017506, 45.111111, 23.111111)


@bot.message_handler(content_types=['animation', 'sticker', 'video'])
def sticker_mod(message):
    print(message)
    bot.send_message(message.chat.id, 'Живописно то как!!!')


@bot.message_handler(content_types=['voice'])
def sticker_mod(message):
    sti = open('static/voice.jpeg', 'rb')
    bot.send_sticker(message.chat.id, sti)


bot.polling()
