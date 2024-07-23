from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel

from helloasso_api_wrapper.models.forms import FormPublicModel
from helloasso_api_wrapper.models.statistics import OrderDetail, PaymentDetail


class ApiNotificationType(str, Enum):
    Payment = "Payment"
    Order = "Order"
    Form = "Form"
    Organization = "Organization"


class PostApiUrlNotificationBody(BaseModel):
    url: str
    notificationType: ApiNotificationType | None = None


class ApiUrlNotificationModel(BaseModel):
    url: str | None = None
    apiNotificationType: ApiNotificationType | None = None


class OrganizationNotificationResultData(BaseModel):
    old_slug_organization: str
    new_slug_organization: str


class OrganizationNotificationResultContent(BaseModel):
    eventType: Literal[ApiNotificationType.Organization]
    data: OrganizationNotificationResultData
    metadata: None = None  # not sure


class OrderNotificationResultContent(BaseModel):
    """
    metadata should contain the metadata sent while creating the checkout intent in `InitCheckoutBody`
    """

    eventType: Literal[ApiNotificationType.Order]
    data: OrderDetail
    metadata: dict[str, Any] | None = None


class PayementNotificationResultContent(BaseModel):
    """
    metadata should contain the metadata sent while creating the checkout intent in `InitCheckoutBody`
    """

    eventType: Literal[ApiNotificationType.Payment]
    data: PaymentDetail
    metadata: dict[str, Any] | None = None


class FormNotificationResultContent(BaseModel):
    eventType: Literal[ApiNotificationType.Form]
    data: FormPublicModel
    metadata: dict[str, Any] | None = None  # not sure


NotificationResultContent = (
    OrganizationNotificationResultContent
    | OrderNotificationResultContent
    | PayementNotificationResultContent
    | FormNotificationResultContent
)
"""
When a new content is available, HelloAsso will call the notification URL callback with the corresponding data in the body.
"""
