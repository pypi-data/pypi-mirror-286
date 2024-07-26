from api.Cli import Cli

from ..BaseCommand import BaseCommand


class Login(BaseCommand):
    def execute(self):
        cli = Cli(self.configuration)
        token = cli.login()

        if token is None:
            self.conversation.newline()
            self.conversation.type(
                "Login failed, please try again with `gibson auth login`."
            )
        else:
            self.configuration.set_access_token(token)
            self.conversation.type(f"Welcome! You are now logged in.")

        self.conversation.newline()
