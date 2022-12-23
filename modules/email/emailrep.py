from sploitkit import Module, Config, Option, Command
import requests
import re
import time
import sys
from rich import print
from rich.prompt import Prompt as input
timestamp = time.strftime('%H:%M:%S')
types = ["email", "username", "name", "ip", "password", "uid"]
prefix = "[bold red][[/bold red]-[bold red]][/bold red]"
prefix2 = "[bold red][[/bold red]![bold red]][/bold red]"
prefix3 = f"[bold red][[/bold red]{timestamp}[bold red]][/bold red]"
EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
class emailRep(Module):
    # Command.set_style("module")
    """ EmailRep - Searches emailrep.io for the reputation of the specified email
    Note: IF you are ratelimited run the program through tor using proxychains
    Author: benjibrown
    Version: 1.0.0
    """
    config = Config({
        Option(
            'EMAIL',
            "Email to scan",
            True,
        ): str("example@example.com"),
        Option(
            'RAW',
            "Output raw data (y/n)",
            False,
        ): str("n"),
    })    
    def query(self):
        #variables
        email = self.config.option('EMAIL').value
        # query
        answer = input.ask(f"{prefix2} Do you want to continue with {email} as the email to scan? (y/n) ")
        if answer == "y":
            return
        else:
            raise Exception("Exiting...See ya!")
    # def search(self):
    #     email = self.config.option("EMAIL").value
    #     raw = self.config.option('RAW').value.lower()
    #     r = requests.get(f"https://emailrep.io/{email}")
    #     jsonresp = r.json()
    #     if raw == "n":
    #         if "fail" and "reason" in jsonresp:
    #             print(f'{prefix3} You have been ratelimited by the API!')
    #         for key,value in jsonresp.items():
    #             if key == "details":
    #                 ff = jsonresp["details"]
    #                 for key,value in ff.items():
    #                     print(f"{prefix3} {key.title()}: {value}")
    #                 return None
    #             print(f"{prefix3} {key.title()}: {value}")
    #     elif raw == "y":
    #         print(jsonresp)
    #     else:
    #         print(f"{prefix2} Invalid raw value! Exiting....See ya!")
    #         raise Exception("Exiting...See ya!")

    def run(self):
        email = self.config.option('EMAIL').value
        raw = self.config.option('RAW').value
        self.query()
        r = requests.get(f"https://emailrep.io/{email}")
        jsonresp = r.json()
        if "n" in raw:
            if "fail" and "reason" in jsonresp:
                print(f'{prefix3} You have been ratelimited by the API!')
            for key,value in jsonresp.items():
                if key == "details":
                    ff = jsonresp["details"]
                    for key,value in ff.items():
                        print(f"{prefix3} {key.title()}: {value}")
                    return None
                print(f"{prefix3} {key.title()}: {value}")
        elif "y" in raw:
            print(jsonresp)
        else:
            print(f"{prefix2} Invalid raw value! Exiting....See ya!")
            raise Exception("Exiting...See ya!")
        