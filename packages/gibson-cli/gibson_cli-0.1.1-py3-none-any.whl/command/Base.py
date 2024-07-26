from api.Cli import Cli
from dev.Dev import Dev
from core.TimeKeeper import TimeKeeper

from .BaseCommand import BaseCommand


class Base(BaseCommand):
    def execute(self):
        entities = self.memory.recall_merged()
        if len(entities) == 0:
            self.conversation.cant_no_entities(self.configuration.project.name)
            exit(1)

        time_keeper = TimeKeeper()
        dev = Dev(self.configuration)

        cli = Cli(self.configuration)
        response = cli.code_base()

        for entry in response["code"]:
            dev.base_component(entry["name"], entry["definition"])

            if self.conversation.muted() is False:
                print(entry["definition"])

        if self.conversation.muted() is False:
            time_keeper.display()
