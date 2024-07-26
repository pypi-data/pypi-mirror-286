from .Configuration import Configuration
from lang.Python import Python


class Env:
    def verify(self, configuration: Configuration):
        if configuration.project.code.language == "python":
            Python().make_import_path(configuration.project.dev.base.path)
        else:
            raise RuntimeError(
                f'unrecognized language "{configuration.project.code.language}"'
            )
