from helloasso_api_wrapper.ha_apiv5_extension import HaApiV5Extension


class GenericClient:
    """
    A class to create a client for the HelloAsso API.

    You can create a client by inheriting this class and passing
    the HelloAssoAPI instance in the constructor.

    Example:
    ```python
    class Users(HelloAssoSubClient):
        def get_my_organizations(self) -> list[OrganizationLightModel]:
            return self.api.callAndSerializeList(
                "/v5/users/me/organizations",
                OrganizationLightModel,
            )
    ```
    """

    def __init__(self, api: HaApiV5Extension):
        self.api = api
