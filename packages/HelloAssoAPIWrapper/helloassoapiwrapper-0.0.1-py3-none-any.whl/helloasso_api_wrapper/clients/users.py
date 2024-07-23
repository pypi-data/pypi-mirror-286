from helloasso_api_wrapper.clients.generic_client import GenericClient
from helloasso_api_wrapper.models.organization import OrganizationLightModel


class Users(GenericClient):
    def get_my_organizations(self) -> list[OrganizationLightModel]:
        return self.api.callAndSerialize(
            "/users/me/organizations",
            list[OrganizationLightModel],
        )
