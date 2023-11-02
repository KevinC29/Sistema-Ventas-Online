from pyramid.response import Response
from pyramid.view import view_config

from ..models import models


@view_config(route_name='client_list', request_method='GET')
def client_list(request):
    try:
        client_all = request.dbsession.query(models.Client).all()

        if not client_all:
            return Response(
                json = {
                    "msg" : "error"
                }, 
                status = 404
            )
        else:
            clients_json = [client.client_to_dict() for client in client_all]
            return Response(
                json = clients_json, 
                status = 200
            )
    except Exception as e:
        message = str(e)
        return Response(
            json={
                "msg": message
            },
            status=500
        )


@view_config(route_name='client_create', request_method='POST')
def client_create(request):
    try:
        json_data = request.json_body
        names = json_data.get('names')
        surnames = json_data.get('surnames')
        dni = json_data.get('dni')
        address = json_data.get('address')
        gender_value = json_data.get('gender')
        balance = json_data.get('balance')

        validate_None = any(value is None for value in (names, surnames, dni, address, gender_value, balance))

        if validate_None :
            return Response(
                json={
                    "msg": "error"
                }, 
                status=400
            )

        is_names_valid = isinstance(names, str)
        is_surnames_valid = isinstance(surnames, str)
        is_dni_valid = isinstance(dni, str)
        is_address_valid = isinstance(address, str)
        is_balance_valid = isinstance(balance, (int, float))

        validate_Type = not all([is_names_valid, is_surnames_valid, is_dni_valid, is_address_valid, is_balance_valid])
        
        if validate_Type :
            return Response(
                json={
                    "msg": "error"
                }, 
                status=400
            )

        validate_gender = not gender_value in [e.value for e in models.GenderEnum]

        if validate_gender:
            return Response(
                json={
                    "msg": "error gender"
                }, 
                status=400
            )
            
        new_client = models.Client(
            names= names,
            surnames= surnames,
            dni= dni,
            address = address,
            gender= models.GenderEnum(gender_value),
            balance= round(float(balance),2)
        )

        request.dbsession.add(new_client)
        request.dbsession.flush()
        response = new_client.client_to_dict()

        return Response(
            json={
                "msg": "succes",
                "data": response
            }, 
            status=201
        )

    except Exception as e:
        message = str(e)
        if 'llave duplicada' in message and 'uq_client_dni' in message:
            return Response(
                json={
                    'msg': 'duplicate'
                }, 
                status=409)
        else:
            return Response(
                json={
                    'msg': message
                }, 
                status=500)


@view_config(route_name='client_update', request_method='PUT')
def client_update(request):
    try:
        client_id = request.matchdict['pk']
        client = request.dbsession.query(models.Client).filter_by(id=client_id).first()

        if not client:
            return Response(
                json = {
                    "msg" : "error"
                }, 
                status = 404
            )
        else:
            json_data = request.json_body
            names = json_data.get('names')
            surnames = json_data.get('surnames')
            dni = json_data.get('dni')
            address = json_data.get('address')
            gender_value = json_data.get('gender')
            balance = json_data.get('balance')

            validate_None = any(value is None for value in (names, surnames, dni, address, gender_value, balance))

            if validate_None :
                return Response(
                    json={
                        "msg": "error"
                    }, 
                    status=400
                )

            is_names_valid = isinstance(names, str)
            is_surnames_valid = isinstance(surnames, str)
            is_dni_valid = isinstance(dni, str)
            is_address_valid = isinstance(address, str)
            is_balance_valid = isinstance(balance, (float))

            validate_Type = not all([is_names_valid, is_surnames_valid, is_dni_valid, is_address_valid, is_balance_valid])
        
            if validate_Type :
                return Response(
                    json={
                        "msg": "error"
                    }, 
                    status=400
                )

            validate_gender = not gender_value in [e.value for e in models.GenderEnum]

            if validate_gender:
                return Response(
                    json={
                        "msg": "error gender"
                    }, 
                    status=400
                )
            
            print(models.GenderEnum(gender_value))
            if client.dni == dni:
                client.names = names
                client.surnames = surnames
                client.address = address
                client.gender = models.GenderEnum(gender_value)
                client.balance = round(float(balance),2)
            else:
                client.names = names
                client.surnames = surnames
                client.dni = dni
                client.address = address
                client.gender = models.GenderEnum(gender_value)
                client.balance = round(float(balance),2)

            request.dbsession.flush()
            response = client.client_to_dict()

            return Response(
                json={
                    "msg": "succes",
                    "data": response
                }, 
                status=200
            )

    except Exception as e:
        message = str(e)
        if 'llave duplicada' in message and 'uq_client_dni' in message:
            return Response(
                json={
                    'msg': 'duplicate'
                }, 
                status=409)
        else:
            return Response(
                json={
                    'msg': message
                }, 
                status=500)


@view_config(route_name='client_delete', request_method='DELETE')
def client_delete(request):
    try:
        client_id = request.matchdict['pk']
        client = request.dbsession.query(models.Client).filter_by(id=client_id).first()

        if not client:
            return Response(
                json = {
                    "msg" : "error"
                }, 
                status = 404
            )
        else:
            request.dbsession.delete(client)
            request.dbsession.flush()

            return Response(
                status = 204
            )
    except Exception as e:
        message = str(e)
        return Response(
            json={
                "msg": message
            },
            status=500
        )
