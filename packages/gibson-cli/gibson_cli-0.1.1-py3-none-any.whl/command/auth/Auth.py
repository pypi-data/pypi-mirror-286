import sys

from ..BaseCommand import BaseCommand
from .Login import Login
from .Logout import Logout


class Auth(BaseCommand):
    def execute(self):
        if len(sys.argv) != 3:
            self.usage()
        elif sys.argv[2] == "login":
            Login(self.configuration).execute()
        elif sys.argv[2] == "logout":
            Logout(self.configuration).execute()
        else:
            self.usage()

    def usage(self):
        self.conversation.type(
            f"usage: {self.configuration.command} auth login\n"
            + f"   or: {self.configuration.command} auth logout\n"
        )
        self.conversation.newline()
        exit(1)
