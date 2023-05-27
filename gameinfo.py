from bs4 import BeautifulSoup
import random
import os
import requests
import json

rows = []
here = os.path.dirname(os.path.abspath(__file__))


def get_game_category():
    category_links = []
    with open(os.path.join(here, 'play_market_categories.txt'), 'r') as open_categories:
        categories_strings = open_categories.readlines()
    for link in categories_strings:
        category_links.append(link.strip('\n'))
    try:
        chosen_category = random.choice(category_links)
    except IndexError:
        chosen_category = random.choice(category_links)
    return chosen_category


def get_soup():
    category = get_game_category()
    category_page = requests.get(category)
    parse_games = BeautifulSoup(category_page.content, 'html.parser')
    soup = parse_games.find_all('div', {'role': 'listitem'})
    return soup


def get_game_link():
    games_list = []
    soup = get_soup()
    if len(soup) == 0:
        soup = get_soup()
    else:
        for game in soup:
            game_link = game.find('a', )['href']
            if 'store/apps/details?id=' in game_link:
                games_list.append(game_link)
    
    game = random.choice(games_list)
    game_full_link = f'https://play.google.com{game}'
    
    return game_full_link


def get_langs_desc(url):
    langs_dict = {'ru': '&hl=ru&gl=US', 'de': '&hl=de&gl=US', 'pl': '&hl=pl&gl=US', 'zh': '&hl=zh&gl=US'}
    descs = {}
    for lang in langs_dict.keys():
        lang_name = f'desc_{lang}'
        parse_link = f'{url}{langs_dict[lang]}'
        resp = requests.get(parse_link)
        parse = BeautifulSoup(str(resp.text), 'html.parser')
        descrip = parse.find('div', {'class': 'bARER'})
        fin_desc = str(descrip).replace('\n', '<br>').replace('\t', '<br>')
        descs[lang_name] = fin_desc
    return descs


def get_game_info():
    tags = []
    imgs_en = []

    url = get_game_link()
    url_en = f'{url}&hl=en&gl=US'

    resp_en = requests.get(url_en)
    parse_en = BeautifulSoup(str(resp_en.text), 'html.parser')
    descrip_en = parse_en.find('div', {'class': 'bARER'})
    desc_en = str(descrip_en).replace('\n', '<br>').replace('\t', '<br>')

    icon_url = parse_en.find('img', {'class': 'T75of'}).attrs['src']
    title = parse_en.find('h1', {'class': 'Fd93Bb'}).text
    try:
        youtube_id = parse_en.find('button', {'class': 'cvriud'}).attrs['data-trailer-url']
    except:
        youtube_id = ''

    imgs_parse_en = parse_en.find_all('img', {'class': 'T75of B5GQxf'})
    for img_en in imgs_parse_en:
        imgs_en.append(img_en.attrs['src'])

    tags_en = parse_en.find_all('span', {'class': 'VfPpkd-vQzf8d'})
    for tag in tags_en[2:-2]:
        tags.append(tag.text)

    prices_block = parse_en.find('button', {'class': 'VfPpkd-LgbsSe'})
    price = prices_block.attrs['aria-label'].replace(' Buy', '').replace('Install', '')

    try:
        year = parse_en.find('div', {'class': 'xg1aie'}).text
    except:
        year = ''

    langs_desc = get_langs_desc(url)

    game_info = {'icon_url': icon_url, 'youtube_id': youtube_id, 'imgs_en': imgs_en, 'title': title, 'tags': tags,
                 'desc_en': desc_en, 'price': price, 'year': year, 'url': url}

    game_info.update(langs_desc)    
    return game_info


def get_n_games(n_games):
    for i in range(n_games):
        game = get_game_info()
        rows.append(game)

    game_info_json = str(json.dumps(rows, ensure_ascii=False))

    return game_info_json



if __name__ == '__main__':
    print(get_n_games(1))
