from sploitkit import Module, Config, Option, Command
import requests
import urllib
import time
import json
import sys
import subprocess
from rich import print
from rich.prompt import Prompt as input

timestamp = time.strftime('%H:%M:%S')
types = ["email", "username", "name", "ip", "password", "uid"]
prefix = "[bold red][[/bold red]-[bold red]][/bold red]"
prefix2 = "[bold red][[/bold red]![bold red]][/bold red]"
prefix3 = f"[bold red][[/bold red]{timestamp}[bold red]][/bold red]"

class photon_spider(Module):
    # Command.set_style("module")
    """Photon Crawler - Uses the python crawler photon to spider a chosen website
    Author: benjibrown
    Version: 1.0.0
    Note: All output is saved to the {path-to-OINTS}/output/photon/ directory
    """
    config = Config({
        Option(
            'TARGET',
            "Target to crawl (with scheme)",
            True,
        ): str("https://example.com"),
    })    
    def query(self):
        target = self.config.option('TARGET').value
        answer = input.ask(f"{prefix2} Do you want to continue with {target} as your target of choice? (y/n) ")
        if answer == "y":
            return
        else:
            raise Exception("Exiting...See ya!")


    def photon(self):
        count = 0
        target = self.config.option('TARGET').value
        print(f"{prefix3} Crawling....")
        scraped = subprocess.run([f"photon", "-u", target, "-e", "json", "-o", "./output/photon/"], capture_output=True)
        with open('output/photon/exported.json', 'r') as data:
            jsondata = json.load(data)
            print(f"{prefix3} Data saved at the output/photon/ directory!")

    def run(self): 
        target = self.config.option('TARGET').value
        self.query()
        self.photon()