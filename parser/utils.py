import bs4
import json
import os
import requests

def get_content(url):
    res = requests.get(url)
    res.raise_for_status()
    res.encoding = 'utf-8'
    return res.text

def get_soup(html):
    return bs4.BeautifulSoup(html, 'lxml')

def create_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def write_image(url, file_path):
    res = requests.get(url)
    res.raise_for_status()

    img_file = open(file_path, 'wb')
    for chunk in res.iter_content(1000000): # 1 MB
        img_file.write(chunk)
    img_file.close()

def save_json(file_path, data):
    with open(file_path, "w") as write_file:
        json.dump(data, write_file)

def load_json(file_path):
    with open(file_path, "r") as read_file:
        data = json.load(read_file)
    return data