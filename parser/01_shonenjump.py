import bs4
import json
import os
import requests

from utils import (get_content, get_soup, create_dir, write_image, save_json)

BASE_URL = 'https://www.shonenjump.com'
RENSAI_URL = BASE_URL + '/j/rensai/'
ARCHIVES_URL = RENSAI_URL + 'archives.html'
LIST_URL = RENSAI_URL + 'list/'

def shonenjump():
    rensai_soup = get_soup(get_content(RENSAI_URL))
    archives_soup = get_soup(get_content(ARCHIVES_URL))

    # store series information: name, abbreviated name and whether it is still ongoing
    all_series = []

    # create icon directory
    create_dir('icons')

    for soup in [rensai_soup, archives_soup]:
        # ongoing series?
        ongoing = True if soup is rensai_soup else False

        section = soup.find('section', class_='serialSeries')

        for li in section.find_all('li'):
            # series name in japanese
            name_jp = li.div.text if li.div else li.p.text
            name_jp = name_jp[1:name_jp.find('』')]
            
            link_tag = li.a

            # abbreviated name
            abbr = link_tag['href'].rsplit('/', 1)[1][:-5]

            # download icon
            img_src = link_tag.img['src']
            img_url = BASE_URL + img_src
            file_path = os.path.join('icons', abbr + '.' + img_src.rsplit('.', 1)[1])
            print(f'Downloading {file_path}...')
            write_image(img_url, file_path)
            
            # add series
            series = { 'name': name_jp, 'abbr': abbr, 'ongoing': ongoing }
            all_series.append(series)

    # save series information
    save_json("data.json", all_series)

    for series in all_series:
        # create directory
        create_dir(series['abbr'])
            
        current_list_url = LIST_URL + series['abbr'] + '.html'

        while current_list_url:
            list_soup = get_soup(get_content(current_list_url))
            ul = list_soup.find('ul', class_='comicsList')
            
            # ignore series that hasn't release any volume yet
            if ul.li is None:
                break
            
            for dl in ul.select('li dl'):
                # skip current volume if it isn't released yet
                if '発売予定' in str(dl.p):
                    continue

                # download cover
                img_src = dl.img['src']
                img_url = BASE_URL + img_src
                file_path = os.path.join(series['abbr'], img_src.rsplit('/', 1)[1])
                print(f'Downloading {file_path}...')
                write_image(img_url, file_path)

            # get url for next list of covers
            next_list_url_tag = list_soup.find('span', class_='current_page').next_sibling.next_sibling
            if next_list_url_tag is None:
                break
            else:
                current_list_url = BASE_URL + next_list_url_tag['href']

if __name__ == '__main__':
    shonenjump()