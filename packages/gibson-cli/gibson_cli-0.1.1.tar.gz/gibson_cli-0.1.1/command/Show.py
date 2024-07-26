import sys

from .BaseCommand import BaseCommand


class Show(BaseCommand):
    def execute(self):
        if len(sys.argv) == 2:
            entities = self.memory.recall_merged()
            if entities is None:
                self.conversation.cant_no_entities(self.configuration.project.name)
                exit(1)
        elif len(sys.argv) == 3:
            entity = self.memory.recall_entity(sys.argv[2])
            if entity is None:
                self.conversation.not_sure_no_entity(
                    self.configuration.project.name, sys.argv[2]
                )
                exit(1)

            entities = [entity]
        else:
            self.usage()

        for entity in entities:
            print(entity["definition"])

    def usage(self):
        self.conversation.display_project(self.configuration.project.name)
        self.conversation.type(
            f"usage: {self.configuration.command} show {{entity name}}\n"
            + "  where {entity name} is one of the entities that exists in "
            + "this project\n"
            + "  omitting {entity name} displays all entities\n"
        )
        self.conversation.newline()
        exit(1)
