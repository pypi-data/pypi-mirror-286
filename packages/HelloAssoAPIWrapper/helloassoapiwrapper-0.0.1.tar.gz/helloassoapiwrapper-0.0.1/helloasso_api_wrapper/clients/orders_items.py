from datetime import datetime

from helloasso_api_wrapper.clients.generic_client import GenericClient
from helloasso_api_wrapper.models.enums import FormType, SortField, SortOrder
from helloasso_api_wrapper.models.forms import (
    FormQuickCreateModel,
)
from helloasso_api_wrapper.models.statistics import Item


class Forms(GenericClient):
    def create_a_simplified_event(
        self,
        item_id: str,
        with_details: bool | None = None,
    ) -> FormQuickCreateModel:
        """
        Get the detail of an item contained in an order
        """
        return self.api.callAndSerialize(
            f"/items/{item_id}",
            FormQuickCreateModel,
            params={"withDetails": with_details},
            method="GET",
        )

    def get_items_from_form(
        self,
        organization_slug: str,
        form_type: FormType,
        form_slug: str,
        from_datetime: datetime | None = None,
        to_datetime: datetime | None = None,
        user_search_key: str | None = None,
        page_index: int | None = None,
        page_size: int | None = None,
        continuation_token: str | None = None,
        tier_types: list[str] | None = None,
        item_states: list[str] | None = None,
        tier_name: str | None = None,
        with_details: bool | None = None,
        sort_order: SortOrder | None = None,
        sort_field: SortField | None = None,
    ) -> list[Item]:
        """
        Get a list of items "sold" in a form
        """
        return self.api.callAndSerialize(
            f"/organizations/{organization_slug}/forms/{form_type}/{form_slug}/items",
            list[Item],
            params={
                "from": from_datetime,
                "to": to_datetime,
                "userSearchKey": user_search_key,
                "pageIndex": page_index,
                "pageSize": page_size,
                "continuationToken": continuation_token,
                "tierTypes": tier_types,
                "itemStates": item_states,
                "tierName": tier_name,
                "withDetails": with_details,
                "sortOrder": sort_order,
                "sortField": sort_field,
            },
            method="GET",
        )
