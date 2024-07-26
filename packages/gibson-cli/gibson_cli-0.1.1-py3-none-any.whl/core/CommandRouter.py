import sys

from command.Api import Api
from command.auth.Auth import Auth
from command.Base import Base
from command.Build import Build
from command.Code import Code
from command.Conf import Conf
from command.Count import Count
from command.Dev import Dev
from command.Forget import Forget
from command.Import import Import
from command.List import List
from command.Merge import Merge
from command.Model import Model
from command.Models import Models
from command.Modify import Modify
from command.Module import Module
from command.New import New
from command.OpenApi import OpenApi
from command.Question import Question
from command.Remove import Remove
from command.Rename import Rename
from command.Rewrite import Rewrite
from command.Schema import Schema
from command.Schemas import Schemas
from command.Show import Show
from command.Test import Test
from command.Tests import Tests
from command.Tree import Tree
from command.WarGames import WarGames
from .Configuration import Configuration
from .Conversation import Conversation
from .Env import Env
from .Memory import Memory


class CommandRouter:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.conversation = Conversation()

    def help(self, exit_code=0):
        dev_off = "*"
        dev_on = ""
        if self.configuration.project.dev.active is True:
            dev_off = ""
            dev_on = "*"

        commands = {
            "api": {
                "description": "write the API code for the project",
                "memory": "stored",
            },
            "auth": {
                "description": "login | logout",
                "memory": None,
            },
            "base": {
                "description": "write the base code for the project",
                "memory": "stored",
            },
            "build": {
                "description": "create the entities in the datastore",
                "memory": "stored",
            },
            "code": {"description": "pair program", "memory": None},
            "conf": {"description": "set a configuration variable", "memory": None},
            "count": {
                "description": "show the number of entities stored",
                "memory": "last | stored",
            },
            "dev": {
                "description": f"mode off{dev_off} | on{dev_on}",
                "memory": None,
            },
            "forget": {
                "description": "delete memory",
                "memory": "all | last | stored",
            },
            "help": {"description": "for help", "memory": None},
            "import": {
                "description": "configure from a data source",
                "memory": "stored",
            },
            "list": {
                "description": "show the names of entities in your project",
                "memory": None,
            },
            "merge": {
                "description": "move last changes into project",
                "memory": "last -> stored",
            },
            "model": {
                "description": "write the model code for an entity",
                "memory": "stored",
            },
            "models": {
                "description": "write all the model code",
                "memory": "stored",
            },
            "modify": {
                "description": "change an entity using natural language",
                "memory": "last > stored",
            },
            "module": {"description": "create a new module", "memory": "last"},
            "new": {"description": "start something new", "memory": None},
            "openapi": {"description": "build from an OpenAPI spec", "memory": "last"},
            "remove": {
                "description": "remove an entity from the project",
                "memory": "last > stored",
            },
            "rename": {
                "description": "rename an entity",
                "memory": "last > stored",
            },
            "rewrite": {
                "description": "rewrite all code from scratch",
                "memory": "stored",
            },
            "schema": {
                "description": "write the schema code for an entity",
                "memory": "stored",
            },
            "schemas": {
                "description": "write all the schema code",
                "memory": "stored",
            },
            "show": {"description": "display an entity", "memory": "last > stored"},
            "test": {
                "description": "write the unit tests for an entity",
                "memory": "stored",
            },
            "tests": {
                "description": "write all the unit tests",
                "memory": "stored",
            },
            "tree": {"description": "illustrate the project layout", "memory": None},
            "? | q": {"description": "ask a question", "memory": None},
        }

        self.conversation.set_delay(0.001)
        self.conversation.display_project(self.configuration.project.name)
        self.conversation.type(f"usage: {self.configuration.command} [command]\n\n")
        self.conversation.type(" command  description" + " " * 40 + "memory\n")
        self.conversation.type(" -------  -----------" + " " * 40 + "------\n")

        for command, config in commands.items():
            memory = ""
            if config["memory"] is not None:
                memory = f"[{config['memory']}]"

            spaces = 61 - (8 + 2 + len(config["description"]))

            self.conversation.type(
                f"{command.rjust(8)}"
                + f"  {config['description']}"
                + " " * spaces
                + f"{memory}\n"
            )

        self.conversation.newline()
        self.conversation.type("memory:\n\n")

        stats = Memory(self.configuration).stats()
        self.conversation.type(
            f"{str(stats['entities']['num']).rjust(8)}"
            + f"  {stats['entities']['word']}"
            + " " * (43 if stats["entities"]["word"] == "entities" else 45)
            + "[stored]\n"
        )
        self.conversation.type(
            f"{str(stats['last']['num']).rjust(8)}"
            + f"  {stats['last']['word']}"
            + " " * (43 if stats["last"]["word"] == "entities" else 45)
            + "[last]\n\n"
        )

        exit(exit_code)

    def run(self):
        if len(sys.argv) == 1 or sys.argv[1] == "help":
            self.help()
            return self

        Env().verify(self.configuration)

        command = None
        if sys.argv[1] == "api":
            command = Api(self.configuration)
        elif sys.argv[1] == "auth":
            command = Auth(self.configuration)
        elif sys.argv[1] == "base":
            command = Base(self.configuration)
        elif sys.argv[1] == "build":
            command = Build(self.configuration)
        elif sys.argv[1] == "code":
            command = Code(self.configuration)
        elif sys.argv[1] == "conf":
            command = Conf(self.configuration)
        elif sys.argv[1] == "count":
            command = Count(self.configuration)
        elif sys.argv[1] == "dev":
            command = Dev(self.configuration)
        elif sys.argv[1] == "forget":
            command = Forget(self.configuration)
        elif sys.argv[1] == "import":
            command = Import(self.configuration)
        elif sys.argv[1] == "list":
            command = List(self.configuration)
        elif sys.argv[1] == "merge":
            command = Merge(self.configuration)
        elif sys.argv[1] == "model":
            command = Model(self.configuration)
        elif sys.argv[1] == "models":
            command = Models(self.configuration)
        elif sys.argv[1] == "modify":
            command = Modify(self.configuration)
        elif sys.argv[1] == "module":
            command = Module(self.configuration)
        elif sys.argv[1] == "new":
            command = New(self.configuration)
        elif sys.argv[1] == "openapi":
            command = OpenApi(self.configuration)
        elif sys.argv[1] == "remove":
            command = Remove(self.configuration)
        elif sys.argv[1] == "rename":
            command = Rename(self.configuration)
        elif sys.argv[1] == "rewrite":
            command = Rewrite(self.configuration, with_header=True)
        elif sys.argv[1] == "schema":
            command = Schema(self.configuration)
        elif sys.argv[1] == "schemas":
            command = Schemas(self.configuration)
        elif sys.argv[1] == "show":
            command = Show(self.configuration)
        elif sys.argv[1] == "test":
            command = Test(self.configuration)
        elif sys.argv[1] == "tests":
            command = Tests(self.configuration)
        elif sys.argv[1] == "tree":
            command = Tree(self.configuration)
        elif sys.argv[1] in ["?", "q"]:
            command = Question(self.configuration)
        else:
            command = WarGames(self.configuration)

        if command is None or command.execute() is False:
            self.help(exit_code=1)
