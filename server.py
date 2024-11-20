import telebot
from api_testin2 import *
import time
bot = telebot.TeleBot("8073250040:AAG9HkbdqHmLvJ-yMX5FyDT3oiWxJQt99UI") # Замените YOUR_BOT_TOKEN на ваш токен бота

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Мяу! Мяяу! мяяяя!")
    bot.register_next_step_handler(message, process_user_message)

def process_user_message(message):
    user_name = message.from_user.first_name
    user_message = message.text
    bot.send_chat_action(message.chat.id, 'typing')
    reply_message = gemini(user_name,user_message)
    if reply_message != "-":
        bot.reply_to(message, reply_message)
        bot.register_next_step_handler(message, process_user_message)
    else:
        time.sleep(0.4)
        bot.register_next_step_handler(message, process_user_message)
bot.polling()