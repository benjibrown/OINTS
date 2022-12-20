from sploitkit import Module, Config, Option, Command
import requests
from rich import print
import os
from rich.prompt import Prompt as input
import json
import re
import time
timestamp = time.strftime('%H:%M:%S')
types = ["email", "username", "name", "ip", "password", "uid"]
prefix = "[bold red][[/bold red]-[bold red]][/bold red]"
prefix2 = "[bold red][[/bold red]![bold red]][/bold red]"
prefix3 = f"[bold red][[/bold red]{timestamp}[bold red]][/bold red]"
EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
subdomains = []
other = []
class CertSH(Module):
    # Command.set_style("module")
    """Cert.sh Subdomain Finder - Uses cert.sh to find subdomains linked to a given domain
    Author: benjibrown
    Version: 1.0.0
    """
    config = Config({
        Option(
            'TARGET',
            "Target to query cert.sh with",
            True,
        ): str("example.com"),
    })    
    def query(self):
        target = self.config.option('TARGET').value
        answer = input.ask(f"{prefix2} Do you want to continue with {target} as your target of choice? (y/n) ")
        print("\n")
        if answer == "y":
            return
        else:
            raise Exception("Exiting...See ya!")
    def cert(self):
        target = self.config.option('TARGET').value  
        response = requests.get(f"https://crt.sh/?q={target}&output=json")
        content = response.json()
        i = 0
        while i == i:
            try:
                subdomains.append(content[i]['name_value'])
                i=i+1
            except IndexError:
                print(f"{prefix3} Done! Output saved to output/cert.sh/")
                break
        with open("output/cert.sh/temp.txt", "w+") as f:
            for subdomain in subdomains:
                f.write(subdomain + "\n")
        lines_seen = set() # holds lines already seen
        outfile = open("output/cert.sh/subdomains.txt", "w+")
        for line in open("output/cert.sh/temp.txt", "r"):
            if line not in lines_seen: # not a duplicate
                outfile.write(line)
                lines_seen.add(line)
        outfile.close()
        with open("output/cert.sh/subdomains.txt", "r") as f:
            for line in f.readlines():
                print(f"{prefix3} Found {line}", end="")

        os.remove("output/cert.sh/temp.txt")

    def run(self):
        target = self.config.option('TARGET').value
        self.query()
        self.cert()

