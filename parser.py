import random
from urllib.request import urlopen

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
from typing import Optional
import json
import time


class Parser:

    def __init__(self):
        self.options = Options()
        # options.add_experimental_option("detach", True)
        self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(
            options=self.options
        )
        self.driver.maximize_window()

    def get_names(self):
        url = 'https://peoplenames.ru'
        firstnames = set()
        counter, n, m = 0, 20, 20
        for i in range(1, n + 1):
            self.driver.get(url=url + f'/female?page={i}')
            time.sleep(0.15)
            names = self.driver.find_elements(by=By.XPATH, value='//ol[@class="sex__names"]/li')
            names = set(map(lambda x: x.text.split('\n')[0], names))
            time.sleep(0.2)
            firstnames = firstnames.union(names)
            counter += 1
            print(f'{counter}/{n + m}')
        for i in range(1, m + 1):
            self.driver.get(url=url + f'/male?page={i}')
            names = self.driver.find_elements(by=By.XPATH, value='//ol[@class="sex__names"]/li')
            names = set(map(lambda x: x.text.split('\n')[0], names))
            time.sleep(0.2)
            firstnames = firstnames.union(names)
            counter += 1
            print(f'{counter}/{n + m}')
        with open('src/firstnames.txt', 'w', encoding='utf-8') as file:
            file.write('\n'.join(firstnames) + '\n')

    def get_regions(self):
        url = 'https://ru.wikipedia.org/wiki/Список_городов_России'
        self.driver.get(url=url)
        time.sleep(0.5)
        path_to_element = '//table[@class="standard sortable jquery-tablesorter"]/tbody/tr/td[4]/a'
        regions = self.driver.find_elements(by=By.XPATH, value=path_to_element)
        time.sleep(1)
        regions = set(map(lambda x: x.text.split('\n')[0], regions))
        time.sleep(0.2)
        with open('src/regions.txt', 'w', encoding='utf-8') as file:
            file.write('\n'.join(regions) + '\n')

    def get_tlds(self):
        url = 'https://en.wikipedia.org/wiki/List_of_Internet_top-level_domains'
        self.driver.get(url=url)
        time.sleep(0.5)

    def get_instruments(self):
        def parse_element(html_code: str, subcategory: str) -> Optional[dict[str, str]]:
            URL = 'https://www.muztorg.ru'
            soup = BeautifulSoup(html_code, 'html.parser')
            try:
                header_block = soup.find('div', class_='product-header').find('a')
            except Exception:
                return None
            href = header_block.get('href')
            title = header_block.get_text()
            del header_block
            try:
                img_href = soup.find('img', class_='img-responsive').get('data-src')
                if img_href is None:
                    return None
                price = soup.find('meta', itemprop='price').get('content')
            except Exception:
                return None
            rate = random.randint(0, 50) / 10
            return {'title': title, 'href': URL + href, 'img_href': img_href if URL in img_href else URL + img_href,
                    'price': int(price), 'rate': rate, 'subcategory': subcategory}

        with open('src/categories.json', 'r', encoding='utf-8') as file:
            href_dicts = [{item['href']: item['title'] for item in i["subcategories"]} for i in json.load(file)]
        instruments = list()
        for href_dict in href_dicts:
            for href in href_dict:
                for page_id in range(1, 4):
                    url = href + f'?page={page_id}'
                    print(url)
                    try:
                        self.driver.get(url=url)
                        time.sleep(0.5)
                    except Exception:
                        continue
                    path_to_element = '//section[@class="product-thumbnail"]'
                    sections = self.driver.find_elements(by=By.XPATH, value=path_to_element)
                    time.sleep(0.5)
                    elements = map(lambda x: parse_element(x.get_attribute('innerHTML'), href_dict[href]), sections)
                    elements = filter(lambda x: x is not None, elements)
                    instruments.extend(elements)
            with open('src/items/instruments/common.json', 'w', encoding='utf-8') as file:
                json.dump(instruments, file, indent=4)

    def load_instruments_img(self):
        with open("src/items/instruments/common.json", "r", encoding="utf-8") as file:
            items = json.load(file)
        counter, target = 0, len(items)
        for item in items:
            article = item["href"].split('/')[-1]
            out = open(f"src/items/instrument-images/{article}.jpg", 'wb')
            img = urlopen(item['img_href'])
            out.write(img.read())
            out.close()
            counter += 1
            print(f"{counter} / {target}")


if __name__ == "__main__":
    p = Parser()
    p.get_instruments()