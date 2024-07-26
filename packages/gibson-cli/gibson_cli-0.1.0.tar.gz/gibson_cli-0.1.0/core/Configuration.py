import errno
import json
import os
import shutil
import sys
import time

from conf.Dependencies import Dependencies
from conf.dev.Api import Api
from conf.dev.Base import Base
from conf.dev.Model import Model
from conf.dev.Schema import Schema
from conf.Platform import Platform
from conf.Project import Project
from conf.Paths import ConfigPaths
from .Conversation import Conversation


class Configuration:
    VERSION = 2
    API_ENV = os.environ.get("GIBSONAI_API_ENV", "staging")

    def __init__(self):
        self.command = None
        if len(sys.argv) >= 1:
            self.command = sys.argv[0].split("/")[-1]

        self.conversation = Conversation()
        self.platform = Platform()
        self.project = Project()
        self.paths = ConfigPaths()
        self.settings = None

        self.__check_configuration_path()

        self.set_config_paths()
        self.__check_for_configuration_migration()

        self.read_config()

    def append_project_to_conf(self, project_name, project_description):
        self.project.api.key = "FIXME"
        self.project.name = project_name
        self.project.datastore.type = "mysql"
        self.project.datastore.uri = "mysql+pymysql://user:password@host/database_name"
        self.project.description = project_description

        dependencies = Dependencies().compute()

        section = f""""{self.project.name}": {{
    "api": {{
        "key": "{self.project.api.key}"
    }},
    "code": {{
        "custom": {{
            "model": {{
                "class": None,
                "path": None
            }}
        }},
        "frameworks": {{
            "api": "{dependencies.api}",
            "model": "{dependencies.model}",
            "revision": "{dependencies.revision}",
            "schema": "{dependencies.schema}",
            "test": "{dependencies.test}",
        }},
        "language": "python"
    }},
    "datastore": {{
        "type": "{self.project.datastore.type}",
        "uri": "{self.project.datastore.uri}"
    }},
    "dev": {{
        "active": False,
        "api": {{
            "path": None,
            "prefix": "-",
            "version": "v1"
        }},
        "base": {{
            "path": None
        }},
        "model": {{
            "path": None
        }},
        "schema": {{
            "path": None
        }}
    }},
    "meta": {{
        "project": {{
            "description": "{self.project.description}"
        }},
        "version": {self.VERSION}
    }},
    "modeler": {{
        "version": "generic-v7"
    }}
}}"""

        if self.settings is None:
            self.settings = {}

        self.settings[self.project.name] = {
            "api": {"key": self.project.api.key},
            "code": {
                "custom": {"model": {"class": None, "path": None}},
                "frameworks": {
                    "api": dependencies.api,
                    "model": dependencies.model,
                    "revision": dependencies.revision,
                    "schema": dependencies.schema,
                    "test": dependencies.test,
                },
                "language": "python",
            },
            "datastore": {
                "type": self.project.datastore.type,
                "uri": self.project.datastore.uri,
            },
            "dev": {
                "active": False,
                "api": {"path": None, "prefix": "-", "version": "v1"},
                "base": {"path": None},
                "model": {
                    "path": None,
                },
                "schema": {"path": None},
            },
            "meta": {
                "project": {"description": self.project.description},
                "version": self.VERSION,
            },
            "modeler": {"version": "generic-v7"},
        }

        self.write_config()

        return section

    def ask_for_path(self, current_value):
        while True:
            path = input(f"  [{current_value}]: > ")
            if path in [None, ""]:
                if current_value not in [None, ""]:
                    path = current_value

            test_file = f"{os.path.expandvars(path)}/gibsonai-test-file"

            try:
                with open(test_file, "w") as f:
                    pass

                os.remove(test_file)

                return path
            except:
                self.conversation.newline()
                self.conversation.type(
                    "    Well this is embarrassing. I cannot write to that path.\n"
                )
                self.conversation.newline()

        raise RuntimeError

    def ask_for_value(self, name, current_value):
        value = input(f"{name} [{current_value}]: > ")
        if value in [None, ""]:
            return current_value

        return value

    def __check_configuration_path(self):
        config_path = os.environ.get("GIBSONAI_CONFIG_PATH", None)
        if config_path is None:
            return self

        if not os.path.isfile(f"{config_path}/config"):
            self.conversation.newline()
            self.conversation.type(
                "[MIGRATION] environment variable detected; moving configuration to\n"
                + f"    {config_path}\n\n"
            )

            self.set_config_paths(ignore_env_vars=True)
            self.read_config()

            old_memory_path = self.project.paths.memory

            self.set_config_paths()
            self.create_project_memory()
            self.write_config()

            shutil.copytree(
                f"{old_memory_path}/{self.project.name}",
                f"{self.project.paths.memory}/{self.project.name}",
            )

        return self

    def __check_for_configuration_migration(self):
        try:
            with open(self.project.paths.config, "r") as f:
                contents = f.read()
        except FileNotFoundError:
            return self

        self.settings = json.loads(contents)
        if self.settings is None:
            return self

        for project_name, conf in self.settings.items():
            if "version" not in conf["meta"]:
                # -- Migrate from version 0 -> 1
                self.conversation.newline()
                self.conversation.type(
                    f"[MIGRATION] {project_name} configuration: 0 -> 1"
                )

                conf["meta"]["version"] = 1
                conf["dev"] = conf["copilot"]
                del conf["copilot"]

                self.settings[project_name] = conf

            if conf["meta"]["version"] == 1:
                # -- Migrate from version 1 -> 2
                self.conversation.newline()
                self.conversation.type(
                    f"[MIGRATION] {project_name} configuration: 1 -> 2\n"
                )
                self.conversation.type(
                    "  We advise that you execute the following command to "
                    + "configure new features:\n"
                    + "    gibson dev on\n"
                )
                self.conversation.wait()

                conf["meta"]["version"] = self.VERSION
                conf["dev"]["api"] = {"path": None, "prefix": "-", "version": "v1"}
                conf["dev"]["base"] = {"path": conf["dev"]["path"]["base"]}
                conf["dev"]["model"] = {"path": conf["dev"]["path"]["model"]}
                conf["dev"]["schema"] = {"path": conf["dev"]["path"]["schema"]}

                del conf["dev"]["path"]

                self.settings[project_name] = conf

        self.write_config()

        return self

    def create_project_memory(self):
        try:
            os.makedirs(self.project.paths.memory)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    def get_access_token(self):
        try:
            with open(f"{self.paths.auth}/{self.API_ENV}", "r") as f:
                contents = f.read()
        except FileNotFoundError:
            return None

        token = json.loads(contents)
        return token["access_token"]

    def get_my_settings(self):
        return self.settings[self.project.name]

    def initialize(self):
        self.conversation.message_welcome()
        print("")
        project_name = self.conversation.prompt_project()
        project_description = self.conversation.prompt_description(project_name)

        self.conversation.message_new_project(project_name)
        self.conversation.pause()

        section = self.append_project_to_conf(project_name, project_description)
        self.create_project_memory()

        self.conversation.message_configuration_added(
            self.project.paths.config, section
        )
        self.conversation.wait()
        self.conversation.message_customize_settings()

        self.conversation.wait()
        self.conversation.message_environment()

        self.conversation.wait()
        self.conversation.message_explain_help()
        self.conversation.pause()
        print("")

        return self

    def read_config(self):
        try:
            with open(self.project.paths.config, "r") as f:
                contents = f.read()
        except FileNotFoundError:
            return self

        self.settings = json.loads(contents)
        if self.settings is None:
            return self

        if len(self.settings.keys()) == 1:
            config = list(self.settings.values())[0]
            self.project.name = list(self.settings.keys())[0]
        else:
            gibsonai_project = os.environ.get("GIBSONAI_PROJECT")
            if gibsonai_project is None:
                self.conversation.gibsonai_project_not_set(self)
                exit(1)

            if gibsonai_project not in self.settings:
                self.conversation.unrecognized_project(self, gibsonai_project)
                exit(1)

            config = self.settings[gibsonai_project]
            self.project.name = gibsonai_project

        self.project.api.key = config["api"]["key"]
        self.project.code.custom.model_class = config["code"]["custom"]["model"][
            "class"
        ]
        self.project.code.custom.model_path = config["code"]["custom"]["model"]["path"]
        self.project.code.frameworks.api = config["code"]["frameworks"]["api"]
        self.project.code.frameworks.model = config["code"]["frameworks"]["model"]
        self.project.code.frameworks.revision = config["code"]["frameworks"]["revision"]
        self.project.code.frameworks.schema = config["code"]["frameworks"]["schema"]
        self.project.code.frameworks.test = config["code"]["frameworks"]["test"]
        self.project.code.language = config["code"]["language"]
        self.project.dev.active = config["dev"]["active"]
        self.project.dev.api.path = config["dev"]["api"]["path"]
        self.project.dev.api.prefix = config["dev"]["api"]["prefix"]
        self.project.dev.api.version = config["dev"]["api"]["version"]
        self.project.dev.base.path = config["dev"]["base"]["path"]
        self.project.dev.model.path = config["dev"]["model"]["path"]
        self.project.dev.schema.path = config["dev"]["schema"]["path"]
        self.project.datastore.type = config["datastore"]["type"]
        self.project.datastore.uri = config["datastore"]["uri"]
        self.project.description = config["meta"]["project"]["description"]
        self.project.modeler.version = config["modeler"]["version"]

        return self

    def set_access_token(self, token):
        try:
            os.mkdir(self.paths.auth)
        except FileExistsError:
            pass

        with open(f"{self.paths.auth}/{self.API_ENV}", "w") as f:
            f.write(json.dumps({"access_token": token}))

    def set_config_paths(self, ignore_env_vars=False):
        user_home = os.environ.get("HOME")
        gibson_config_dir = ".gibsonai"
        self.paths.auth = f"{user_home}/{gibson_config_dir}/auth"

        project_config_path = None
        if ignore_env_vars is False:
            project_config_path = os.environ.get("GIBSONAI_CONFIG_PATH", None)

        if project_config_path is None:
            project_config_path = user_home
            if project_config_path is None:
                raise RuntimeError(
                    "Gibson here. Please set your HOME environment variable."
                )

            project_config_path += f"/{gibson_config_dir}"

        self.project.paths.top = project_config_path
        self.project.paths.config = f"{self.project.paths.top}/config"
        self.project.paths.memory = f"{self.project.paths.top}/memory"

    def set_project_env(self, project_name):
        os.environ["GIBSONAI_PROJECT"] = project_name
        return self

    def turn_dev_off(self):
        self.settings[self.project.name]["dev"]["active"] = False
        self.write_config()
        return self

    def turn_dev_on(
        self, api_path, api_prefix, api_version, base_path, model_path, schema_path
    ):
        self.settings[self.project.name]["dev"]["active"] = True
        self.settings[self.project.name]["dev"]["api"]["path"] = api_path
        self.settings[self.project.name]["dev"]["api"]["prefix"] = api_prefix
        self.settings[self.project.name]["dev"]["api"]["version"] = api_version
        self.settings[self.project.name]["dev"]["base"]["path"] = base_path
        self.settings[self.project.name]["dev"]["model"]["path"] = model_path
        self.settings[self.project.name]["dev"]["schema"]["path"] = schema_path
        self.write_config()
        return self

    def write_config(self):
        try:
            os.mkdir("/".join(self.project.paths.config.split("/")[0:-1]))
        except FileExistsError:
            pass

        with open(self.project.paths.config, "w") as f:
            f.write(json.dumps(self.settings))

        self.read_config()

        return self
