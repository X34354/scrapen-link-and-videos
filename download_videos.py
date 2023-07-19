import pandas as pd
import time
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import os
import re
import json


def get_download_link(link):

    cookies = {
        '_ga': 'GA1.2.1563791596.1674937703',
        '__cflb': '02DiuEcwseaiqqyPC5reXswsgyrfhBQenxsTGZJLiEXYo',
        '_gid': 'GA1.2.79836344.1679896364',
        '_gat_UA-3524196-6': '1',
    }

    headers = {
        'authority': 'ssstik.io',
        'accept': '*/*',
        'accept-language': 'es-419,es;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'hx-current-url': 'https://ssstik.io/es',
        'hx-request': 'true',
        'hx-target': 'target',
        'hx-trigger': '_gcaptcha_pt',
        'origin': 'https://ssstik.io',
        'referer': 'https://ssstik.io/es',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    }


    params = {
        'url': 'dl',
    }

    data = {
        'id': link,
        'locale': 'es',
        'tt': 'bm9XdHlh',
    }

    response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)
    download_soup = BeautifulSoup(response.text, "html.parser")
    download_link = download_soup.a["href"]
    return download_link , download_soup


def save_video_from_soup( index, mp4_file , sobre):
    paragraphs = []
    try:
        for x in sobre:
            paragraphs.append(str(x))

        nombre = [re.split("@", paragraphs[0])[0]]
        if len(nombre) == 0 or len(nombre) > 76:
            nombre = ['Meme' + str(index)]
    except:
        nombre = 'meme' + str(index)

    with open(f"videos_to_narrate/{nombre[0]}.mp4", "wb") as output:
        while True:
            data = mp4_file.read(4096)
            if data:
                output.write(data)
            else:
                break


def download_video(link, index):
    download_link, download_soup = get_download_link(link)
    mp4_file = urlopen(download_link)
    sobre = download_soup.find(class_="maintext").extract()

    save_video_from_soup(index,mp4_file, sobre )


def clean_and_process_videos(data):

    df = pd.read_csv(data['file_path'])
    videos = list(df['URL'])
    videos = videos[:100]
    i = 0

    for video in videos:
        nombre = video
        lista = nombre.split('/')
        nombre = lista[3] + '-' + lista[5]
        print(nombre)
        path_r = data['path'] + str(nombre) + '.mp4'
        

        is_exist = os.path.exists(path_r)


        if is_exist :
            continue
        else:
            try:
                download_video(video, i)
                time.sleep(30)
            except:
                print('Failed to download the video:', nombre)
                time.sleep(30)
        i += 1

if __name__ == "__main__":
    
    # Open the JSON file
    with open('configuration.json', 'r') as file:
        data = json.load(file)

    clean_and_process_videos(data)
