import os
import requests

from services.auth.Server import Server as AuthServer
from core.Configuration import Configuration
from lang.Python import Python
from core.Memory import Memory

from .BaseApi import BaseApi


class Cli(BaseApi):
    API_ENV = os.environ.get("GIBSONAI_API_ENV", "staging")
    PREFIX = "cli"
    VERSION = "v1"

    def __init__(self, configuration: Configuration):
        super().__init__()
        self.configuration = configuration

    def code_api(self):
        return self._post(
            "code/api",
            self.__structure_context_payload(self.configuration, with_stored=True),
        ).json()

    def code_base(self):
        return self._post(
            "code/base",
            self.__structure_context_payload(self.configuration, with_stored=True),
        ).json()

    def code_model_attributes(self, model_name, instructions):
        payload = self.__structure_context_payload(self.configuration)
        payload["model"] = {"name": model_name}
        payload["q"] = instructions

        return self._post("code/model/attributes", payload).json()

    def code_models(self, entities: list):
        payload = self.__structure_context_payload(self.configuration, with_stored=True)
        payload["entities"] = entities

        return self._post("code/models", payload).json()

    def code_schemas(self, entities: list):
        payload = self.__structure_context_payload(self.configuration, with_stored=True)
        payload["entities"] = entities

        return self._post("code/schemas", payload).json()

    def code_testing(self, entities: list):
        payload = self.__structure_context_payload(self.configuration, with_stored=True)
        payload["entities"] = entities

        return self._post("code/testing", payload).json()

    def code_writer_entity_modifier(self, context, name, definition, instructions):
        payload = self.__structure_context_payload(self.configuration)
        payload["context"] = context
        payload["entity"] = {"definition": definition, "name": name}
        payload["q"] = instructions

        return self._post("code/writer/entity/modifier", payload).json()

    def code_writer_schema_context(self):
        return self._post(
            "code/writer/schema/context",
            self.__structure_context_payload(self.configuration, with_stored=True),
        ).json()

    def get_client_id(self):
        return {
            "local": "9b0cbebd-3eb4-47be-89ac-4aa589316ff4",
            "staging": "02459e16-f356-4c01-b689-59847ed04b0a",
            "production": "da287371-240b-4b53-bfde-4b1581cca62a",
        }[self.API_ENV]

    def get_api_domain(self):
        return {
            "local": "http://localhost:8000",
            "staging": "https://staging-api.gibsonai.com",
            "production": "https://api.gibsonai.com",
        }[self.API_ENV]

    def get_app_domain(self):
        return {
            "local": "http://localhost:5173",
            "staging": "https://staging-app.gibsonai.com",
            "production": "https://app.gibsonai.com",
        }[self.API_ENV]

    def get_headers(self):
        headers = {
            "X-Gibson-Client-ID": self.get_client_id(),
            "X-Gibson-API-Key": self.configuration.project.api.key,
        }

        token = self.configuration.get_access_token()
        if token is not None:
            headers["Authorization"] = f"Bearer {token}"

        return headers

    def get_url(self, end_point):
        return f"{self.get_api_domain()}/{self.VERSION}/{self.PREFIX}/{end_point}"

    def import_(self):
        return self._get("import")

    def llm_query(self, instructions, has_file, has_python, has_sql):
        project_config = self.configuration.project
        r = self._post(
            "llm/query",
            {
                "content": {
                    "meta": {
                        "file": int(has_file),
                        "python": int(has_python),
                        "sql": int(has_sql),
                    }
                },
                "frameworks": {
                    "api": project_config.code.frameworks.api,
                    "model": project_config.code.frameworks.model,
                    "revision": project_config.code.frameworks.revision,
                    "schema_": project_config.code.frameworks.schema,
                    "test": project_config.code.frameworks.test,
                },
                "q": instructions,
            },
        )

        return r.json()

    def login(self):
        token = AuthServer(self.get_app_domain()).get_token()
        return token

    def modeler_entity_modify(
        self, modeler_version, project_description, entity: dict, modifications: str
    ):
        r = self._put(
            "modeler/entity/modify",
            {
                "entity": entity,
                "modeler": {"version": modeler_version},
                "modifications": modifications,
                "project": {"description": project_description},
            },
        )

        return r.json()

    def modeler_entity_remove(self, modeler_version, entities: list, entity_name):
        r = self._put(
            "modeler/entity/remove",
            {
                "entity": {"name": entity_name},
                "modeler": {"version": modeler_version},
                "schema_": entities,
            },
        )

        return r.json()

    def modeler_entity_rename(self, modeler_version, entities: list, current, new):
        r = self._put(
            "modeler/entity/rename",
            {
                "entity": {"current": current, "new": new},
                "modeler": {"version": modeler_version},
                "schema_": entities,
            },
        )

        return r.json()

    def modeler_module(self, modeler_version, project_description, module):
        r = self._post(
            "modeler/module",
            {
                "modeler": {"version": modeler_version},
                "module": module,
                "project": {"description": project_description},
            },
        )

        return r.json()

    def modeler_openapi(self, modeler_version, contents):
        r = self._post(
            "modeler/openapi",
            {"contents": contents, "modeler": {"version": modeler_version}},
        )

        return r.json()

    def modeler_reconcile(self, modeler_version, entities: list):
        r = self._post(
            "modeler/reconcile",
            {"modeler": {"version": modeler_version}, "schema_": entities},
        )

        return r.json()

    def __structure_context_payload(
        self,
        with_last=False,
        with_merged=False,
        with_stored=False,
    ):
        project_config = self.configuration.project
        payload = {
            "api": {
                "prefix": project_config.dev.api.prefix,
                "version": project_config.dev.api.version,
            },
            "frameworks": {
                "api": project_config.code.frameworks.api,
                "model": project_config.code.frameworks.model,
                "revision": project_config.code.frameworks.revision,
                "schema_": project_config.code.frameworks.schema,
                "test": project_config.code.frameworks.test,
            },
            "language": project_config.code.language,
            "path": {
                "api": Python().make_import_path(project_config.dev.api.path),
                "base": Python().make_import_path(project_config.dev.base.path),
                "custom": {
                    "model": {
                        "class_": project_config.code.custom.model_class,
                        "path": project_config.code.custom.model_path,
                    }
                },
                "model": Python().make_import_path(project_config.dev.model.path),
                "schema_": Python().make_import_path(project_config.dev.schema.path),
            },
        }

        if with_last is True:
            payload["schema_"] = Memory(self.configuration).recall_last()["entities"]
        elif with_merged is True:
            payload["schema_"] = Memory(self.configuration).recall_merged()
        elif with_stored is True:
            payload["schema_"] = Memory(self.configuration).recall_entities()

        return payload
