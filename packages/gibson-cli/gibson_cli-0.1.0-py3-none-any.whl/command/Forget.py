import sys

from .BaseCommand import BaseCommand


class Forget(BaseCommand):
    def execute(self):
        if len(sys.argv) != 3 or sys.argv[2] not in ["all", "last", "stored"]:
            self.usage()

        if sys.argv[2] == "all":
            self.memory.forget_last()
            self.memory.forget_entities()
        elif sys.argv[2] == "last":
            self.memory.forget_last()
        elif sys.argv[2] == "stored":
            self.memory.forget_entities()
        else:
            raise NotImplementedError

        self.conversation.display_project(self.configuration.project.name)
        self.conversation.type("Yeah man, forgotten.\n")
        self.conversation.newline()

        return self

    def usage(self):
        self.conversation.display_project(self.configuration.project.name)
        self.conversation.type(
            f"usage: {self.configuration.command} forget [which memory]\n"
            + '  where [which memory] is one of "all", "last" or "stored"\n'
        )
        self.conversation.newline()
        exit(1)
