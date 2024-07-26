import os
import shutil

from core.Configuration import Configuration
from services.code.customization.CustomizationManager import CustomizationManager
from core.TimeKeeper import TimeKeeper

from .Api import Api
from .Base import Base
from .BaseCommand import BaseCommand
from .Models import Models
from .Schemas import Schemas
from .Tests import Tests


class Rewrite(BaseCommand):
    def __init__(
        self,
        configuration: Configuration,
        header="Writing Code",
        wipe=True,
        with_header=False,
    ):
        super().__init__(configuration)
        self.wipe = wipe
        self.with_header = with_header

    def execute(self):
        if self.with_header is True:
            self.conversation.display_project(self.configuration.project.name)

        customization_manager = CustomizationManager(self.configuration).preserve()

        try:
            if self.wipe is True:
                for root, dirs, files in os.walk(
                    os.path.expandvars(self.configuration.project.dev.base.path)
                ):
                    for file in files:
                        os.unlink(os.path.join(root, file))

                    for dir_ in dirs:
                        shutil.rmtree(os.path.join(root, dir_))

            self.conversation.type("Writing Code\n")

            time_keeper = TimeKeeper()

            self.conversation.type("  API      ")

            self.conversation.mute()
            Api(self.configuration).disable_customization_management().execute()
            self.conversation.unmute()

            self.conversation.type(time_keeper.get_display())
            self.conversation.newline()

            time_keeper = TimeKeeper()

            self.conversation.type("  Base     ")

            self.conversation.mute()
            Base(self.configuration).execute()
            self.conversation.unmute()

            self.conversation.type(time_keeper.get_display())
            self.conversation.newline()

            time_keeper = TimeKeeper()

            self.conversation.type("  Models   ")

            self.conversation.mute()
            Models(self.configuration).execute()
            self.conversation.unmute()

            self.conversation.type(time_keeper.get_display())
            self.conversation.newline()

            time_keeper = TimeKeeper()

            self.conversation.type("  Schemas  ")

            self.conversation.mute()
            Schemas(self.configuration).execute()
            self.conversation.unmute()

            self.conversation.type(time_keeper.get_display())
            self.conversation.newline()

            time_keeper = TimeKeeper()

            self.conversation.type("  Tests    ")

            self.conversation.mute()
            Tests(self.configuration).execute()
            self.conversation.unmute()

            self.conversation.type(time_keeper.get_display())
            self.conversation.newline()
        finally:
            customization_manager.restore()

        if self.with_header is True:
            self.conversation.newline()

        return self
