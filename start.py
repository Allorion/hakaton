from face_identification.autorisation import FaceToFaceAuthorization
from color_identification.script import start
from multiprocessing.pool import ThreadPool
import time
import subprocess
import telebot

bot = telebot.TeleBot("1758127509:AAHmhR7T0ESLFsyN1r4xuWM9v77_UQxHWZY")

obj = FaceToFaceAuthorization()
color, img = start()
while True:
    if color == False:
        bot.send_message(805127154, "Неавторизованный пользователь на машине'KP-21', машина заблокирована")
        photo = open(f'{img}', 'rb')
        bot.send_photo(805127154, photo)
        time.sleep(5)
        status = obj.authorization_start()
        if status == 0 or status == 2:
            cmd='rundll32.exe user32.dll, LockWorkStation'
            subprocess.call(cmd)
            break
        elif status == 1:
            time.sleep(10)
            color = start()
