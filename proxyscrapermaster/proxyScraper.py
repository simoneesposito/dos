import requests
from bs4 import BeautifulSoup
import threading
import os
import argparse


pathTextFile = ''
proxyType = ''

# From proxyscrape.com
def proxyscrapeScraper(proxytype, timeout, country):
    response = requests.get("https://api.proxyscrape.com/?request=getproxies&proxytype=" + proxytype + "&timeout=" + timeout + "&country=" + country)
    proxies = response.text
    with open(pathTextFile, "a") as txt_file:
        txt_file.write(proxies)


# From proxy-list.download
def proxyListDownloadScraper(url, type, anon):
    session = requests.session()
    url = url + '?type=' + type + '&anon=' + anon
    html = session.get(url).text
    if args.verbose:
        print(url)
    with open(pathTextFile, "a") as txt_file:
        for line in html.split('\n'):
            if len(line) > 0:
                txt_file.write(line)

# From proxy-list.download
def personal(url):
    session = requests.session()
    url = url
    html = session.get(url).text
    if args.verbose:
        print(url + ' scraped successfully')
    with open(pathTextFile, "a") as txt_file:
        for line in html.split('\n'):
            if len(line) > 0:
                txt_file.write(line)


# From sslproxies.org, free-proxy-list.net, us-proxy.org, socks-proxy.net
def makesoup(url):
    page=requests.get(url)
    if args.verbose:
        print(url + ' scraped successfully')
    return BeautifulSoup(page.text,"html.parser")


def proxyscrape(table):
    proxies = set()
    for row in table.findAll('tr'):
        fields = row.findAll('td')
        count = 0
        proxy = ""
        for cell in row.findAll('td'):
            if count == 1:
                proxy += ":" + cell.text.replace('&nbsp;', '')
                proxies.add(proxy)
                break
            proxy += cell.text.replace('&nbsp;', '')
            count += 1
    return proxies


def scrapeproxies(url):
    soup=makesoup(url)
    result = proxyscrape(table = soup.find('table', attrs={'class': 'table table-striped table-bordered'}))
    proxies = set()
    proxies.update(result)
    with open(pathTextFile, "a") as txt_file:
        for line in proxies:
	        txt_file.write("".join(line) + "\n")


# output watcher
def output():
    if os.path.exists(pathTextFile):
        os.remove(pathTextFile)
    elif not os.path.exists(pathTextFile):
        with open(pathTextFile, 'w'): pass


if __name__ == "__main__":

        global proxy

        parser = argparse.ArgumentParser()
        parser.add_argument("-p", "--proxy", help="Supported proxy type: http ,https, socks, socks4, socks5", required=True)
        parser.add_argument("-o", "--output", help="output file name to save .txt file", default='output.txt')
        parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
        args = parser.parse_args()

        proxy = args.proxy
        pathTextFile = args.output

        if proxy == 'https':
            threading.Thread(target=scrapeproxies, args=('http://sslproxies.org',)).start()
            threading.Thread(target=proxyListDownloadScraper, args=('https://www.proxy-list.download/api/v1/get', 'https', 'elite',)).start()
            threading.Thread(target=proxyListDownloadScraper, args=('https://www.proxy-list.download/api/v1/get', 'https', 'transparent',)).start()
            threading.Thread(target=proxyListDownloadScraper, args=('https://www.proxy-list.download/api/v1/get', 'https', 'anonymous',)).start()
            threading.Thread(target=personal, args=('https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt',)).start()
            threading.Thread(target=personal, args=('https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http%2Bhttps.txt',)).start()
            threading.Thread(target=personal, args=('https://raw.githubusercontent.com/roma8ok/proxy-list/main/proxy-list-https.txt',)).start()
            threading.Thread(target=personal, args=('https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt',)).start()
            threading.Thread(target=personal, args=('https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt',)).start()
            threading.Thread(target=personal, args=('https://www.proxy-list.download/api/v1/get?type=https',)).start()

            output()

        if proxy == 'http':
            threading.Thread(target=scrapeproxies, args=('http://free-proxy-list.net',)).start()
            threading.Thread(target=scrapeproxies, args=('http://us-proxy.org',)).start()
            threading.Thread(target=proxyscrapeScraper, args=('http','1000','All',)).start()
            threading.Thread(target=proxyListDownloadScraper, args=('https://www.proxy-list.download/api/v1/get', 'http', 'elite',)).start()
            threading.Thread(target=proxyListDownloadScraper, args=('https://www.proxy-list.download/api/v1/get', 'http', 'transparent',)).start()
            threading.Thread(target=proxyListDownloadScraper, args=('https://www.proxy-list.download/api/v1/get', 'http', 'anonymous',)).start()
            threading.Thread(target=personal, args=('https://api.proxyscrape.com/v2/?request=getproxies&protocol=http',)).start()
            threading.Thread(target=personal, args=('https://raw.githubusercontent.com/chipsed/proxies/main/proxies.txt',)).start()
            threading.Thread(target=personal, args=('https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',)).start()
            threading.Thread(target=personal, args=('https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt',)).start()
            threading.Thread(target=personal, args=('https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt',)).start()
            threading.Thread(target=personal, args=('https://raw.githubusercontent.com/proxiesmaster/Free-Proxy-List/main/proxies.txt',)).start()
            threading.Thread(target=personal, args=('https://raw.githubusercontent.com/roma8ok/proxy-list/main/proxy-list-http.txt',)).start()
            threading.Thread(target=personal, args=('https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',)).start()
            threading.Thread(target=personal, args=('https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt',)).start()
            threading.Thread(target=personal, args=('https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',)).start()
            threading.Thread(target=personal, args=('https://raw.githubusercontent.com/Volodichev/proxy-list/main/http.txt',)).start()
            threading.Thread(target=personal, args=('https://www.proxy-list.download/api/v1/get?type=http',)).start()
            threading.Thread(target=personal, args=('https://www.proxyscan.io/download?type=http',)).start()





            output()

        if proxy == 'socks':
            threading.Thread(target=scrapeproxies, args=('http://socks-proxy.net',)).start()
            threading.Thread(target=proxyscrapeScraper, args=('socks4','1000','All',)).start()
            threading.Thread(target=proxyscrapeScraper, args=('socks5','1000','All',)).start()
            threading.Thread(target=proxyListDownloadScraper, args=('https://www.proxy-list.download/api/v1/get', 'socks5', 'elite',)).start()
            threading.Thread(target=proxyListDownloadScraper, args=('https://www.proxy-list.download/api/v1/get', 'socks4', 'elite',)).start()
            output()

        if proxy == 'socks4':
            threading.Thread(target=proxyscrapeScraper, args=('socks4','1000','All',)).start()
            threading.Thread(target=proxyListDownloadScraper, args=('https://www.proxy-list.download/api/v1/get', 'socks4', 'elite',)).start()
            output()

        if proxy == 'socks5':
            threading.Thread(target=proxyscrapeScraper, args=('socks5','1000','All',)).start()
            threading.Thread(target=proxyListDownloadScraper, args=('https://www.proxy-list.download/api/v1/get', 'socks5', 'elite',)).start()
            output()
