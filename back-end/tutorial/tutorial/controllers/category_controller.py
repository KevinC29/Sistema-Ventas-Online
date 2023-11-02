import json

from .utils import response_json

def collection_to_json(query_data):
    categories_dict = [category.category_to_dict() for category in query_data]
    return response_json("Lista de categorias", categories_dict)

