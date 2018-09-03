import bs4
import json
import requests
import time

from utils import (get_content, get_soup, save_json, load_json)

MANGA_SEARCH_URL = 'https://myanimelist.net/manga.php?type=1&q='

# load series information
all_series = load_json("data.json")

for series in all_series:
    # search on MyAnimeList
    query_soup = get_soup(get_content(MANGA_SEARCH_URL + series['name']))
    time.sleep(15) # rate limiting

    table_row_tag = query_soup.find('div', class_='js-categories-seasonal').tr.next_sibling
    link_tag = table_row_tag.find('a', class_='hoverinfo_trigger fw-b')

    # series name in english
    name_en = link_tag.strong.text
    print(f'{series["name"]} | {name_en}')

    # parse series page
    info_url = link_tag['href']
    info_soup = get_soup(get_content(info_url))
    time.sleep(15) # rate limiting

    container = info_soup.find('div', class_='js-scrollfix-bottom')

    # author
    author_tags = container.find('span', string='Authors:').parent.find_all('a')
    author = ''
    for tag in author_tags:
        author_name = tag['href'].rsplit('/', 1)[1].replace('_', ' ')
        author_work = tag.next_sibling # story, art or both
        author += author_name + author_work

    # update series information
    series['name'] = name_en
    series['author'] = author

# save updated series information
save_json("data.json", all_series)