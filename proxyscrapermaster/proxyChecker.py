import urllib.request
import threading
import random
import argparse
from time import time, sleep

user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36"

def random_user_agent(file='user_agents.txt'):
	with open(file, "r") as f:
		lines = f.readlines()
		user_agent = random.choice(lines).replace("\n", "")
		f.close()
		sleep(0.1)
	return str(user_agent)

proxyType = ''

def checkproxy(txtfile):
	global out_file
	candidate_proxies = open(txtfile).readlines()
	filedl = open(txtfile, "w")
	filedl.close()
	out_file = open(txtfile, "a")
	threads = []
	for i in candidate_proxies:
		t = threading.Thread(target=checker, args=[i])
		t.start()
		threads.append(t)

	for t in threads:
		t.join()

	out_file.close()
	if args.verbose:
		print("\n\nCurrent IPs in proxylist: %s\n" % (len(open(txtfile).readlines())))


def checker(i):
	proxy = proxyType + '://' + i
	proxy_support = urllib.request.ProxyHandler({proxyType: proxy})
	opener = urllib.request.build_opener(proxy_support)
	urllib.request.install_opener(opener)
	global site
	req = urllib.request.Request(proxyType + '://' + site)
	global user_agent
	if args.random_agent:
		user_agent = random_user_agent()
	req.add_header("User-Agent", user_agent)
	try:
		global chosenTimeout
		start_time = time()
		urllib.request.urlopen(req, timeout=chosenTimeout)
		end_time = time()
		time_taken = end_time - start_time
		out_file.write(i)
		if args.verbose:
			print ("%s works!" % proxy+'\n')
			print('time: ' + str(time_taken)+'\n')
			print('user_agent: ' + user_agent +'\n')
	except Exception as e:
		print(e)
		pass
		if args.verbose:
			print ("%s does not respond.\n" % proxy+'\n')


# Добавление аргументов в парсер
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--timeout", type=int, help="dismiss the proxy after -t seconds", default=20)
parser.add_argument("-p", "--proxy", help="check HTTPS or HTTP proxies", default='http')
parser.add_argument("-l", "--list", help="path to your list.txt", default='output.txt')
parser.add_argument("-s", "--site", help="check with specific website like google.com", default='https://google.com/')
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
parser.add_argument("-r", "--random_agent", help="use a random user agent per proxy", action="store_true")
args = parser.parse_args() # Получение всех аргументов
txtfile = args.list # list.txt
site = args.site # Сайт указанный пользователем (default="https://google.com/")
proxyType = args.proxy # Какие прокси парсить (default="http")
chosenTimeout = args.timeout
threading.Thread(target=checkproxy, args=(txtfile,)).start() # старт
