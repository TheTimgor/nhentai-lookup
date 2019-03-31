import requests
from bs4 import BeautifulSoup
import re
from PIL import Image
import pytesseract
import io
import os
from time import sleep

os.environ["TESSDATA_PREFIX"] = 'tessdata'


def get_text(url, lang):
    response = requests.get(url)
    i = Image.open(io.BytesIO(response.content))
    t = pytesseract.image_to_string(i, lang=lang)
    return t


for nh_id in range(1, 999999):
    print(f'getting gallery {nh_id}')
    coverpage = requests.get(f'http://nhentai.net/g/{nh_id}')
    if not coverpage.status_code == 404:
        soup = BeautifulSoup(coverpage.text, 'lxml')
        tags = soup.find(text=re.compile('Languages')).parent.findAll()
        languages = [t.text for t in tags]
        if any('japanese' in l.lower() for l in languages):
            language = 'jpn'
        elif any('english' in l.lower() for l in languages):
            language = 'eng'
        elif any('chinese' in l.lower() for l in languages):
            language = 'chi_sim'
        print(language)

        i = 1
        while True:
            page = requests.get(f'https://nhentai.net/g/{nh_id}/{i}')
            # print(page)
            soup = BeautifulSoup(page.text, 'lxml')
            imgs = soup.select('#image-container')
            if len(imgs) < 1:
                break
            img = imgs[0].find('a').img['src']
            text = get_text(img, language)
            print(text)
            i += 1


