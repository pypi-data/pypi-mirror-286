#!/usr/bin/env python3

from core.CommandRouter import CommandRouter
from core.Configuration import Configuration


def main():
    configuration = Configuration()
    if configuration.settings is None:
        configuration.initialize()
    else:
        router = CommandRouter(configuration).run()


if __name__ == "__main__":
    main()
