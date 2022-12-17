import telebot
from telebot import types
import functions
import shops
from geopy.distance import geodesic
import library
import func
import os

bot = telebot.TeleBot(os.environ['PROJECT_BOT_TOKEN'])

@bot.message_handler(commands=['start'])  # можно несколько фиговин
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)  #
    knopka1 = types.KeyboardButton("Рандомная настолка")  # 1
    knopka2 = types.KeyboardButton("Порекомендуй настолку")  # 2
    knopka4 = types.KeyboardButton("3 новые игры")
    knopka5 = types.KeyboardButton("Хиты")
    knopka6 = types.KeyboardButton("Ближайший от меня магазин", request_location=True)
    knopka7 = types.KeyboardButton("Для Тимура")
    markup.add(knopka1, knopka2, knopka4, knopka5, knopka6, knopka7)
    bot.send_message(message.chat.id, text="Привет всем любителям настолок",
                     reply_markup=markup)  # можно еще режим указать(parse_mode)


@bot.message_handler(commands=['geo'])
def geo(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Отправь мне своё местоположение", reply_markup=keyboard)


@bot.message_handler(func=lambda message: True)
def bot_message(message):
    if message.text == 'Рандомная настолка':
        ans = functions.get_random_game()
        link = ans[0]
        name = ans[1]
        price = ans[2]
        players = ans[3]
        time = ans[4]
        tag = ans[5]
        mes = "Название:" + name + '\n' + '\n' + "Цена:" + price + '\n' + '\n' + "Количество игроков:" + players + '\n' + '\n' + "Время игры:" + time + '\n' + '\n' "Тэги:" + tag
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Страничка", url=link))
        bot.send_message(message.chat.id, text=mes, reply_markup=markup)
    elif message.text == 'Порекомендуй настолку':
        tex = "Так, давай подберем настолку. Для этого тебе надо ответить на 3 вопроса." + '\n' + '\n' + "Количество игроков: " + '\n' + "1. Одиночный" + '\n' + "2.Дуэль" + '\n' + "3.Для средней компании(3-8 человек)" + '\n' + "4. Для большой компании(от 8 человек)" '\n' + \
              '\n' + 'Продолжительность игры:' + '\n' + "1.Быстрые(<20 минут)" + '\n' + "2.Нормальные(<60 минут)" + '\n' + "3.Долгие(>60 минут)" + '\n' + '\n' + "Сложность игры:" + '\n' + \
              "1. Легкие" + '\n' + "2. Средней сложности" + '\n' + "3.Сложные \n Ответ дайте в формате: ANS 1 2 3"
        bot.send_message(message.chat.id, text=tex)
    # сделать словарик
    # чтобы 2 варианта было
    elif message.text == "3 новые игры":
        lst = func.get_3_new_games()
        game1 = lst[0].split(" / ")
        game2 = lst[1].split(" / ")
        game3 = lst[2].split(" / ")
        tex1 = "Название: " + game1[1] + '\n' + '\n' + "Цена: " + game1[2] + '\n' + '\n' + game1[3] + '\n' + '\n' + \
               game1[4]
        tex2 = "Название: " + game2[1] + '\n' + '\n' + "Цена: " + game2[2] + '\n' + '\n' + game2[3] + '\n' + '\n' + \
               game2[4]
        tex3 = "Название: " + game3[1] + '\n' + '\n' + "Цена: " + game3[2] + '\n' + '\n' + game3[3] + '\n' + '\n' + \
               game3[4]
        markup1 = types.InlineKeyboardMarkup()
        markup1.add(types.InlineKeyboardButton("Ссылка на игру", url=game1[0]))
        markup2 = types.InlineKeyboardMarkup()
        markup2.add(types.InlineKeyboardButton("Ссылка на игру", url=game2[0]))
        markup3 = types.InlineKeyboardMarkup()
        markup3.add(types.InlineKeyboardButton("Ссылка на игру", url=game3[0]))
        bot.send_message(message.chat.id, text=tex1, reply_markup=markup1)
        bot.send_message(message.chat.id, text=tex2, reply_markup=markup2)
        bot.send_message(message.chat.id, text=tex3, reply_markup=markup3)
    elif message.text == "ANS 4 3 3":
        bot.send_message(message.chat.id, "Нет настолок по заданным параметрам. Попробуйте вбить другие")
    elif "ANS" in message.text:
        str_text = message.text.split()
        if 1 <= int(str_text[1]) <= 4 and 1 <= int(str_text[2]) < 4 and 1 <= int(str_text[3]) < 4:
            ans = functions.recommend_games(library.amount_dict[int(str_text[1])], library.time_dict[int(str_text[2])],
                                            library.difficulty_dict[int(str_text[3])])
            for i in range(0, 3):
                markup1 = types.InlineKeyboardMarkup()
                markup1.add(types.InlineKeyboardButton("Ссылка на игру", url=ans[i][0]))
                tex = "Название: " + ans[i][1] + "\n" + "Цена:" + ans[i][2]
                bot.send_message(message.chat.id, text=tex, reply_markup=markup1)
        else:
            bot.send_message(message.chat.id, "Я вас не понимаю")
    elif message.text == "Хиты":
        lst = func.get_3_hit_games()
        game1 = lst[0].split(" / ")
        game2 = lst[1].split(" / ")
        game3 = lst[2].split(" / ")
        tex1 = "Название: " + game1[1] + '\n' + '\n' + "Цена: " + game1[2] + '\n' + '\n' + game1[3] + '\n' + '\n' + \
               game1[4]
        tex2 = "Название: " + game2[1] + '\n' + '\n' + "Цена: " + game2[2] + '\n' + '\n' + game2[3] + '\n' + '\n' + \
               game2[4]
        tex3 = "Название: " + game3[1] + '\n' + '\n' + "Цена: " + game3[2] + '\n' + '\n' + game3[3] + '\n' + '\n' + \
               game3[4]
        markup1 = types.InlineKeyboardMarkup()
        markup1.add(types.InlineKeyboardButton("Ссылка на игру", url=game1[0]))
        markup2 = types.InlineKeyboardMarkup()
        markup2.add(types.InlineKeyboardButton("Ссылка на игру", url=game2[0]))
        markup3 = types.InlineKeyboardMarkup()
        markup3.add(types.InlineKeyboardButton("Ссылка на игру", url=game3[0]))
        bot.send_message(message.chat.id, text=tex1, reply_markup=markup1)
        bot.send_message(message.chat.id, text=tex2, reply_markup=markup2)
        bot.send_message(message.chat.id, text=tex3, reply_markup=markup3)
    elif message.text == "Для Тимура":
        photo = open('попугай.jpeg', 'rb')
        bot.send_photo(message.chat.id, photo=photo)
    else:
        bot.send_message(message.chat.id, "Я вас не понимаю")


@bot.message_handler(func=lambda message: True, content_types=['location'])
def dist(message):
    lat = message.location.latitude
    lon = message.location.longitude
    d = []
    for km in shops.shop:
        res = geodesic((km['lonm'], km['latm']), (lat, lon)).kilometers
        d.append(res)
    idx = d.index(min(d))
    d_str = str(round(min(d), 2))
    tex = shops.shop[idx]['title'] + '\n' + "Адрес: " + shops.shop[idx][
        'address'] + '\n' + "Расстояние: " + d_str + "км"
    bot.send_message(message.chat.id, text=tex, parse_mode='HTML')
    bot.send_venue(message.chat.id,
                   shops.shop[idx]['lonm'],
                   shops.shop[idx]['latm'],
                   shops.shop[idx]['title'],
                   shops.shop[idx]['address'])


# магазины Hobby Games


bot.polling(none_stop=True)
