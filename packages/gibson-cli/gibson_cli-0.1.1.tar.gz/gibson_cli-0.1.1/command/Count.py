import sys

from .BaseCommand import BaseCommand


class Count(BaseCommand):
    def execute(self):
        if len(sys.argv) != 3 or sys.argv[2] not in ["last", "stored"]:
            self.usage()

        if sys.argv[2] == "last":
            count = 0
            if self.memory.last is not None:
                count = len(self.memory.last["entities"])

            print(count)
        elif sys.argv[2] == "stored":
            count = 0
            if self.memory.entities is not None:
                count = len(self.memory.entities)

            print(count)
        else:
            raise NotImplementedError

        return self

    def usage(self):
        self.conversation.display_project(self.configuration.project.name)
        self.conversation.type(
            f"usage: {self.configuration.command} count [which memory]\n"
            + '  where [which memory] is one of "last" or "stored"\n'
        )
        self.conversation.newline()
        exit(1)
