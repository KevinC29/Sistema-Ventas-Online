from pyramid.response import Response
from pyramid.view import view_config

from ..controllers.sale_controller import (
    validate_data_none_sale, 
    validate_data_type_sale,
    validate_exist_client,
    validate_data_subtotal_sale,
    validate_data_iva_sale,
    validate_data_total_sale,
    create_sale
)
from ..controllers.detSale_controller import (
    validate_data_list_detSale,
    create_detSale
)
from ..models import models
import uuid
from datetime import date


@view_config(route_name='sale_list', request_method='GET')
def sale_list(request):
    try:
        sale_all = request.dbsession.query(models.Sale).all()

        if not sale_all:
            return Response(
                json = {
                    "msg" : "error"
                }, 
                status = 404
            )
        else:
            sale_json = [sale.sale_to_dict() for sale in sale_all]
            return Response(
                json = sale_json, 
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

@view_config(route_name='sale_create', request_method='POST')
def sale_create(request):
    try:
        json_data = request.json_body

        date_joined = json_data.get('date_joined')
        subtotal = json_data.get('subtotal')
        iva = json_data.get('iva')
        total = json_data.get('total')
        cli_id = json_data.get('cli_id')
        detalle = json_data.get('det')

        if validate_data_none_sale(date_joined, subtotal, iva, total, cli_id, detalle):
            return Response(
                json={
                    "msg": "error data none"
                }, 
                status=400
            )
        elif validate_data_type_sale(date_joined, subtotal, iva, total, cli_id, detalle):
            return Response(
                json={
                    "msg": "error data type"
                }, 
                status=400
            )
        elif validate_exist_client(request, cli_id):
            return Response(
                json={
                    "msg": "error client not found"
                }, 
                status=404
            )
        
        data_values_sale = [validate_data_subtotal_sale(subtotal), 
            validate_data_iva_sale(iva), 
            validate_data_total_sale(total)]

        if any(data_values_sale):
            return Response(
                json={
                    "msg": "error data negative"
                }, 
                status=400
            )

        #validar datos de los detalles
        value, message = None, None
        if len(detalle) == 0:
            return Response(
                json={
                    "msg": "error lista de detalle vacia"
                }, 
                status=400
            )
        else :
            value, message = validate_data_list_detSale(detalle)
            if value == True and 'product' in message:
                return Response(
                        json={
                            "msg": message
                        }, 
                        status=404
                    )
            elif value == True:
                return Response(
                        json={
                            "msg": message
                        }, 
                        status=400
                    )
        
        # validar datos de la venta  
        if value != data_values_sale[0]:
            return Response(
                    json={
                        "msg": "error subtotal with sum detSale"
                    }, 
                    status=400
                )
        elif (data_values_sale[0] * data_values_sale[1])/100 != data_values_sale[2]:
            return Response(
                    json={
                        "msg": "error total with iva for subtotal"
                    }, 
                    status=400
                )
        else:

            new_sale = create_sale(request, date_joined, data_values_sale[0], data_values_sale[1], data_values_sale[2], cli_id)

            for det in detalle:
                prod_id = det.get('prod_id')
                price = det.get('price')
                cant = det.get('cant')
                subtotal = det.get('subtotal')
                create_detSale(request, price, cant, subtotal, prod_id, new_sale)
                
            response = new_sale.sale_to_dict()

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