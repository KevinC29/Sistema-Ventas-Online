from pyramid.response import Response
from pyramid.view import view_config

from ..controllers.client_controller import (
    validate_data_none_client,
    validate_data_type_client,
    validate_data_gender_client,
    validate_data_balance_client,
    validate_exist_client,
    list_client,
    create_client,
    update_client,
    delete_client
)

from ..models import models

@view_config(route_name='client_list', request_method='GET')
def client_list(request):
    try:
        client_all = list_client(request)

        if client_all == True:
            return Response(
                json = {
                    'status': False,
                    "msg" : "error client list empty"
                }, 
                status = 404
            )
        else:
            return Response(
                json = {
                    'status': True,
                    "msg" : "succes",
                    "data" : client_all
                },
                status = 200
            )
        
        request.dbsession.close()
            
    except Exception as e:
        message = str(e)
        return Response(
            json={
                'status': False,
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

        if validate_data_none_client(names, surnames, dni, address, gender_value, balance):
            return Response(
                json={
                    'status': False,
                    "msg": "error data none"
                }, 
                status=400
            )
        elif validate_data_type_client(names, surnames, dni, address, gender_value, balance):
            return Response(
                json={
                    'status': False,
                    "msg": "error data type"
                }, 
                status=400
            )
        elif validate_data_gender_client(gender_value):
            return Response(
                json={
                    'status': False,
                    "msg": "error data gender"
                }, 
                status=400
            )
        elif validate_data_balance_client(balance) == True:
            return Response(
                json={
                    'status': False,
                    "msg": "error data balance negative"
                }, 
                status=400
            )
        else:
            balance_value = validate_data_balance_client(balance)
        
        response = create_client(request, names, surnames, dni, address, gender_value, balance_value)

        return Response(
            json={
                'status': True,
                "msg": "succes",
                "data": response
            }, 
            status=201
        )

        request.dbsession.commit()
        request.dbsession.close()

    except Exception as e:
        message = str(e)
        if 'llave duplicada' in message and 'uq_client_dni' in message:
            return Response(
                json={
                    'status': False,
                    'msg': 'duplicate'
                }, 
                status=409)
        else:
            return Response(
                json={
                    'status': False,
                    'msg': message
                }, 
                status=500)

@view_config(route_name='client_update', request_method='PUT')
def client_update(request):
    try:
        client_id = request.matchdict['pk']
        client = validate_exist_client(request, client_id)

        json_data = request.json_body

        names = json_data.get('names')
        surnames = json_data.get('surnames')
        dni = json_data.get('dni')
        address = json_data.get('address')
        gender_value = json_data.get('gender')
        balance = json_data.get('balance')

        if client == True:
            return Response(
                json = {
                    'status': False,
                    "msg" : "error client not exist"
                }, 
                status = 404
            )
        elif validate_data_none_client(names, surnames, dni, address, gender_value, balance):
            return Response(
                json={
                    'status': False,
                    "msg": "error data none"
                }, 
                status=400
            )
        elif validate_data_type_client(names, surnames, dni, address, gender_value, balance):
            return Response(
                json={
                    'status': False,
                    "msg": "error data type"
                }, 
                status=400
            )
        elif validate_data_gender_client(gender_value):
            return Response(
                json={
                    'status': False,
                    "msg": "error data gender"
                }, 
                status=400
            )
        elif validate_data_balance_client(balance) == True:
            return Response(
                json={
                    'status': False,
                    "msg": "error data balance negative"
                }, 
                status=400
            )
        else:
            balance_value = validate_data_balance_client(balance)
            
        response = update_client(request, client, names, surnames, dni, address, gender_value, balance_value)

        return Response(
            json={
                'status': True,
                "msg": "succes",
                "data": response
            }, 
            status=200
        )

        request.dbsession.commit()
        request.dbsession.close()

    except Exception as e:
        message = str(e)
        if 'llave duplicada' in message and 'uq_client_dni' in message:
            return Response(
                json={
                    'status': False,
                    'msg': 'duplicate'
                }, 
                status=409)
        else:
            return Response(
                json={
                    'status': False,
                    'msg': message
                }, 
                status=500)

@view_config(route_name='client_delete', request_method='DELETE')
def client_delete(request):
    try:
        client_id = request.matchdict['pk']
        client = delete_client(request, client_id)

        if client:
            return Response(
                json = {
                    'status': False,
                    "msg" : "error client not exist"
                }, 
                status = 404
            )
        else:
            return Response(
                json = {
                    'status': True,
                    "msg" : "ok"
                }, 
                status = 200
            )

        request.dbsession.commit()
        request.dbsession.close()        
            
    except Exception as e:
        message = str(e)
        return Response(
            json={
                'status': False,
                "msg": message
            },
            status=500
        )
