from typing import List
import uuid
import pytest
from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.testmonitor import TestMonitorClient
from nisystemlink.clients.testmonitor import models
from nisystemlink.clients.testmonitor.models import (
    CreateProductsPartialSuccess,
    Product,
)
from nisystemlink.clients.testmonitor.models._paged_products import PagedProducts
from nisystemlink.clients.testmonitor.models._query_products_request import (
    QueryProductsRequest,
)


@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration) -> TestMonitorClient:
    """Fixture to create a TestMonitorClient instance."""
    return TestMonitorClient(enterprise_config)


@pytest.fixture
def unique_part_number() -> str:
    """Unique product id for this test."""
    product_id = uuid.uuid1().hex
    return product_id


@pytest.fixture
def create_products(client: TestMonitorClient):
    """Fixture to return a factory that creates specs."""
    responses: List[CreateProductsPartialSuccess] = []

    def _create_products(products: List[Product]) -> CreateProductsPartialSuccess:
        response = client.create_products(products)
        responses.append(response)
        return response

    yield _create_products

    created_products: List[Product] = []
    for response in responses:
        if response.products:
            created_products = created_products + response.products
    client.delete_products(ids=[product.id for product in created_products])


@pytest.mark.integration
@pytest.mark.enterprise
class TestTestMonitor:
    def test__api_info__returns(self, client: TestMonitorClient):
        response = client.api_info()
        assert len(response.dict()) != 0

    def test__create_single_product__one_product_created_with_right_field_values(
        self, client: TestMonitorClient, create_products
    ):
        part_number = "Test Part Number"
        name = "Test Name"
        family = "Example Family"
        keywords = ["testing"]
        properties = {"test_property": "yes"}
        product = Product(
            part_number=part_number,
            name=name,
            family=family,
            keywords=keywords,
            properties=properties,
        )

        response: CreateProductsPartialSuccess = create_products([product])
        assert response is not None
        assert len(response.products) == 1
        created_product = response.products[0]
        assert created_product.part_number == part_number
        assert created_product.name == name
        assert created_product.family == family
        assert created_product.keywords == keywords
        assert created_product.properties == properties

    def test__create_multiple_products__multiple_creates_succeed(
        self, client: TestMonitorClient, create_products
    ):
        products = [
            Product(part_number="Test Part Number"),
            Product(part_number="Test Part Number 2"),
        ]
        response: CreateProductsPartialSuccess = create_products(products)
        assert response is not None
        assert len(response.products) == 2

    def test__create_single_product_and_get_products__at_least_one_product_exists(
        self, client: TestMonitorClient, create_products, unique_part_number
    ):
        products = [Product(part_number=unique_part_number)]
        create_products(products)
        get_response = client.get_products()
        assert get_response is not None
        assert len(get_response.products) >= 1

    def test__create_multiple_products_and_get_products_with_take__only_take_returned(
        self, client: TestMonitorClient, create_products, unique_part_number
    ):
        products = [
            Product(part_number=unique_part_number),
            Product(part_number=unique_part_number),
        ]
        create_products(products)
        get_response = client.get_products(take=1)
        assert get_response is not None
        assert len(get_response.products) == 1

    def test__create_multiple_products_and_get_products_with_count_at_least_one_count(
        self, client: TestMonitorClient, create_products, unique_part_number
    ):
        products = [
            Product(part_number=unique_part_number),
            Product(part_number=unique_part_number),
        ]
        create_products(products)
        get_response: models.PagedProducts = client.get_products(return_count=True)
        assert get_response is not None
        assert get_response.total_count >= 2

    def test__get_product_by_id__product_matches_expected(
        self, client: TestMonitorClient, create_products, unique_part_number
    ):
        part_number = unique_part_number
        products = [Product(part_number=part_number)]
        create_response: CreateProductsPartialSuccess = create_products(products)
        assert create_response is not None
        id = create_response.products[0].id
        product = client.get_product(id)
        assert product is not None
        assert product.part_number == part_number

    def test__query_product_by_part_number__matches_expected(
        self, client: TestMonitorClient, create_products, unique_part_number
    ):
        part_number = unique_part_number
        products = [Product(part_number=part_number)]
        create_response: CreateProductsPartialSuccess = create_products(products)
        assert create_response is not None
        created_product = create_response.products[0]
        query_request = QueryProductsRequest(
            filter=f'partNumber="{part_number}"', return_count=True
        )
        query_response: PagedProducts = client.query_products(query_request)
        assert query_response.total_count == 1
        assert query_response.products[0].part_number == part_number
