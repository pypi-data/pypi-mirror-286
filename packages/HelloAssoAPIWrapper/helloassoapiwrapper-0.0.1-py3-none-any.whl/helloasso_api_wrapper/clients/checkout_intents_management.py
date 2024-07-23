from helloasso_api_wrapper.clients.generic_client import GenericClient
from helloasso_api_wrapper.models.carts import (
    CheckoutIntentResponse,
    InitCheckoutBody,
    InitCheckoutResponse,
)


class CheckoutIntentsManagement(GenericClient):
    def retrieve_a_checkout_intent(
        self,
        organization_slug: str,
        checkout_intent_id: int,
    ) -> CheckoutIntentResponse:
        """
        Retrieve a checkout intent, with the order if the payment has been authorized.
        """
        return self.api.callAndSerialize(
            f"/organizations/{organization_slug}/checkout-intents/{checkout_intent_id}",
            CheckoutIntentResponse,
            method="GET",
        )

    def init_a_checkout(
        self,
        organization_slug: str,
        init_checkout_body: InitCheckoutBody,
    ) -> InitCheckoutResponse:
        """
        https://www.helloasso.com/public-documents/documents_api/documentation_checkout.pdf
        """
        # Tested, works
        return self.api.callAndSerialize(
            f"/organizations/{organization_slug}/checkout-intents",
            InitCheckoutResponse,
            body=init_checkout_body,
            method="POST",
        )
