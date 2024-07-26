from api.Cli import Cli
from dev.Dev import Dev
from core.TimeKeeper import TimeKeeper

from .BaseCommand import BaseCommand


class Schemas(BaseCommand):
    def execute(self):
        entities = []
        if self.memory.entities is not None:
            for entity in self.memory.entities:
                entities.append(entity["name"])

        if len(entities) == 0:
            self.conversation.cant_no_entities(self.configuration.project.name)
            exit(1)

        time_keeper = TimeKeeper()

        cli = Cli(self.configuration)
        response = cli.code_schemas(entities)

        for entry in response["code"]:
            Dev(self.configuration).schema(entry["entity"]["name"], entry["definition"])

            if self.conversation.muted() is False:
                print(entry["definition"])

        if self.conversation.muted() is False:
            time_keeper.display()
