import sys

from api.Cli import Cli
from dev.Dev import Dev
from core.TimeKeeper import TimeKeeper

from .BaseCommand import BaseCommand


class Model(BaseCommand):
    def execute(self):
        if len(sys.argv) != 3:
            self.usage()

        entity = self.memory.recall_stored_entity(sys.argv[2])
        if entity is None:
            self.conversation.not_sure_no_entity(
                self.configuration.project.name, sys.argv[2]
            )
            exit(1)

        time_keeper = TimeKeeper()

        cli = Cli(self.configuration)
        response = cli.code_models([entity["name"]])

        Dev(self.configuration).model(
            response["code"][0]["entity"]["name"], response["code"][0]["definition"]
        )

        print(response["code"][0]["definition"])
        time_keeper.display()

    def usage(self):
        self.conversation.display_project(self.configuration.project.name)
        self.conversation.type(
            f"usage: {self.configuration.command} model [entity name]\n"
            + "  where [entity name] is one of the entities that exists "
            + "in this project\n"
        )
        self.conversation.newline()
        exit(1)
