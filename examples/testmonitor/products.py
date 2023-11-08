"""Functionality of Product APIs."""
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

FAMILY = "EXAMPLE FAMILY"

client = TestMonitorClient()

# Create a Product.
products_request = CreateProductsRequest(
    products=[
        ProductRequestObject(
            part_number="example_product_1",
            name="example_product",
            family=FAMILY,
            keywords=["example_keywords"],
            properties={"example_key": "example_value"},
            file_ids=["example_file_id"],  # File ids are not verified.
        )
    ]
)
create_product_response = client.create_products(products=products_request)
example_product = create_product_response.products[0]

print("Product Created Successfully.")
print("Created Product Name:", example_product.name)

# Query the product.
query_filter = ProductsAdvancedQuery(
    filter="partNumber == @0",
    substitutions=["example_product_1"],
    order_by=ProductQueryOrderByField.NAME,
    descending=False,
    projection=[ProductField.ID],
    take=1,
    return_count=True,
)
query_product_response = client.query_products(query_filter=query_filter)
queried_product = query_product_response.products[0]

if queried_product.id:
    product_id = queried_product.id

print("Product Queried Successfully.")
print("Queried Product ID:", product_id)

# Update the product.
update_product_request = UpdateProductsRequest(
    products=[
        ProductUpdateRequestObject(
            id=product_id,
            name="updated_product",
            family=FAMILY,
            keywords=["updated_keywords"],
            properties={"updated_key": "updated_value"},
            file_ids=["updated_file_id"],  # File ids are not verified.
        )
    ],
    replace=False,
)
update_product_response = client.update_products(request_body=update_product_request)
updated_product = update_product_response.products[0]

print("Product Updated Successfully.")
print("Updated Product Name:", updated_product.name)

# Delete the product.
client.delete_product(productId=product_id)
print("Product Deleted Successfully")
