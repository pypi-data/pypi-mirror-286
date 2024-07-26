import sys

from api.Cli import Cli

from .BaseCommand import BaseCommand
from .Rewrite import Rewrite


class Remove(BaseCommand):
    def execute(self):
        if len(sys.argv) != 3:
            self.usage()

        self.conversation.display_project(self.configuration.project.name)

        found = False

        last = self.memory.recall_last()
        if last is not None:
            entities = []
            for entity in last["entities"]:
                if entity["name"] == sys.argv[2]:
                    found = True
                else:
                    entities.append(entity)

            if found:
                if len(entities) == 0:
                    self.memory.forget_last()
                else:
                    self.memory.remember_last({"entities": entities})

                self.conversation.type(f"[Removed] {sys.argv[2]}\n")
                self.conversation.newline()

                return self

        cli = Cli(self.configuration)
        entities = []

        stored = self.memory.recall_entities()
        if stored is not None and len(stored) > 0:
            for entity in stored:
                entities.append(entity)
                if entity["name"] == sys.argv[2]:
                    found = True

        if not found:
            self.conversation.type(
                f'Nothing removed, did not find entity named "{sys.argv[2]}".\n'
            )
            self.conversation.newline()
            return self

        response = cli.modeler_entity_remove(
            self.configuration.project.modeler.version, entities, sys.argv[2]
        )

        if len(response["entities"]) == 0:
            self.memory.forget_stored()
        else:
            self.memory.remember_entities(response["entities"])

        self.conversation.type(f"[Removed] {sys.argv[2]}\n")
        self.conversation.newline()

        Rewrite(self.configuration, header="Refactoring").execute()

        self.conversation.newline()

        return self

    def usage(self):
        self.conversation.display_project(self.configuration.project.name)
        self.conversation.type(
            f"usage: {self.configuration.command} remove [entity name]\n"
            + "  where [entity name] is one of the entities that exists in this project\n"
        )
        self.conversation.newline()
        exit(1)
