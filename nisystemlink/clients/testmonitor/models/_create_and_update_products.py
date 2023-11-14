"""Create and Update products models."""
from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._testmonitor_models import (
    Error,
    ProductRequestObject,
    ProductResponseObject,
    ProductUpdateRequestObject,
)


class CreateProductsRequest(JsonModel):
    products: List[ProductRequestObject]
    """
    Array of products to be created.
    """


class UpdateProductsRequest(JsonModel):
    products: List[ProductUpdateRequestObject]
    """
    Array of products to update.
    """
    replace: bool
    """
    Replace the existing fields instead of merging them.
    """


class CreateOrUpdateProductsResponse(JsonModel):
    products: List[ProductResponseObject]
    """
    Array of products which are created or updated.
    """
    failed: Optional[List[ProductRequestObject]]
    """
    Array of products which are not created or not updated properly.
    """
    error: Optional[Error]
    """
    Default error model.
    """
