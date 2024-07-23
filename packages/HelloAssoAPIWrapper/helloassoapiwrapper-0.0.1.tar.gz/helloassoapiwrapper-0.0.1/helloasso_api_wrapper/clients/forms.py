from helloasso_api_wrapper.clients.generic_client import GenericClient
from helloasso_api_wrapper.models.enums import FormType
from helloasso_api_wrapper.models.forms import (
    FormPublicModel,
    FormQuickCreateModel,
    FormQuickCreateRequest,
)
from helloasso_api_wrapper.models.results_with_pagination_model.forms import (
    PaginatedFormLightModel,
)


class Forms(GenericClient):
    def create_a_simplified_event(
        self,
        organization_slug: str,
        form_type: FormType,
        quick_form_create_request_body: FormQuickCreateRequest,
    ) -> FormQuickCreateModel:
        """
        Create a simplified event for an Organism
        """
        return self.api.callAndSerialize(
            f"/organizations/{organization_slug}/forms/{form_type}/action/quick-create",
            FormQuickCreateModel,
            body=quick_form_create_request_body,
            method="POST",
        )

    def get_form_public_data(
        self,
        organization_slug: str,
        form_type: FormType,
        form_slug: str,
    ) -> FormPublicModel:
        """
        Get detailed public data about a specific form
        """

        return self.api.callAndSerialize(
            f"/organizations/{organization_slug}/forms/{form_type}/{form_slug}/public",
            FormPublicModel,
            method="GET",
        )

    def get_form_types(
        self,
        organization_slug: str,
        states: list[str] | None = None,
    ) -> list[FormType]:
        """
        Get a list of formTypes for an organization
        """
        # Tested and works

        return self.api.callAndSerialize(
            f"/organizations/{organization_slug}/formTypes",
            list[FormType],
            params={"states": states},
            method="GET",
        )

    def get_organization_forms(
        self,
        organization_slug: str,
        states: list[str] | None = None,
        form_types: list[FormType] | None = None,
        page_index: int | None = None,
        page_size: int | None = None,
        continuation_token: str | None = None,
    ) -> PaginatedFormLightModel:
        """
        Get the forms of a specific organization
        """
        # Tested and works

        return self.api.callAndSerialize(
            f"/organizations/{organization_slug}/forms",
            PaginatedFormLightModel,
            params={
                "states": states,
                "formTypes": form_types,
                "pageIndex": page_index,
                "pageSize": page_size,
                "continuationToken": continuation_token,
            },
            method="GET",
        )
