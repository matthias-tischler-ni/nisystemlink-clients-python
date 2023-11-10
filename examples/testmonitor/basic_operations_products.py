"""This example demonstrates the basic operations of TestMonitorClient - Product APIs.
1. Create a product
2. Query for a product by its part_number
3. Update a product (name)
4. Delete a product
"""
from nisystemlink.clients.testmonitor import TestMonitorClient
from nisystemlink.clients.testmonitor.models import (
    CreateProductsRequest,
    ProductField,
    ProductQueryOrderByField,
    ProductRequestObject,
    ProductsAdvancedQuery,
    ProductUpdateRequestObject,
    UpdateProductsRequest,
)

PART_NUMBER = "example_product_1"

client = TestMonitorClient()

# Create a Product.
create_product_response = client.create_products(
    products=CreateProductsRequest(
        products=[
            ProductRequestObject(
                part_number=PART_NUMBER,
                name="example_product",
                family="example",
                keywords=["example_keyword"],
                properties={"example_key": "example_value"},
            )
        ]
    )
)
example_product = create_product_response.products[0]

print(f"Created Product {example_product.id}")

# Query the product by part_number
query_product_response = client.query_products(
    query_filter=ProductsAdvancedQuery(
        filter="partNumber == @0",
        substitutions=[PART_NUMBER],
        order_by=ProductQueryOrderByField.NAME,
        descending=False,
        projection=[ProductField.ID],
        take=1,
        return_count=True,
    )
)
queried_product = query_product_response.products[0]

if queried_product.id:
    product_id = queried_product.id

print(f"Queried Product by Part Number {product_id}")

# Update the product name
update_product_response = client.update_products(
    request_body=UpdateProductsRequest(
        products=[ProductUpdateRequestObject(id=product_id, name="updated_product")],
        replace=False,
    )
)
updated_product = update_product_response.products[0]

print(f"Updated Product Name {updated_product.name}")

# Delete the product.
client.delete_product(productId=product_id)
print(f"Deleted product {product_id}")
