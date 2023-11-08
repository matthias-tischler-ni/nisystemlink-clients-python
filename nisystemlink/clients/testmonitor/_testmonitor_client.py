"""Implementation of TestMonitorClient."""
# Python Modules.
from typing import List, Optional, Union

# Third party modules.
from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import delete, get, post
from nisystemlink.clients.testmonitor import models
from uplink import Query


class TestMonitorClient(BaseClient):
    """Class contains a set of methods to access the APIs of TestMonitor."""

    def __init__(self, configuration: Optional[core.HttpConfiguration] = None):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about
                how to connect. If not provided, an instance of
                :class:`JupyterHttpConfiguration <nisystemlink.clients.core.JupyterHttpConfiguration>`
                is used.

        Raises:
            ApiException: if unable to communicate with the TestMonitor Service.
        """
        if configuration is None:
            configuration = core.JupyterHttpConfiguration()

        super().__init__(configuration, "/nitestmonitor/v2/")

    # versioning
    @get("")
    def api_info(self) -> models.V2Operations:
        """Get information about available API operations.

        Returns:
            Information about available API operations.
        """
        ...

    # products
    @post("query-products")
    def query_products(
        self,
        query_filter: models.ProductsAdvancedQuery,
    ) -> models.ProductsQueryResponse:
        """Get products based on the filter.

        Args:
            query_filter: Filter to be applied for Products .

        Returns:
            List of products.
        """
        ...

    @get("products", args=[Query, Query, Query])
    def get_products(
        self,
        continuationToken: Optional[str],
        take: Optional[int],
        returnCount: bool,
    ) -> models.ProductsQueryResponse:
        """Get product details of multiple products.

        Args:
            continuationToken: The token used to paginate results.
            take: Limits the returned list of products to the specified number.
            returnCount: Total count of the products available.

        Returns:
            List of products.
        """
        ...

    @post("products")
    def create_products(
        self,
        products: models.CreateProductsRequest,
    ) -> models.CreateOrUpdateProductsResponse:
        """Create new products with given product details.

        Args:
            products: The request body of the products.

        Returns:
            Details of newly created products.

        """
        ...

    @get("products/{productId}")
    def get_product(self, productId: Optional[str]) -> models.ProductResponseObject:
        """Get product details of a single product.

        Args:
            productId: Unique ID of a product.

        Returns:
            Details of the provided product id.
        """
        ...

    @delete("products/{productId}")
    def delete_product(self, productId: str) -> None:
        """Delete a product.

        Args:
            productId: Id of the product to be deleted.

        Returns:
            None
        """
        ...

    @post("query-product-values")
    def query_product_values(
        self,
        product_query: models.ProductValuesQuery,
    ) -> List[str]:
        """Get product values.

        Args:
            product_query: Filter to be applied for products.

        Returns:
            List of values based on the product_query.
        """
        ...

    @post("update-products")
    def update_products(
        self,
        request_body: models.UpdateProductsRequest,
    ) -> models.CreateOrUpdateProductsResponse:
        """Update multiple products.

        Args:
            request_body: The updated details of the products.

        Returns:
            Details of updated products.
        """
        ...

    @post("delete-products")
    def delete_products(self, request_body: models.ProductDeleteRequest) -> None:
        """Delete multiple products.

        Args:
            request_body: List of product ids to be deleted.

        Returns:
            None
        """
        ...
