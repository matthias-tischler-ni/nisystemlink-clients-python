"""Query products model."""
from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Field

from ._testmonitor_models import ProductResponseObject


class QueryProductsResponse(JsonModel):
    products: List[ProductResponseObject]
    """
    Array of products.
    """
    continuation_token: Optional[str] = Field(None, alias="continuationToken")
    """
    A token which allows the user to resume this query at the next item in the matching product set.
    In order to continue paginating a query, pass this token to the service on a subsequent request.
    The service will respond with a new continuation token.
    To paginate a set of products,
    continue sending requests with the newest continuation token provided by the service,
    until this value is null.
    """
    total_count: Optional[int] = Field(None, alias="totalCount")
    """
    The number of matching products, if returnCount is true.
    This value is not present if returnCount is false.
    """


class QueryProductValuesResponse(JsonModel):
    __root__: List[str]
    """
    Array of strings.
    """
