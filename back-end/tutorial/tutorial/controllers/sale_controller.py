import json

def sale_to_json(query_data):
    sale_dict = [sale.sale_to_dict() for sale in query_data]
    return json.dumps(sale_dict)