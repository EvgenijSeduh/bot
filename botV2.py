import telebot
from telebot import types
import json

bot = telebot.TeleBot("7602253002:AAGDrKFhtMXE_caajTOxGksmdFGxp2u2v6Y")

with open("bd_questions.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)
way = []


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет " + message.from_user.first_name + "! Какой вопрос тебя интересует?",
        reply_markup=createKeyboard(data.keys(), False),
    )

    
@bot.message_handler()
def menu(message):
    if message.text == 'Назад':
        way.pop()
    else:
        appendUnique(way, message.text)
    if way == []:
        bot.send_message(message.chat.id, 'Главное меню', reply_markup=createKeyboard(data.keys(), False))
    else:
        section = data
        for i in way:
            if not i in section:
                way.pop()
                bot.send_message(message.chat.id, "Я не понял что вы написали, давайте еще раз\n" + 'Главное меню -> '+' -> '.join(way),reply_markup=createKeyboard(section.keys(), True))
                return
            if isinstance(section[i], dict):
                section = section[i]
            elif isinstance(section[i],str):
                bot.send_message(message.chat.id, section[i], reply_markup=createKeyboard([], True))
                return
        bot.send_message(message.chat.id,'Главное меню -> '+' -> '.join(way), reply_markup=createKeyboard(section.keys(), True))


def createKeyboard(keyArr, addBack: bool):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for i in keyArr:
        kb.add(types.KeyboardButton(text=i))
    if addBack:
        kb.add(types.KeyboardButton(text='Назад'))
    return kb

def appendUnique(arr: list, element):
    if not element in arr:
        arr.append(element)
bot.polling()
