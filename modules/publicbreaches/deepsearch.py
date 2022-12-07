import re
import sys
import bs4
import time
import json
import rich
import requests
from rich import print
from bs4 import BeautifulSoup
from requests import ConnectionError
from rich.prompt import Prompt as input
from sploitkit import Module, Config, Option, Command
# required definitions
timestamp = time.strftime('%H:%M:%S')
types = ["email", "username", "name", "ip", "password", "uid"]
prefix = "[bold red][[/bold red]-[bold red]][/bold red]"
prefix2 = "[bold red][[/bold red]![bold red]][/bold red]"
prefix3 = f"[bold red][[/bold red]{timestamp}[bold red]][/bold red]"
EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
IP_REGEX = re.compile(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$")
class deepSearch(Module):
    # Command.set_style("module")
    """Deepsearch - Searches DeepSearch for given IP/Email/Password/Name/UID/Username
    Author: benjibrown
    Version: 1.0.0
    """
    config = Config({
        Option(
            'TYPE',
            "Select a type, can be one of 6 - name, password, email, ip, uid, username",
            True,
        ): str("email"),
        Option(
            'TARGET',
            "Must be an IP, Email, Password, Username, Name or UID",
            True,
        ): str("example@example.com"),
        Option(
            'PHPSESSID',
            "Must be a valid PHP session ID, collect from DeepSearch website after logging in",
            True,
        ): str("bmljZSBqb2Igb24gZmluZGluZyB0aGlzIQ"),
        Option(
            'TOR_PORT',
            "Port in which Tor instance is running",
            True,
        ): str("9050"),
        Option(
            'TOR_HOST',
            "Host in which Tor instance is running",
            True,
        ): str("127.0.0.1"),
        Option(
            'DEEPSEARCH_URI',
            "Deepsearch .onion link - Only change if Deepsearch URI has changed",
            False,
        ): str("http://xjypo5vzgmo7jca6b322dnqbsdnp3amd24ybx26x5nxbusccjkm4pwid.onion/deepsearch"),
    })    
    def query(self):
        #variables
        type = self.config.option('TYPE').value.lower()
        target = self.config.option('TARGET').value.lower()
        tor_port = self.config.option('TOR_PORT').value
        tor_host = self.config.option('TOR_HOST').value
        # query
        answer = input.ask(f"{prefix2} Do you want to continue with {target} as your {type} of choice and {tor_port}, {tor_host} as your TOR config? (y/n) ")
        if answer == "y":
            return
        else:
            print(f'{prefix2} Exiting....See ya!')
            return None
    def search(self):
        #variables
        search = self.config.option('TARGET').value
        search_type = self.config.option('TYPE').value
        phpsessid = self.config.option('PHPSESSID').value
        uri = self.config.option('DEEPSEARCH_URI').value
        tor_host = self.config.option('TOR_HOST').value
        tor_port = self.config.option('TOR_PORT').value
        session = requests.session()
        #set proxies
        session.proxies = {'http': f'socks5h://{tor_host}:{tor_port}', 'https': f'socks5h://{tor_host}:{tor_port}'}
        # send request
        print(f"{prefix3} Scraping data.....")
        request_data = {'search': search, 'dropdownn': search_type, 'tsearchv': 'match'}
        response = session.post(uri, data=request_data, cookies={'PHPSESSID':phpsessid})
        # run parsing function
        print(f"{prefix3} Parsing response.....")
        html = response.text
        soup = BeautifulSoup(html, "lxml")

        td = soup.find_all('td')

        i = 0
        while i < len(td):
            first_item  = td[i].getText()
            second_item = td[i+1].getText()  
            
            if '/20' in first_item:
                print("---------------------------------------------------")
            
            print(f"{prefix3} {first_item}:\t {second_item}")
            i += 2
        return None
    def run(self):
        #variables
        type = self.config.option('TYPE').value.lower()
        target = self.config.option('TARGET').value.lower()
        tor_port = self.config.option('TOR_PORT').value
        tor_host = self.config.option('TOR_HOST').value
        phpsessid = self.config.option('PHPSESSID').value.lower()
        # validate input
        if type not in types:
            print(f'{prefix2} Please provide a valid TYPE!')
        if type == "email":
            if not EMAIL_REGEX.match(target):
                print(f'{prefix2} Please provide a valid email!')
                return None
        if type == "ip":
            if not IP_REGEX.match(target):
                print(f'{prefix2} Please provide a valid IP!')
                return None
        if tor_port >= 65535 or tor_port <= 0:
            print(f'{prefix2} Please provide a valid TOR PORT!')
            return None
        if not IP_REGEX.match(tor_host):
            print(f'{prefix2} Please provide a valid TOR HOST!')
            return None
        if phpsessid == "bmljZSBqb2Igb24gZmluZGluZyB0aGlzIQ":
            print(f'{prefix2} Please provide a PHPSESSID - You selected the example one!')
            return None
            
        self.query()
        #init session

        # run search function
        self.search()