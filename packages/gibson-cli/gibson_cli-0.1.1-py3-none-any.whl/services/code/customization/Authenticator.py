import os

from core.Configuration import Configuration
from services.code.customization.BaseCustomization import BaseCustomization


class Authenticator(BaseCustomization):
    def __init__(self, configuration: Configuration):
        super().__init__(configuration)
        self.__link_target = None
        self.__file_contents = None

    def __get_file_name(self):
        return (
            self.configuration.project.dev.api.path
            + "/"
            + self.configuration.project.dev.api.version
            + "/Authenticator.py"
        )

    def preserve(self):
        authenticator_file_name = self.__get_file_name()

        if os.path.islink(authenticator_file_name):
            self.__link_target = os.readlink(authenticator_file_name)
        elif os.path.isfile(authenticator_file_name):
            with open(authenticator_file_name, "r") as f:
                self.__file_contents = f.read()

        return self

    def restore(self):
        authenticator_file_name = self.__get_file_name()

        if self.__link_target is not None:
            try:
                os.unlink(authenticator_file_name)
            except FileNotFoundError:
                pass

            os.symlink(self.__link_target, authenticator_file_name)
        elif self.__file_contents is not None:
            try:
                os.unlink(authenticator_file_name)
            except FileNotFoundError:
                pass

            with open(authenticator_file_name, "w") as f:
                f.write(self.__file_contents)

        return self
