import json

def product_to_json(query_data):
    product_dict = [product.product_to_dict() for product in query_data]
    return json.dumps(product_dict)