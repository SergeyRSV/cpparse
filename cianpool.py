import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool

from proxy_script_new import stpr

proxy_list = []


def get_proxy_list():
    global proxy_list
    proxy_list = stpr()
    print(proxy_list)
    return proxy_list


def get_proxy():
    global proxy_list
    loop = True
    while loop == True:
        try:
            print('\n' + '+', proxy_list[0])
            print('Connected')
            try:
                headers = {
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
                }
                r = requests.get('http://cian.ru', proxies={'http': proxy_list[0]}, headers=headers, timeout=8)
                print(r)
            except:
                print('Timeout error: ' + str(proxy_list[0]))
                del proxy_list[0]
                continue
            if r.status_code == 200:
                print(r.status_code)
                loop = False
                proxyfile = open("proxy.txt", "w", encoding='utf-8')
                proxyfile.write(proxy_list[0])
                proxyfile.close()
            elif r.status_code == 404:
                print('Конец')
            else:
                del proxy_list[0]
                continue
        except:
            print('Bad')
            del proxy_list[0]
            print(proxy_list)
            continue


def get_html(page):
    global proxy_list
    url = 'https://krasnogorsk.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=' + str(
        page) + '&region=175071&room1=1&room2=1'

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    try:
        print('2', proxy_list[0])
        r = requests.get(url, proxies={'http': proxy_list[0]}, headers=headers, timeout=12)
        return r.text
    except:
        print('block')
        return r


def get_page_link(page_html, page):
    global proxy_list
    soup = BeautifulSoup(page_html, 'lxml')
    is_work = False
    while is_work == False:
        try:
            link = soup.find("div", {
                "class": '_93444fe79c--wrapper--E9jWb'}).findAll("a", {
                "class": 'c6e8ba5398--header--1fV2A'})
            is_work = True
        except:
            print('captcha block')
            del proxy_list[0]
            print(proxy_list)
            get_proxy()
            continue

    links = []
    for link_sin in link:
        links.append(link_sin['href'])
    print(links)
    print('Страница', page, )
    return links


def get_info(url):
    proxy = open('proxy.txt').read().split('\n')
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    r = requests.get(url, proxies={'http': proxy}, headers=headers, timeout=12)

    soup = BeautifulSoup(r.text, 'lxml')

    title = soup.find("h1", {"class": "a10a3f92e9--title--2Widg"})
    address = soup.find("address", {"class": "a10a3f92e9--address--140Ec"})
    price = soup.find("span", {"itemprop": "price"})
    info = soup.find("div", {"class": "a10a3f92e9--info-block--3hCay"})
    description = soup.find("p", {"class": "a10a3f92e9--description-text--1_Lup"})

    string = ''
    string += str(title.text) + '\n'

    for td in address:
        try:
            if td.text == 'На карте':
                break
            else:
                string += str(td.text) + '\n'
        except:
            pass

    for td in info:
        try:
            info = td.find("div", {"class": "a10a3f92e9--info-text--2uhvD"})
            string += str(info.text) + '\n'
        except:
            pass

    string += str(price.text) + '\n'
    string += str(description.text) + '\n' + '\n'

    print(string)

    handle = open("output.txt", "a", encoding='utf-8')
    handle.write(str(string))
    handle.write('------------------\n')
    handle.close()


def tread_parse(page_link):
    with Pool(15) as p:
        p.map(get_info, page_link)


def main():
    page = 1
    get_proxy_list()
    get_proxy()
    while page <= 20:
        page_html = get_html(page)
        page_link = get_page_link(page_html, page)
        tread_parse(page_link)
        get_info(page_link)
        page += 1


if __name__ == '__main__':
    main()
