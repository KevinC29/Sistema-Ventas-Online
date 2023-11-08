from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPNotFound
)

from ..controllers.user_controller import (
    validate_data_none_user, 
    validate_data_type_user,
    validate_data_role_user,
    validate_exist_user,
    list_user,
    create_user,
    update_user,
    delete_user
)

from ..models import models

@view_config(route_name='user_list', request_method='GET')
def user_list(request):
    try:
        user_all = list_user(request)
        
        if user_all == True:
            return Response(
                json = {
                    'status': False,
                    "msg" : "error user list empty"
                }, 
                status = 404
            )
        else:
            return Response(
                json = {
                    'status': True,
                    "msg" : "succes",
                    "data" : user_all
                }, 
                status = 200
            )
        
        request.dbsession.close()
        
    except Exception as e:
        message = str(e)
        return Response(
            json={
                "msg": message
            },
            status=500
        )
    
@view_config(route_name='user_create', request_method='POST')
def user_create(request):
    try:
        json_data = request.json_body

        name = json_data.get('name')
        role = json_data.get('role')
        password_hash = json_data.get('password_hash')

        
        if validate_data_none_user(name, role, password_hash):
            return Response(
                json={
                    'status': False,
                    "msg": "error data none"
                }, 
                status=400
            )
        elif validate_data_type_user(name, role, password_hash):
            return Response(
                json={
                    'status': False,
                    "msg": "error data type"
                }, 
                status=400
            )
        elif validate_data_role_user(role):
            return Response(
                json={
                    'status': False,
                    "msg": "error type role"
                }, 
                status=400
            )
        
        response = create_user(request, name, role, password_hash)

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
        if 'llave duplicada' in message and 'uq_users_name' in message:
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

@view_config(route_name='user_update', request_method='PUT')
def user_update(request):
    try:
        user_id = request.matchdict['pk']
        user = validate_exist_user(request, user_id)

        json_data = request.json_body
            
        name = json_data.get('name')
        role = json_data.get('role')
        password_hash = json_data.get('password_hash')

        if user == True:
            return Response(
                json = {
                    'status': False,
                    "msg" : "error user not exist"
                }, 
                status = 404
            )
        elif validate_data_none_user(name, role, password_hash):
            return Response(
                json={
                    'status': False,
                    "msg": "error data none"
                }, 
                status=400
            )
        elif validate_data_type_user(name, role, password_hash):
            return Response(
                json={
                    'status': False,
                    "msg": "error data type"
                }, 
                status=400
            )
        elif validate_data_role_user(role):
            return Response(
                json={
                    'status': False,
                    "msg": "error type role"
                }, 
                status=400
            )
    
        response = update_user(request, user, name, role, password_hash)

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
        if 'llave duplicada' in message and 'uq_users_name' in message:
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

@view_config(route_name='user_delete', request_method='DELETE')
def user_delete(request):
    try:
        user_id = request.matchdict['pk']
        user = delete_user(request, user_id)

        if user:
            return Response(
                json = {
                    'status': False,
                    "msg" : "error user not exist"
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