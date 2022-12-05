from sploitkit import Module, Config, Option, Command
import requests

class dnsHost(Module):
    # Command.set_style("module")
    """ Test module
    Author: benjibrown
    Version: 1.0.0
    """
    config = Config({
        Option(
            'STRING',
            "Test echo",
            True,
        ): str("Hello World!"),
    })    

    def run(self):
        string = self.config.option('STRING').value
        print(string)

