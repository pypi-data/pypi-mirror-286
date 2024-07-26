from core.Configuration import Configuration


class BaseCustomization:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration

    def preserve(self):
        raise NotImplementedError

    def restore(self):
        raise NotImplementedError
