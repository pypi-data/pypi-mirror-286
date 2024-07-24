import os

import requests

from ._exceptions import ModulosError
from . import resources


__all__ = [
    "Modulos",
]


class Modulos:
    testing: resources.Testing

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
    ) -> None:

        if api_key is None:
            api_key = os.environ.get("MODULOS_API_KEY")
        if api_key is None:
            raise ModulosError(
                "The api_key client option must be set either by passing "
                "api_key to the client "
                "or by setting the MODULOS_API_KEY environment variable"
            )

        self.api_key = api_key

        if base_url is None:
            base_url = "https://app.modulos.ai/api"
        self.base_url = base_url

        self.testing = resources.Testing(self)

    def post(
        self,
        endpoint: str,
        url_params: dict | None = None,
        data: dict | None = None,
        files: dict | None = None,
    ):
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        api_url = f"{self.base_url}{endpoint}"

        if url_params:
            api_url += "?" + "&".join([f"{k}={v}" for k, v in url_params.items()])

        response = requests.post(
            api_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=data,
            files=files,
        )

        return response

    def get(self, endpoint: str, data: dict | None = None):
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        api_url = f"{self.base_url}{endpoint}"
        response = requests.get(
            api_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=data,
        )
        return response

    def delete(
        self,
        endpoint: str,
        url_params: dict | None = None,
        data: dict | None = None,
    ):
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        api_url = f"{self.base_url}{endpoint}"

        if url_params:
            api_url += "?" + "&".join([f"{k}={v}" for k, v in url_params.items()])

        response = requests.delete(
            api_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=data,
        )
        return response

    def patch(self, endpoint: str, data: dict):
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        api_url = f"{self.base_url}{endpoint}"
        response = requests.patch(
            url=api_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=data,
        )
        return response
