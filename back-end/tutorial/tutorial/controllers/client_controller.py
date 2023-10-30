import json

def client_to_json(query_data):
    clients_dict = [client.client_to_dict() for client in query_data]
    return json.dumps(clients_dict)