import pandas as pd
from bs4 import BeautifulSoup
import random
import requests

data = pd.read_json("processed_items.json")


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

    data_query = data_query.sort_values(by="BGGscore", ascending=False)[:min(3, data_query.shape[0])]

    game_information = [[data_query.iloc[idx][x] for x in ['url', 'name', 'price']] for idx in range(min(3, data_query.shape[0]))]

    game_information = ['\n\r'.join(game_information[i]) for i in range(min(3, len(game_information)))]

    while len(game_information) < 3:
        game_id = random.randint(0, data.shape[0])
        game = data.iloc[game_id]
        game_information_add = [game[x] for x in ['url', 'name', 'price']]
        game_information.append('\n\r'.join(game_information_add))
    return game_information


def get_3_upper_games(link):  # print 5 upper games on page
    r = requests.get(link)
    page = r.content.decode('utf-8')
    soup = BeautifulSoup(page, 'html.parser')
    games = soup.find_all('div', class_="product-item")

    games_to_return = list()

    for i in range(min(len(games), 3)):
        name = games[i].find('picture').find('img')['title']
        price = games[i]['data-price']
        link = games[i].find('div', class_='image').find('a')['href']
        players = soup.find_all('div', class_='params')[i].find('div', class_='params__item players')['title']
        time = soup.find_all('div', class_='params__item time')[i]['title']
        to_add = ' / '.join([link, name, price, players, time])
        games_to_return.append(to_add)
    return games_to_return


def get_games_from_page(link):  # print all games on page
    r = requests.get(link)
    page = r.content.decode('utf-8')
    soup = BeautifulSoup(page, 'html.parser')
    games = soup.find_all('div', class_="product-item")

    games_to_return = list()

    for i in range(len(games)):
        name = games[i].find('picture').find('img')['title']
        price = games[i]['data-price']
        link = games[i].find('div', class_='image').find('a')['href']
        to_add = ' / '.join([link, name, price])
        games_to_return.append(to_add)
    return (games_to_return,
            len(soup.find_all('span', class_="icon icon-arrow-right")) != 0)  # возвращает 0 если дальше страниц нет


def get_all_games(link):
    page = 1
    games_to_return_extended = list()
    while True:
        page_link = link + "&page=" + str(page)
        (games_to_return, is_next_exists) = get_games_from_page(page_link)
        games_to_return_extended.extend(games_to_return)
        if is_next_exists:
            page += 1
        else:
            break
    return games_to_return_extended


def get_3_new_games():
    return get_3_upper_games(
        "https://hobbygames.ru/catalog/search?keyword=&new=1&sort=date_added&order=DESC&parameter_type=1125")


def get_3_hit_games():
    return get_3_upper_games("https://hobbygames.ru/catalog/search?keyword=&hit=1&parameter_type=1125")


def get_all_new_games():
    return get_all_games(
        "https://hobbygames.ru/catalog/search?keyword=&new=1&sort=date_added&order=DESC&parameter_type=1125")


def get_all_hit_games():
    return get_all_games("https://hobbygames.ru/catalog/search?keyword=&hit=1&parameter_type=1125")


def get_random_game():
    game_id = random.randint(0, data.shape[0])
    game = data.iloc[game_id]
    game_information = [game[x] for x in ['url', 'name', 'price', 'players', 'playtime', 'tags']]
    return game_information
