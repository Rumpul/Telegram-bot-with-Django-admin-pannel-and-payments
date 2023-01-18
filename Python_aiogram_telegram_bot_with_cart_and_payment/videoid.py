import config
import telebot
import time
import os

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['test'])
def find_file_ids(message):
    """
    Function to get Video Id
    :param message: Start with command /test
    :return: Video Id
    """
    for file in os.listdir('Видео/'):
        if file.split('.')[-1] == 'mp4':
            f = open('Видео/'+ file, 'rb')
            msg = bot.send_video(message.chat.id, f, None, width=1080, height=1920)
            # А теперь отправим вслед за файлом его file_id
            bot.send_message(message.chat.id, msg.video.file_id, reply_to_message_id=msg.message_id)
        time.sleep(3)

if __name__ == '__main__':
    bot.infinity_polling()