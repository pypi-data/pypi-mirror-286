import sys

from api.Cli import Cli

from .BaseCommand import BaseCommand


class Modify(BaseCommand):
    def execute(self):
        if len(sys.argv) < 4:
            self.usage()

        entity = self.memory.recall_entity(sys.argv[2])
        if entity is None:
            self.conversation.not_sure_no_entity(
                self.configuration.project.name, sys.argv[2]
            )
            exit(1)

        cli = Cli(self.configuration)

        response = cli.modeler_entity_modify(
            self.configuration.project.modeler.version,
            self.configuration.project.description,
            entity,
            " ".join(sys.argv[3:]),
        )

        self.memory.remember_last(response)

        print(response["entities"][0]["definition"])

    def usage(self):
        self.conversation.display_project(self.configuration.project.name)
        self.conversation.type(
            f"usage: {self.configuration.command} "
            + "modify [entity name] [instructions]\n"
            + "  where [entity name] is one of the entities that exists in "
            + "this project\n"
            + "  and [instructions] is natural language describing the changes\n"
        )
        self.conversation.newline()
        exit(1)
