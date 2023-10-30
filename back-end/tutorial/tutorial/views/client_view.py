from pyramid.response import Response
from pyramid.view import view_config
from ..controllers.client_controller import client_to_json

from ..models import models

# @view_config(accept='application/json')
@view_config(route_name='client_list', request_method='GET')
def client_list(request):
    try:
        client_all = request.dbsession.query(models.Client).all()
        clients_json = client_to_json(client_all)
        return Response(json=clients_json, content_type='application/json')
    except Exception as e:
        response_data = []
        return Response(json=response_data, content_type='application/json')


    