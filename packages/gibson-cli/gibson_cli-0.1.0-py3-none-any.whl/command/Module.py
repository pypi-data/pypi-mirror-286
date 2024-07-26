import re
import sys

from api.Cli import Cli

from .BaseCommand import BaseCommand


class Module(BaseCommand):
    def execute(self):
        if len(sys.argv) != 3:
            self.usage()

        if not re.search("^[a-z0-9]+$", sys.argv[2]):
            self.conversation.display_project(self.configuration.project.name)
            self.conversation.type("[module name] should only contain ^[a-z0-9]+$.\n\n")
            return True

        cli = Cli(self.configuration)

        response = cli.modeler_module(
            self.configuration.project.modeler.version,
            self.configuration.project.description,
            sys.argv[2],
        )

        self.memory.remember_last(response)

        for entity in response["entities"]:
            print(entity["definition"])
            self.conversation.newline()

    def usage(self):
        self.conversation.display_project(self.configuration.project.name)
        self.conversation.type(
            f"usage: {self.configuration.command} module [module name]\n"
            + "  where [module name] is the name of the module I should create for "
            + "this project\n"
            + "  [module name] ~ ^[a-z0-9]+$\n"
        )
        self.conversation.newline()
        exit(1)
