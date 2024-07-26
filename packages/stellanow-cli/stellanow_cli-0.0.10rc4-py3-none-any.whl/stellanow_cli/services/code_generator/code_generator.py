"""
Copyright (C) 2022-2024 Stella Technologies (UK) Limited.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""
import itertools
import json
from dataclasses import dataclass
from typing import Generator, List

import httpx
from keycloak import KeycloakError, KeycloakOpenID
from loguru import logger

from stellanow_cli.core.datatypes import (
    StellaEntity,
    StellaEvent,
    StellaEventDetailed,
    StellaField,
    StellaModel,
    StellaModelDetailed,
    StellaModelField,
)
from stellanow_cli.core.decorators import make_stella_context_pass_decorator
from stellanow_cli.exceptions.api_exceptions import (
    StellaAPIBadRequestError,
    StellaAPIForbiddenError,
    StellaAPIInternalServerError,
    StellaAPINotFoundError,
    StellaAPIUnauthorisedError,
    StellaAPIWrongCredentialsError,
    StellaNowKeycloakCommunicationException,
)
from stellanow_cli.services.service import StellaNowService, StellaNowServiceConfig

CODE_GENERATOR_SERVICE_NAME = "code-generator-service"
OIDC_CLIENT_ID = "tools-cli"


@dataclass
class CodeGeneratorServiceConfig(StellaNowServiceConfig):
    base_url: str
    username: str
    password: str
    organization_id: str
    project_id: str


class CodeGeneratorService(StellaNowService):
    def __init__(self, config: CodeGeneratorServiceConfig) -> None:  # noqa
        self._config = config
        self.auth_token = None
        self.refresh_token = None
        self.keycloak = KeycloakOpenID(
            server_url=self._auth_url, client_id=OIDC_CLIENT_ID, realm_name=self._config.organization_id, verify=True
        )

        self.authenticate()

    @classmethod
    def service_name(cls) -> str:
        return CODE_GENERATOR_SERVICE_NAME

    @property
    def _auth_url(self):
        return f"{self._config.base_url}/auth/"

    @property
    def _events_url(self):
        return f"{self._config.base_url}/workflow-management/projects/{{projectId}}/events"

    @property
    def _event_url(self):
        return f"{self._config.base_url}/workflow-management/projects/{{projectId}}/events/{{eventId}}"

    @property
    def _models_url(self):
        return f"{self._config.base_url}/workflow-management/projects/{{projectId}}/model"

    @property
    def _model_url(self):
        return f"{self._config.base_url}/workflow-management/projects/{{projectId}}/model/{{modelId}}"

    def _handle_response(self, response):
        if response.status_code < 400:
            return
        try:
            details = response.json().get("details", dict())[0]
            if not isinstance(details, dict):
                details = dict()
        except json.JSONDecodeError:
            details = dict()
        match response.status_code:
            case 400:
                raise StellaAPIBadRequestError(details)
            case 401:
                errors = details.get("errors", list())
                if not isinstance(errors, list):
                    errors = list()

                for error in errors:
                    match error.get("errorCode"):
                        case "inactiveAuthToken":
                            self.auth_refresh()
                            return
                        case "wrongUsernameOrPassword":
                            raise StellaAPIWrongCredentialsError()
                        case _:
                            raise StellaAPIUnauthorisedError(details)
                else:
                    response.raise_for_status()
            case 403:
                raise StellaAPIForbiddenError(details)
            case 404:
                raise StellaAPINotFoundError(details)
            case 500:
                raise StellaAPIInternalServerError(details)
            case _:
                response.raise_for_status()

    def _get_token_response(self):
        try:
            return self.keycloak.token(username=self._config.username, password=self._config.password)
        except KeycloakError as exc:
            logger.error("operation failed")
            raise StellaNowKeycloakCommunicationException(details=exc)

    def authenticate(self):
        logger.info("Authenticating to the API ... ")

        if self.refresh_token is not None:
            self.auth_refresh()
        else:
            self.auth_token = None
            self.refresh_token = None

            response = self._get_token_response()

            self.auth_token = response.get("access_token")
            self.refresh_token = response.get("refresh_token")

        logger.info("Authentication Successful")

    def auth_refresh(self):
        if self.refresh_token is None:
            self.authenticate()
        else:
            logger.info("API Token Refreshing ...")

            refresh_token = self.refresh_token

            self.auth_token = None
            self.refresh_token = None

            response = self.keycloak.refresh_token(refresh_token)

            self.auth_token = response.get("password")
            self.refresh_token = response.get("refresh_token")

            logger.info("API Token Refresh Successful")

    def get_events(self) -> List[StellaEvent]:
        page_size: int = 100
        events: List[StellaEvent] = []
        for page_number in itertools.count(1, 1):
            url = (
                self._events_url.format(projectId=self._config.project_id)
                + f"?page={page_number}&pageSize={page_size}&filter=IncludeInactive"
            )
            headers = {"Authorization": f"Bearer {self.auth_token}"}

            response = httpx.get(url, headers=headers)
            self._handle_response(response)

            page_events = response.json().get("details", dict()).get("results", [])
            if not page_events:
                break

            events.extend(
                StellaEvent(
                    id=event.get("id"),
                    name=event.get("name"),
                    isActive=event.get("isActive"),
                    createdAt=event.get("createdAt"),
                    updatedAt=event.get("updatedAt"),
                )
                for event in page_events
            )

        return events

    def get_event_details(self, event_id: str) -> StellaEventDetailed:
        url = self._event_url.format(projectId=self._config.project_id, eventId=event_id)
        headers = {"Authorization": f"Bearer {self.auth_token}"}

        response = httpx.get(url, headers=headers)
        self._handle_response(response)

        details = response.json().get("details", dict())
        # logger.info(details)

        # create StellaEntity objects from the 'entities' list
        entities = [StellaEntity(**entity) for entity in details.get("entities", list())]

        # create StellaField objects from the 'fields' list
        fields = [StellaField(**field) for field in details.get("fields", list())]

        # create and return StellaEventDetailed object
        return StellaEventDetailed(
            id=details.get("id"),
            name=details.get("name"),
            description=details.get("description"),
            isActive=details.get("isActive"),
            createdAt=details.get("createdAt"),
            updatedAt=details.get("updatedAt"),
            fields=fields,
            entities=entities,
        )

    def get_models(self) -> Generator[StellaModel, None, None]:
        page_size = 100
        for page_number in itertools.count(1, 1):
            url = (
                self._models_url.format(projectId=self._config.project_id) + f"?page={page_number}&pageSize={page_size}"
            )
            headers = {"Authorization": f"Bearer {self.auth_token}"}

            response = httpx.get(url, headers=headers)
            self._handle_response(response)

            models = response.json().get("details", dict()).get("results", [])
            if not models:
                break

            yield from (
                StellaModel(
                    id=model.get("id"),
                    name=model.get("name"),
                    createdAt=model.get("createdAt"),
                    updatedAt=model.get("updatedAt"),
                )
                for model in models
            )

    def get_model_details(self, model_id: str) -> StellaModelDetailed:
        url = self._model_url.format(projectId=self._config.project_id, modelId=model_id)
        headers = {"Authorization": f"Bearer {self.auth_token}"}

        response = httpx.get(url, headers=headers)
        self._handle_response(response)

        details = response.json().get("details", dict())
        # logger.info(details)

        fields = [StellaModelField(**field) for field in details.get("fields", list())]

        return StellaModelDetailed(
            id=details.get("id"),
            name=details.get("name"),
            description=details.get("description"),
            createdAt=details.get("createdAt"),
            updatedAt=details.get("updatedAt"),
            fields=fields,
        )


pass_code_generator_service = make_stella_context_pass_decorator(CodeGeneratorService)
