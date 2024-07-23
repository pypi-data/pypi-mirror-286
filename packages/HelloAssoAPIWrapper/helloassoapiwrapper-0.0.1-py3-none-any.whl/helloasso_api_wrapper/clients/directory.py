from helloasso_api_wrapper.clients.generic_client import GenericClient
from helloasso_api_wrapper.models.directory import (
    ListFormsRequest,
    ListOrganizationsRequest,
)
from helloasso_api_wrapper.models.results_with_pagination_model.directory import (
    PaginatedSynchronizableFormModel,
    PaginatedSynchronizableOrganizationModel,
)


class Directory(GenericClient):
    def get_all_forms(
        self,
        list_forms_request: ListFormsRequest,
        page_size: int | None = None,
        continuation_token: str | None = None,
    ) -> PaginatedSynchronizableFormModel:
        """
        Get all forms by form filters and organization filters
        """
        # Could not try due to insufficient Privileges
        return self.api.callAndSerialize(
            "/directory/forms",
            PaginatedSynchronizableFormModel,
            params={
                "pageSize": page_size,
                "continuationToken": continuation_token,
            },
            body=list_forms_request,
            method="POST",
        )

    def get_all_organizations(
        self,
        list_organizations_request_body: ListOrganizationsRequest,
        page_size: int | None = None,
        continuation_token: str | None = None,
    ) -> PaginatedSynchronizableOrganizationModel:
        """
        Get all organization by organization filters
        """
        # Could not try due to insufficient Privileges
        return self.api.callAndSerialize(
            "/directory/organizations",
            PaginatedSynchronizableOrganizationModel,
            params={
                "pageSize": page_size,
                "continuationToken": continuation_token,
            },
            body=list_organizations_request_body,
            method="POST",
        )
