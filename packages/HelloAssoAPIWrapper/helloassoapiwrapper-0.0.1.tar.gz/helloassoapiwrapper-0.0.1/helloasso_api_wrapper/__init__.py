from collections.abc import Callable
from typing import Literal

from helloasso_api_wrapper.clients.checkout_intents_management import (
    CheckoutIntentsManagement,
)
from helloasso_api_wrapper.clients.directory import Directory
from helloasso_api_wrapper.clients.forms import Forms
from helloasso_api_wrapper.clients.organization_visualisation import (
    OrganizationVisualisation,
)
from helloasso_api_wrapper.clients.users import Users
from helloasso_api_wrapper.ha_apiv5_extension import HaApiV5Extension


class HelloAssoAPIWrapper:
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
        self.api = HaApiV5Extension(
            api_base=api_base,
            client_id=client_id,
            client_secret=client_secret,
            timeout=timeout,
            access_token=access_token,
            refresh_token=refresh_token,
            oauth2_token_getter=oauth2_token_getter,
            oauth2_token_setter=oauth2_token_setter,
        )
        self.checkout_intents_management = CheckoutIntentsManagement(self.api)
        self.directory = Directory(self.api)
        self.forms = Forms(self.api)
        self.organizations = OrganizationVisualisation(self.api)
        self.users = Users(self.api)
