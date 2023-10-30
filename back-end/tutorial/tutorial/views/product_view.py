from pyramid.response import Response
from pyramid.view import view_config
from ..controllers.product_controller import product_to_json

from ..models import models

# @view_config(accept='application/json')
@view_config(route_name='product_list', request_method='GET')
def product_list(request):
    try:
        product_all = request.dbsession.query(models.Product).all()
        products_json = product_to_json(product_all)
        return Response(json=products_json, content_type='application/json')
    except Exception as e:
        response_data = []
        return Response(json=response_data, content_type='application/json')