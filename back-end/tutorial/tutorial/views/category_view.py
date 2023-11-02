from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPNotFound
)
# from pyramid.csrf import get_csrf_token
# from pyramid.session import check_csrf_token
from ..models import models

@view_config(route_name='category_list', request_method='GET')
def category_list(request):
    try:
        category_all = request.dbsession.query(models.Category).all()

        if not category_all:
            return Response(
                json = {
                    "msg" : "error"
                }, 
                status = 404
            )
        else:
            categories_json = [category.category_to_dict() for category in category_all]
            return Response(
                json = categories_json, 
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

    
@view_config(route_name='category_create', request_method='POST')
def category_create(request):
    try:
        json_data = request.json_body
        name = json_data.get('name')
        desc = json_data.get('desc')

        validate_None = any(value is None for value in (name, desc))

        if validate_None:
            return Response(
                json={
                    "msg": "error"
                }, 
                status=400
            )

        is_name_valid = isinstance(name, str)
        is_desc_valid = isinstance(desc, str)

        validate_Type = not all([is_name_valid, is_desc_valid])

        if validate_Type:
            return Response(
                json={
                    "msg": "error"
                }, 
                status=400
            )
            
        new_category = models.Category(
            name=name,
            desc=desc
        )

        request.dbsession.add(new_category)
        request.dbsession.flush()
        response = new_category.category_to_dict()

        return Response(
            json={
                "msg": "succes",
                "data": response
            }, 
            status=201
        )

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
        category = request.dbsession.query(models.Category).filter_by(id=category_id).first()

        if not category:
            return Response(
                json = {
                    "msg" : "error"
                }, 
                status = 404
            )
        else:
            json_data = request.json_body
            name = json_data.get('name')
            desc = json_data.get('desc')

            validate_None = any(value is None for value in (name, desc))

            if validate_None:
                return Response(
                    json={
                        "msg": "error"
                    }, 
                    status=400
                )

            is_name_valid = isinstance(name, str)
            is_desc_valid = isinstance(desc, str)

            validate_Type = not all([is_name_valid, is_desc_valid])

            if validate_Type:
                return Response(
                    json={
                        "msg": "error"
                    }, 
                    status=400
                )

            if category.name == name:
                category.desc = desc
            else:
                category.name = name
                category.desc = desc
            
            request.dbsession.flush()
            response = category.category_to_dict()

            return Response(
                json={
                    "msg": "succes",
                    "data": response
                }, 
                status=200
            )

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
        category = request.dbsession.query(models.Category).filter_by(id=category_id).first()

        if not category:
            return Response(
                json = {
                    "msg" : "error"
                }, 
                status = 404
            )
        else:
            request.dbsession.delete(category)
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
