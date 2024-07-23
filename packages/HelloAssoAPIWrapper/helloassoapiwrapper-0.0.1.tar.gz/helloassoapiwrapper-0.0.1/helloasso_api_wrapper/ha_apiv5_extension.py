from collections.abc import Callable
from enum import Enum
from typing import Any, Literal, TypeVar

from helloasso_api import HaApiV5
from pydantic import BaseModel, TypeAdapter


class HaApiV5Extension(HaApiV5):  # type: ignore
    """
    The class inherit from HaApiV5 and add some methods to serialize the response of the API.
    """

    def __init__(
        self,
        api_base: str,
        client_id: str,
        client_secret: str,
        timeout: int | None = None,
        access_token: str | None = None,
        refresh_token: str | None = None,
        oauth2_token_getter: (
            Callable[
                [Literal["access_token", "refresh_token"], str],
                str,
            ]
            | None
        ) = None,
        oauth2_token_setter: (
            Callable[
                [Literal["access_token", "refresh_token"], str, str],
                None,
            ]
            | None
        ) = None,
    ):
        super().__init__(
            api_base=api_base,
            client_id=client_id,
            client_secret=client_secret,
            timeout=timeout,
            access_token=access_token,
            refresh_token=refresh_token,
            oauth2_token_getter=oauth2_token_getter,
            oauth2_token_setter=oauth2_token_setter,
        )

    Model = TypeVar("Model", bound=BaseModel | list | Enum)

    def serialize(
        self,
        obj: Any,
        model: type[Model],
    ) -> Model:
        type_adapter = TypeAdapter(model)
        return type_adapter.validate_python(obj)  # type: ignore

    def callAndSerialize(
        self,
        sub_path: str,
        model: type[Model],
        params: dict | None = None,
        method: str | None = "GET",
        body: BaseModel | None = None,
        headers: dict | None = None,
        include_auth: bool = True,
    ) -> Model:
        """
        Call the request using HaApiV5 and then serialize the response.

        The `body` will be serialized to json using Pydantic and passed to HaAPIV5.
        """

        # The default json serializer used by Requests does not handle datetime
        # We will use Pydantic serializer instead then pass the body as `data`, including an "application/json" header
        # See https://github.com/psf/requests/issues/3947
        data = body.model_dump_json() if body else None
        if headers is None:
            headers = {}
        headers["Content-type"] = "application/json"

        sub_path = "/v5" + sub_path
        response = self.call(
            sub_path,
            params=params,
            method=method,
            data=data,
            headers=headers,
            include_auth=include_auth,
        ).json()

        return self.serialize(response, model)
