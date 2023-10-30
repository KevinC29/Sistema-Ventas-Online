import json

def categoy_to_json(query_data):
    categories_dict = [category.category_to_dict() for category in query_data]
    return json.dumps(categories_dict)
