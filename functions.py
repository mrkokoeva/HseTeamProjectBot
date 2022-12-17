import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup
import random
import requests
from lxml import etree

data = pd.read_json("processed_items.json")
#data_raw = pd.read_json("items.json")

#st.write(data_raw)

st.write(data)

# по количеству игроков: solo, duel, medium company, big company              --- solo duel normal big
# по продолжительности игры: быстрые (<20 min), среднии(<60min), долгие(else) --- fast normal long

# выбрать теги:

# казуальность: для новичков(difficulty <= 2.5), для опытных (<= 3.5), для профессионалов (else)
# ---beginner veteran professional

def get_filter_string(elements):
    s1 = str()
    for elem in elements:
        s1 += str(elem) + "|"
    if len(s1) > 0:
        s1 = s1[:-1]
    return s1


def recommend_games(number_of_players, duration, difficulty):  # return top 3 games by input params
    data_query = data

    if len(difficulty) > 0:
        data_query = data_query.query('difficulty in @difficulty')
    if len(duration) > 0:
        data_query = data_query.query('playtime_processed in @duration')
    if len(number_of_players) > 0:
        data_query = data_query[data_query['players_processed'].str.contains(get_filter_string(number_of_players))]
   # if len(tags) > 0:
    #    data_query = data_query[data_query['tags'].str.contains(get_filter_string(tags))]

    data_query = data_query.sort_values(by="BGGscore", ascending=False)[:3]

    game_information = [[data_query.iloc[idx][x] for x in ['url', 'name', 'price']] for idx in range(3)]

    #game_information = ['\n\r'.join(game_information[i]) for i in range(3)]

    return game_information


def get_3_upper_games(link):  # print 5 upper games on oage
    r = requests.get(link)
    page = r.content.decode('utf-8')
    soup = BeautifulSoup(page, 'html.parser')
    games = soup.find_all('div', class_="product-item")
    # print("\n\n\n\n\n", games[0], "\n\n\n\n\n")

    for i in range(min(len(games), 3)):
        st.write()
        name = games[i].find('a', class_="name").text
        price = games[i]['data-price']

    # cnt = 0
    # for game in games:
    #     cnt += 1
    #     if cnt == 3:
    #         break
    #     st.write()
    #     print(game.find('a', class_="name").text, "heuy\n\n\n\n\n\n")
    #     name = game.find('a', class_="name").text
    #     price = game['data-price']


def get_games_from_page(link, games_to_return):  # print all games on page
    r = requests.get(link)
    page = r.content.decode('utf-8')
    soup = BeautifulSoup(page, 'html.parser')
    games = soup.find_all('div', class_="product-item")

    for i in range(len(games)):
        name = games[i].find('img')['title']
        # link =
        # image = games[i].find('img')['src']
        price = games[i]['data-price']
        games_to_return.append((name, price))

    return len(soup.find_all('span', class_="icon icon-arrow-right")) != 0  # возвращает 0 если дальше страниц нет


def get_all_games(link):
    page = 1
    games_to_return = list()
    while True:
        page_link = link + "&page=" + str(page)
        is_next_exists = get_games_from_page(page_link, games_to_return)
        if is_next_exists:
            page += 1
        else:
            break
    return games_to_return


def get_3_new_games():
    return get_3_upper_games("https://hobbygames.ru/catalog/search?keyword=&new=1&sort=date_added&order=DESC&parameter_type=1125")


def get_3_hit_games():
    return get_3_upper_games("https://hobbygames.ru/catalog/search?keyword=&hit=1&parameter_type=1125")


def get_all_new_games():
    return get_all_games("https://hobbygames.ru/catalog/search?keyword=&new=1&sort=date_added&order=DESC&parameter_type=1125")


def get_all_hit_games():
    return get_all_games("https://hobbygames.ru/catalog/search?keyword=&hit=1&parameter_type=1125")


def get_random_game():
    game_id = random.randint(0, data.shape[0])
    game = data.iloc[game_id]
    st.write(game)
    game_information = [game[x] for x in ['url', 'name', 'price', 'players', 'playtime', 'tags']]
    st.write(game_information)
    return game_information


# EXAMPLE
number_of_players_1 = ["duel", "normal"]
duration_1 = ["long"]
tags_1 = ["Новогодняя подборка", "Игры для взрослых"]
difficulty_1 = ["professional", "beginner"]

recommend_game = recommend_games(number_of_players_1, duration_1, difficulty_1)

random_game = get_random_game()

get_3_new_games()

#all_tags = set()
#
# for i in range(720):
#     for tag in data.iloc[i]['tags'].split(' / '):
#         all_tags.add(tag)

#st.write(all_tags)



#allowed tags
#{'Детективные истории', 'Игра Престолов. Настольная игра','Кооперативные игры', 'Ticket To Ride (Билет на Поезд)', 'Dungeons and Dragons', 'Песнь льда и огня', 'Каркассон', 'Хардкорные игры', 'Игры для взрослых', 'Блиц!', 'Приключенческие игры', 'Головоломки', 'Игры в дорогу', 'Древний Ужас', 'Uno (Уно)', 'Чужая планета', 'Новогодняя подборка', 'Мафия', 'Стартовый набор', 'Детектив', 'Карточные игры', 'Квесты', 'Классические игры', 'Codenames (Кодовые имена)', 'Спортивные игры', 'Интерактивные игры', 'Манчкин', 'Фигурки и сувениры', 'Игры на внимание', 'Gloomhaven', 'Детские товары', 'Крокодил', 'Логические игры', 'Warhammer Underworlds', 'Шахматы',  'Империи', 'Властелин Колец', 'На ловкость', 'Базовые коробки', 'Командные игры', 'Замес', 'Семейные игры', 'Детективные игры', 'Монополия', 'Детские игры', 'Вселенная Лавкрафта', 'Гарри Поттер', 'Codex (Кодекс)', 'Время Валеры', 'Эмоциональный интеллект', 'Доббль', 'Мрачные истории', 'Подарочные издания', 'Я не робот', 'Игры для компании', 'Подземелье', 'Коробочные Игры', 'Star Wars: Самостоятельные игры', 'Warhammer 40,000', 'Полукооперативные игры', 'Для двоих', 'Вечериночные игры', 'Стратегические игры'}
