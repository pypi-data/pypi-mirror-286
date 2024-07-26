import os
import re
import sys

from api.Cli import Cli

from .BaseCommand import BaseCommand


class New(BaseCommand):
    def execute(self):
        if len(sys.argv) != 3:
            self.usage()

        if sys.argv[2] != "project":
            self.usage()

        self.conversation.new_project(self.configuration)
        project_name = self.conversation.prompt_project()
        if project_name in self.configuration.settings:
            self.conversation.project_already_exists(project_name)
            exit(1)

        project_description = self.conversation.prompt_description(project_name)

        self.configuration.set_project_env(project_name)
        self.configuration.append_project_to_conf(project_name, project_description)

        self.conversation.configure_new_project(self.configuration)

    def usage(self):
        self.conversation.display_project(self.configuration.project.name)
        self.conversation.type(
            f"usage: {self.configuration.command} new [thing]\n"
            + '  where [thing] can only be "project", for now\n'
        )
        self.conversation.newline()
        exit(1)
