import telebot
from api_testin3 import *
bot = telebot.TeleBot("7182536634:AAEs_ou2rl9sIDAA_QN3ALNtEGQLM5WHgsw") # Замените YOUR_BOT_TOKEN на ваш токен бота

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Санёк started.")

    bot.register_next_step_handler(message, process_user_message)


def process_user_message(message):
    user_name = message.from_user.first_name
    user_message = message.text
    bot.send_chat_action(message.chat.id, 'typing')
    reply_message = gemini(user_name, user_message)
    if reply_message != "-":
        bot.reply_to(message, reply_message)
    time.sleep(0.3)
    bot.register_next_step_handler(message, process_user_message)

bot.polling()