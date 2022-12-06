from sploitkit import Module, Config, Option, Command
import requests

class deepSearch(Module):
    # Command.set_style("module")
    """Deepsearch - Searches DeepSearch for given IP/Email/Password/Name/UID/Username
    Author: benjibrown
    Version: 1.0.0
    """
    config = Config({
        Option(
            'TYPE',
            "Select a type, can be one of 4 - name, password, email, ip, uid, username",
            True,
        ): str("email"),
    })    

    def run(self):
        string = self.config.option('TYPE').value
        if string == "email":
            print("trolled")