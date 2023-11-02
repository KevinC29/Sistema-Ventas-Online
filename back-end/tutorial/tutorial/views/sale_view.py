# from pyramid.response import Response
# from pyramid.view import view_config
# from ..controllers.sale_controller import sale_to_json
# from pyramid.httpexceptions import (
#     HTTPNotFound,
#     HTTPSeeOther,
# )

# from ..models import models

# # @view_config(accept='application/json')
# @view_config(route_name='sale_list', request_method='GET')
# def sale_list(request):
#     sale_all = request.dbsession.query(models.Sale).all()
#     if not sale_all:
#         raise HTTPNotFound('No such page')        
#     sales_json = sale_to_json(sale_all)
#     return Response(json=sales_json, content_type='application/json', status=200)