from helloasso_api_wrapper.clients.generic_client import GenericClient
from helloasso_api_wrapper.models.organization import OrganizationModel


class OrganizationVisualisation(GenericClient):
    def get_organization_details(self, organization_slug: str) -> OrganizationModel:
        return self.api.callAndSerialize(
            f"/organizations/{organization_slug}",
            OrganizationModel,
        )
