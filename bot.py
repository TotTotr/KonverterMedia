import telebot
import requests
import currency_converter
import json
import config
from telebot import types
bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=["help"])
def helping(message):
    bot.send_message(message.chat.id, "Выбери пункт /translate, чтобы перевести валюту")


@bot.message_handler(commands=["convert"])
def translate(message):
    key = types.InlineKeyboardMarkup()
    but_1 = types.InlineKeyboardButton(text="RUB_USD",callback_data="RUB_USD")
    but_2 = types.InlineKeyboardButton(text="USD_RUB",callback_data="USD_RUB")
    key.add(but_1, but_2)
    bot.send_message(message.chat.id,"Выберите конвертер для перевода:", reply_markup=key)

@bot.callback_query_handler(func=lambda c:True)
def inlin(c):
    if c.data == "RUB_USD":
        bot.send_message(c.message.chat.id, "Напишите сумму")
        bot.register_next_step_handler(c.message, translate_rub_usd)
    elif c.data == "USD_RUB":
        bot.send_message(c.message.chat.id, "Напишите сумму")
        bot.register_next_step_handler(c.message, translate_usd_rub)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет, " + message.chat.first_name+ ", я помогу перевести деньги")


@bot.message_handler(content_types=["text"])
def dialog(message):
    if message.text == "Привет" or message.text == "привет":
        bot.send_message(message.chat.id, "Привет, " + message.chat.first_name)
    elif message.text == "Как дела?" or message.text == "Как дела":
        bot.send_message(message.chat.id, "Все отлично. ")



def translate_rub_usd(message):
    from currency_converter import CurrencyConverter
    c = CurrencyConverter()
    sum = message.text
    sum = c.convert(int(sum), 'RUB', 'USD')
    bot.send_message(message.chat.id, str(sum))


def translate_usd_rub(message):
    from currency_converter import CurrencyConverter
    c = CurrencyConverter()
    sum = message.text
    sum = c.convert(int(sum), 'USD', 'RUB')
    bot.send_message(message.chat.id, str(sum))

bot.polling(none_stop=True)


