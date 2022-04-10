import telebot
import os
import pafy



bot = telebot.TeleBot("KEY") 

@bot.message_handler(commands=['start'])
def started(message):
    bot.send_message(message.chat.id , 'Пропишите /Скачать_Видео')


@bot.message_handler(commands=['Скачать_Видео'])
def video(message):

    msg = bot.send_message(message.chat.id,"Отправте ссылку")
    bot.register_next_step_handler(msg,get_video)

def get_video(message):
    v = pafy.new(message.text)
    global streams
    streams = v.streams

    available_streams = {}
    count = 1 
    global name
    name = v.title
    for stream in streams:
        available_streams[count] = stream
        bot.send_message(message.chat.id,f"{count}: {stream}")
        count += 1    
    bot.send_message(message.chat.id,"Выберите Качество")
    bot.register_next_step_handler(message,final)

def final(message):
    try :
        stream_count = int(message.text)
        bot.send_message(message.chat.id,"Видео скачивается!")
        d = streams[stream_count - 1].download()
    except : 
        bot.send_message(message.chat.id,"Error, Попробуйте другое Качество")
    
    bot.send_message(message.chat.id,"Видео Скачалось!!!")
    video = open(f'{name}.mp4', 'rb')
    bot.send_video(message.chat.id, video)
    bot.register_next_step_handler(message,delete_video)

def delete_video(message):
    os.remove(f"{name}.mp4")
    print('Видео удалилось')
 

bot.polling()
