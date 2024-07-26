import sys

from api.Cli import Cli

from .BaseCommand import BaseCommand


class List(BaseCommand):
    def execute(self):
        if len(sys.argv) != 3:
            self.usage()

        self.conversation.display_project(self.configuration.project.name)

        entities = {"last": [], "stored": []}

        last = self.memory.recall_last()
        if last is not None:
            for entity in last["entities"]:
                entities["last"].append(entity["name"])

        stored = self.memory.recall_entities()
        if stored is not None:
            for entity in stored:
                entities["stored"].append(entity["name"])

        if len(entities["last"]) == 0 and len(entities["stored"]) == 0:
            self.conversation.nothing_to_list(sys.argv[2])
            self.conversation.newline()
        else:
            self.conversation.type("    Name".ljust(60), delay=0.0001)
            self.conversation.type("Memory", delay=0.002)
            self.conversation.newline()
            self.conversation.type("    ----".ljust(60), delay=0.0001)
            self.conversation.type("------", delay=0.002)
            self.conversation.newline()

            entities["last"].sort()
            entities["stored"].sort()

            if len(entities["stored"]) > 0:
                for entity in entities["stored"]:
                    self.conversation.type(f"    {entity}".ljust(60), delay=0.0001)
                    self.conversation.type("[stored]", delay=0.002)
                    self.conversation.newline()

                self.conversation.newline()

            if len(entities["last"]) > 0:
                for entity in entities["last"]:
                    self.conversation.type(f"    {entity}".ljust(60), delay=0.0001)
                    self.conversation.type("[last]", delay=0.002)
                    self.conversation.newline()

                self.conversation.newline()

    def usage(self):
        self.conversation.display_project(self.configuration.project.name)
        self.conversation.type(f"usage: {self.configuration.command} list entities\n")
        self.conversation.newline()
        exit(1)
