from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPNotFound
)

from ..controllers.category_controller import (
    validate_data_none_category, 
    validate_data_type_category,
    validate_exist_category,
    list_category,
    create_category,
    update_category,
    delete_category
)
# from pyramid.csrf import get_csrf_token
# from pyramid.session import check_csrf_token
from ..models import models

@view_config(route_name='category_list', request_method='GET')
def category_list(request):
    try:
        category_all = list_category(request)
        
        if category_all == True:
            return Response(
                json = {
                    "msg" : "error category list empty"
                }, 
                status = 404
            )
        else:
            return Response(
                json = category_all, 
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
    
@view_config(route_name='category_create', request_method='POST')
def category_create(request):
    try:
        json_data = request.json_body

        name = json_data.get('name')
        desc = json_data.get('desc')
        
        if validate_data_none_category(name, desc):
            return Response(
                json={
                    "msg": "error data none"
                }, 
                status=400
            )
        elif validate_data_type_category(name, desc):
            return Response(
                json={
                    "msg": "error data type"
                }, 
                status=400
            )
            
        response = create_category(request, name, desc)

        return Response(
            json={
                "msg": "succes",
                "data": response
            }, 
            status=201
        )

        request.dbsession.commit()
        request.dbsession.close()

    except Exception as e:
        message = str(e)
        if 'llave duplicada' in message and 'uq_category_name' in message:
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

@view_config(route_name='category_update', request_method='PUT')
def category_update(request):
    try:
        category_id = request.matchdict['pk']
        category = validate_exist_category(request, category_id)

        json_data = request.json_body
            
        name = json_data.get('name')
        desc = json_data.get('desc')

        if category == True:
            return Response(
                json = {
                    "msg" : "error category not exist"
                }, 
                status = 404
            )
        elif validate_data_none_category(name, desc):
            return Response(
                json={
                    "msg": "error data none"
                }, 
                status=400
            )
        elif validate_data_type_category(name, desc):
            return Response(
                json={
                    "msg": "error data type"
                }, 
                status=400
            )
    
        response = update_category(request, category, name, desc)

        return Response(
            json={
                "msg": "succes",
                "data": response
            }, 
            status=200
        )

        request.dbsession.commit()
        request.dbsession.close()

    except Exception as e:
        message = str(e)
        if 'llave duplicada' in message and 'uq_category_name' in message:
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


@view_config(route_name='category_delete', request_method='DELETE')
def category_delete(request):
    try:
        category_id = request.matchdict['pk']
        category = delete_category(request, category_id)

        if category:
            return Response(
                json = {
                    "msg" : "error category not exist"
                }, 
                status = 404
            )
        else:
            return Response(
                status = 204
            )

        request.dbsession.commit()
        request.dbsession.close()
            
    except Exception as e:
        message = str(e)
        return Response(
            json={
                "msg": message
            },
            status=500
        )