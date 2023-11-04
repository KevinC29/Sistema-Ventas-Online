from pyramid.response import Response
from pyramid.view import view_config

from ..controllers.product_controller import (
    validate_url,
    validate_data_none_product,
    validate_data_type_product,
    validate_exist_product,
    validate_exist_category,
    validate_data_stock_product,
    validate_data_pvp_product,
    list_product,
    create_product,
    update_product,
    delete_product
)
from ..models import models

@view_config(route_name='product_list', request_method='GET')
def product_list(request):
    try:
        product_all = list_product(request)

        if product_all == True:
            return Response(
                json = {
                    "msg" : "error product list empty"
                }, 
                status = 404
            )
        else:
            return Response(
                json = {
                    "msg" : "succes",
                    "data" : product_all
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

@view_config(route_name='product_create', request_method='POST')
def product_create(request):
    try:
        json_data = request.json_body

        name = json_data.get('name')
        image = json_data.get('image')
        stock = json_data.get('stock')
        pvp = json_data.get('pvp')
        cat_id = json_data.get('cat_id')

        if validate_data_none_product(name, image, stock, pvp, cat_id):
            return Response(
                json={
                    "msg": "error data none"
                }, 
                status=400
            )
        elif validate_data_type_product(name, image, stock, pvp, cat_id):
            return Response(
                json={
                    "msg": "error data type"
                }, 
                status=400
            )
        elif validate_url(image):
            return Response(
                json={
                    "msg": "error img url not valid or not found"
                }, 
                status=404
            )
        elif validate_exist_category(request, cat_id):
            return Response(
                json={
                    "msg": "error category not found"
                }, 
                status=404
            )
        elif validate_data_stock_product(stock) or validate_data_pvp_product(pvp) == True:
            return Response(
                json={
                    "msg": "error data negative"
                }, 
                status=400
            )
        else:
            pvp_value = validate_data_pvp_product(pvp)
            
        response = create_product(request, name, image, stock, pvp_value, cat_id)

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
        if 'llave duplicada' in message and 'uq_product_name' in message:
            return Response(
                json={
                    'msg': 'duplicate'
                }, 
                status=409)
        elif 'UUID' in message:
            return Response(
                json={
                    'msg': 'uuid error'
                }, 
                status=400)
        else :
            return Response(
                json={
                    'msg': message
                }, 
                status=500)

@view_config(route_name='product_update', request_method='PUT')
def product_update(request):
    try:
        product_id = request.matchdict['pk']
        product = validate_exist_product(request, product_id)

        json_data = request.json_body

        name = json_data.get('name')
        image = json_data.get('image')
        stock = json_data.get('stock')
        pvp = json_data.get('pvp')
        cat_id = json_data.get('cat_id')

        if product == True:
            return Response(
                json={
                    "msg": "error product not found"
                }, 
                status=404
            )
        elif validate_data_none_product(name, image, stock, pvp, cat_id):
            return Response(
                json={
                    "msg": "error data none"
                }, 
                status=400
            )
        elif validate_data_type_product(name, image, stock, pvp, cat_id):
            return Response(
                json={
                    "msg": "error data type"
                }, 
                status=400
            )
        elif validate_url(image):
            return Response(
                json={
                    "msg": "error img url not valid or not found"
                }, 
                status=404
            )
        elif validate_exist_category(request, cat_id):
            return Response(
                json={
                    "msg": "error category not found"
                }, 
                status=404
            )
        elif validate_data_stock_product(stock) or validate_data_pvp_product(pvp) == True:
            return Response(
                json={
                    "msg": "error data negative"
                }, 
                status=400
            )
        else:
            pvp_value = validate_data_pvp_product(pvp)
            
        response = update_product(request, product, name, image, stock, pvp_value, cat_id)

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
        if 'llave duplicada' in message and 'uq_product_name' in message:
            return Response(
                json={
                    'msg': 'duplicate'
                }, 
                status=409)
        elif 'UUID' in message:
            return Response(
                json={
                    'msg': 'uuid error'
                }, 
                status=400)
        else :
            return Response(
                json={
                    'msg': message
                }, 
                status=500)

@view_config(route_name='product_delete', request_method='DELETE')
def product_delete(request):
    try:
        product_id = request.matchdict['pk']
        product = delete_product(request, product_id)

        if product:
            return Response(
                json = {
                    "msg" : "error product not exist"
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
