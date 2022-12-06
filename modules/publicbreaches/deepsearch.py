from sploitkit import Module, Config, Option, Command
import requests
import re
import sys
import rich
from rich import print
from rich.prompt import Prompt as input
types = ["email", "username", "name", "ip", "password", "uid"]
prefix = "[bold red][[/bold red]-[bold red]][/bold red]"
EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
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
    })    
    def query(self):
        type = self.config.option('TYPE').value
        target = self.config.option('TARGET').value
        answer = input.ask(f"{prefix} Do you want to continue with {target} as your {type} of choice? (y/n) ")
        if answer == "y":
            return
        else:
            print(f'{prefix} Exiting....See ya!')
            return None

    def run(self):
        type = self.config.option('TYPE').value
        target = self.config.option('TARGET').value
        if type not in types:
            print(f'{prefix} Please provide a valid TYPE!')
        if type == "email":
            if not EMAIL_REGEX.match(target):
                print(f'{prefix} Please provide a valid email!')
                return None
        self.query()
