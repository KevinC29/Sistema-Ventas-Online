from pyramid.response import Response
from pyramid.view import view_config
from ..controllers.category_controller import categoy_to_json

from ..models import models

# @view_config(accept='application/json')
@view_config(route_name='category_list', request_method='GET')
def category_list(request):

    try:
        category_all = request.dbsession.query(models.Category).all()
        categories_json = categoy_to_json(category_all)
        return Response(json=categories_json, content_type='application/json')
    except Exception as e:
        response_data = []
        return Response(json=response_data, content_type='application/json')
    
    
    


# json_data = request.json_body
# La vista de creación de una categoría

# @view_config(route_name='category_create', request_method='POST')
# def category_create(request):
#     data = {}
#     try:
#         action = request.POST.get('action')
#         if action == 'add':
#             form = CategoryForm(request.POST)
#             if form.validate():
#                 data = form.save()
#             else:
#                 data['error'] = form.errors
#         else:
#             data['error'] = 'No ha ingresado a ninguna opción'
#     except Exception as e:
#         data['error'] = str(e)
#     return Response(json=data)

# # La vista de actualización de una categoría
# @view_config(route_name='category_update', request_method='POST')
# def category_update(request):
#     data = {}
#     try:
#         action = request.POST.get('action')
#         if action == 'edit':
#             category_id = int(request.matchdict['id'])
#             category = Category.query.get(category_id)
#             form = CategoryForm(request.POST)
#             if form.validate():
#                 data = form.save()
#             else:
#                 data['error'] = form.errors
#         else:
#             data['error'] = 'No ha ingresado a ninguna opción'
#     except Exception as e:
#         data['error'] = str(e)
#     return Response(json=data)

# # La vista de eliminación de una categoría
# @view_config(route_name='category_delete', request_method='POST')
# def category_delete(request):
#     data = {}
#     try:
#         category_id = int(request.matchdict['id'])
#         category = Category.query.get(category_id)
#         category.delete()
#     except Exception as e:
#         data['error'] = str(e)
#     return Response(json=data)
