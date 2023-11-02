import json

def response_json(message, response):
    response = { 
        "message": message,
        "data": response
    }
    return json.dumps(response)