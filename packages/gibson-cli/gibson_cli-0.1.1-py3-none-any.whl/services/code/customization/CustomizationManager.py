from core.Configuration import Configuration
from services.code.customization.Authenticator import Authenticator


class CustomizationManager:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.customizations = [Authenticator(self.configuration)]

    def preserve(self):
        for customization in self.customizations:
            customization.preserve()

        return self

    def restore(self):
        for customization in self.customizations:
            customization.restore()

        return self
