import telebot
import random
from telebot import types 
import requests
from bs4 import BeautifulSoup as BS 
from PIL import Image
import os
import cv2

# f = open(r'C:\Users\Tamara Sheverdyaeva\bots_tg\anecs.txt', 'r' , encoding='UTF-8')
f = open(r'bot/anecs.txt', 'r', encoding='UTF-8')
anecdotes = f.read().split('\n')
f.close

# images = os.listdir(r'C:\Users\Tamara Sheverdyaeva\bots_tg\images')
images = ['img1.jpg','img2.jpg','img3.jpg','img4.jpg','img5.jpg','img6.jpg','img7.jpg','img8.jpg','img9.jpg','img10.jpg','img11.jpg','img12.jpg']

URL = 'https://citatnica.ru/citaty/mudrye-frazy-i-aforizmy-300-tsitat'
def parser(URL):
    r = requests.get(URL)
    soup = BS(r.text, 'html.parser')
    afors = soup.find_all('div', class_='su-note-inner su-u-clearfix su-u-trim')
    return [c.text for c in afors]


list_of_afors = parser(URL)
random.shuffle(list_of_afors)


TOKEN = '6779687892:AAEx24g351wB4-9Ix8TWZRxFDVsNcjwV6-0'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я бот Matoo! Напиши /hello, чтобы узнать больше')

@bot.message_handler(commands=['hello'])
def hello(message):


    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Что ты умеешь?')
    btn2 = types.KeyboardButton('Список команд')
    btn3 = types.KeyboardButton('куда я жмал?')
    markup.add(btn1, btn2, btn3)

    bot.send_message(message.chat.id,
    f'''Привет, {message.from_user.first_name}!
    Я бот <b>{bot.get_me().first_name}</b>!
    Готов начать работу!''',
         parse_mode='html', reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def pars_text(message):
    if message.text == 'Что ты умеешь?':
        bot.send_message(message.chat.id,
     f'''Я могу: 
     - рассказать анекдот (необязательно смешной)
     - прислать глупую бесмысленную цитату
     - прислать случайную картинку.
                         
    Посмотри список команд и выбери, что тебе интересно.''')


    elif message.text == 'куда я жмал?':
        bot.send_message(message.chat.id, 'я не знаю куда ты жмал, sorry')

    elif message.text ==  'Список команд':

        inline = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton('анекдот', callback_data='anec')
        button_2 = types.InlineKeyboardButton('цитатка', callback_data='citate')
        button_3 = types.InlineKeyboardButton('случайная картинка', callback_data='pict')

        inline.add(button_1,   button_2, button_3)

        bot.send_message(message.chat.id, f'''Команды
                                После окончания работы каждой команды
                                не забудь снова нажать кнопку "список команд"''', reply_markup=inline)



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
     if call.data == 'anec':
        answer = random.choice(anecdotes)
        bot.send_message(call.message.chat.id, answer)
     elif call.data == 'citate':
         

        bot.send_message(call.message.chat.id, list_of_afors[0])
        del list_of_afors[0]
        
     elif call.data == 'pict':
        random_image = random.choice(images)
        with open(os.path.join(r'C:\Users\Tamara Sheverdyaeva\bots_tg\images', random_image), 'rb') as image_file:
            bot.send_photo(call.message.chat.id, photo=image_file)
    
    

bot.polling(non_stop=True)
