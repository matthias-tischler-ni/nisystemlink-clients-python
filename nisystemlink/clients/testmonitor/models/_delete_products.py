"""Delete products model."""
from typing import List

from nisystemlink.clients.core._uplink._json_model import JsonModel


class ProductDeleteRequest(JsonModel):
    ids: List[str]
    """
    Array of product ids to delete.
    """
