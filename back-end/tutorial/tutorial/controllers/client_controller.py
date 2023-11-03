from ..models import models


def validate_data_none_client(names, surnames, dni, address, gender_value, balance):
    validate_None = any(value is None for value in (names, surnames, dni, address, gender_value, balance))
    return validate_None
    
def validate_data_type_client(names, surnames, dni, address, gender_value, balance):
    is_names_valid = isinstance(names, str)
    is_surnames_valid = isinstance(surnames, str)
    is_dni_valid = isinstance(dni, str)
    is_address_valid = isinstance(address, str)
    is_balance_valid = isinstance(balance, (int, float))
    validate_Type = not all([is_names_valid, is_surnames_valid, is_dni_valid, is_address_valid, is_balance_valid])
    return validate_Type

def validate_data_gender_client(gender):
    validate_gender = not gender in [e.value for e in models.GenderEnum]
    return validate_gender

def validate_data_balance_client(balance):
    balance_value = round(float(balance),2)
    validate_Balance = not balance_value >= 0
    if validate_Balance:
        return True
    else:
        return balance_value

def validate_exist_client(request, client_id):
    client = request.dbsession.query(models.Client).filter_by(id=client_id).first()
    if not client:
        return True
    else: 
        return client

def list_client(request):
    client_all = request.dbsession.query(models.Client).all()
    if not client_all:
        return True
    else:
        clients_json = [client.client_to_dict() for client in client_all]
        return clients_json
            
def create_client(request, names, surnames, dni, address, gender_value, balance):

    new_client = models.Client(
        names= names,
        surnames= surnames,
        dni= dni,
        address = address,
        gender= models.GenderEnum(gender_value),
        balance= balance
    )

    request.dbsession.add(new_client)
    request.dbsession.flush()

    return new_client.client_to_dict()

def update_client(request, client, names, surnames, dni, address, gender_value, balance_value):
    if client.dni == dni:
        client.names = names
        client.surnames = surnames
        client.address = address
        client.gender = models.GenderEnum(gender_value)
        client.balance = balance_value
    else:
        client.names = names
        client.surnames = surnames
        client.dni = dni
        client.address = address
        client.gender = models.GenderEnum(gender_value)
        client.balance = balance_value
    request.dbsession.flush()
    return client.client_to_dict()

def delete_client(request, client_id):
    client = validate_exist_client(request, client_id)
    if client == True:
        return True
    else:
        request.dbsession.delete(client)
        request.dbsession.flush()
        return False