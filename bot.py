import telebot
from io import BytesIO
import cv2
from PIL import Image
import numpy as np
from ultralytics import YOLO

TOKEN = 'токен'

ALLOWED_FORMATS = ['.bmp', '.dng', '.jpeg', '.jpg', '.mpo', '.png', '.tif', '.tiff', '.webp', '.pfm', '.asf', '.avi', '.gif', '.m4v', '.mkv', '.mov', '.mp4', '.mpeg', '.mpg', '.ts', '.wmv', '.webm']

Model = YOLO('best.pt')

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Привет! Я бот для детектирования сорняков и посева на изображениях.\nДля уточнения поддерживаемых форматах напишите команду "/help"')

@bot.message_handler(commands=['help'])
def send_help(message):
    available_formats = "Доступные форматы для обработки:\n\n"  \
                        "'.bmp', '.dng', '.jpeg', '.jpg', '.mpo', '.png', '.tif', '.tiff', '.webp', '.pfm'"

    bot.reply_to(message, available_formats)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.reply_to(message, 'Отправьте мне фото или файл и я помогу вам с детекцией.')

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        file_stream = bot.download_file(file_info.file_path)

        img = cv2.imdecode(np.frombuffer(file_stream, np.uint8), -1)
        res = Model(img)
        res_plotted = res[0].plot()
        res_plotted = cv2.cvtColor(res_plotted, cv2.COLOR_BGR2RGB)

        image_bytes = BytesIO()
        Image.fromarray(res_plotted).save(image_bytes, format='JPEG')
        image_bytes.seek(0)

        bot.send_photo(message.chat.id, photo=image_bytes)
        bot.reply_to(message, 'Сделяль')

    except Exception as e:
        bot.reply_to(message, 'Произошла ошибка при обработке фото. Пожалуйста, попробуйте еще раз.')


@bot.message_handler(content_types=['document'])
def handle_document(message):
    return handle_photo(message)

bot.polling(none_stop=True)
