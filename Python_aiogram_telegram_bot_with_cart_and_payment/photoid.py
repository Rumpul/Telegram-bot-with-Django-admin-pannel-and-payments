import config
import telebot
import time
import os

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['test'])
def find_file_ids(message):
    """
    Function to get Photo Id
    :param message: Start with command /test
    :return: Photo Id
    """
    for file in os.listdir('Картинки/'):
        if file.split('.')[-1] == 'png':
            f = open('Картинки/' + file, 'rb')
            msg = bot.send_photo(message.chat.id, f, None)
            # А теперь отправим вслед за файлом его file_id
            bot.send_message(message.chat.id, msg.photo[-1].file_id, reply_to_message_id=msg.message_id)
        time.sleep(3)


if __name__ == '__main__':
    bot.infinity_polling()
