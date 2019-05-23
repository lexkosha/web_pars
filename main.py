from bs4 import BeautifulSoup

import requests
import csv


URL = 'site.ru'
URL_XML = 'site/sitemap.xml'


def get_html(url):
    """Получаем html"""
    r = requests.get(url)
    return r.text


def cleam_xml_url(xml_url):
    """Чистим карту сайта формата xml"""
    soup = BeautifulSoup(xml_url, 'lxml')
    url = soup.findAll('loc')
    all_url = []
    for clear_url in url:
        links = str(clear_url)
        links = links[5:-6:1]
        all_url.append(links)
    return all_url


def check_html(html):
    """Вытаскиваем таблицу размеров и артикул. Содаем словарь"""
    soup = BeautifulSoup(html, 'lxml')
    try:
        table = soup.find('div', {'id': 'tb_sizes'})
    except:
        table = 'Нет данных'
    try:
        sku = table.find('th').text[9::1]
    except:
        sku = 'Нет данных'
    data = {'table': table,
            'sku': sku}
    return data


def write_csv(data):
    with open('ecoten.csv', 'a') as f:
        writer = csv.writer(f, delimiter=';')

        writer.writerow((data['table'],
                         data['sku']))
        print(data['sku'], 'Спарсил')


def main():
    all_url = cleam_xml_url(get_html(URL_XML))
    for url in all_url:
        check_url = get_html(url)
        html = check_html(check_url)
        write_csv(html)

if __name__ == '__main__':
    main()