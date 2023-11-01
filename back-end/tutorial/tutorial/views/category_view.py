from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPNotFound,
    # HTTPSeeOther,
)
# from pyramid.csrf import get_csrf_token
# from pyramid.session import check_csrf_token
from ..controllers.category_controller import categoy_to_json

from ..models import models

# @view_config(accept='application/json')
@view_config(route_name='category_list', request_method='GET')
def category_list(request):
    category_all = request.dbsession.query(models.Category).all()
    if not category_all:
        raise HTTPNotFound('No such page')        
    categories_json = categoy_to_json(category_all)
    return Response(json=categories_json, content_type='application/json', status=200)
    
# La vista de creación de una categoría

@view_config(route_name='category_create', request_method='POST')
def category_create(request):
    try:
        json_data = request.json_body
        name = json_data.get('name')
        desc = json_data.get('desc')

        if name is None or desc is None:
            raise HTTPForbidden('No se puede crear una categoría sin nombre o descripción')
        elif not isinstance(name, str) or not isinstance(desc, str):
            raise HTTPForbidden('El tipo de dato de nombre o descripción no es válido')

        new_category = models.Category(
            name=name,
            desc=desc
        )

        request.dbsession.add(new_category)
        request.dbsession.flush()
        response = new_category.category_to_dict()
        return Response(json=response, status=201)

    except Exception as e:

        return Response(str(e), content_type='text/plain', status=500)

# La vista de actualización de una categoría
@view_config(route_name='category_update', request_method='PUT')
def category_update(request):
    try:
        category_id = request.matchdict['pk']
        category = request.dbsession.query(models.Category).filter_by(id=category_id).one()
        if category:
            json_data = request.json_body
            name = json_data.get('name')
            desc = json_data.get('desc')

            if name is None or desc is None:
                raise HTTPForbidden('No se puede editar una categoría sin nombre o descripción')
            elif not isinstance(name, str) or not isinstance(desc, str):
                raise HTTPForbidden('El tipo de dato de nombre o descripción no es válido')
                
            category.name = name
            category.desc = desc

            request.dbsession.flush()
            response = category.category_to_dict()

            return Response(json=response, status=200)
        else:
            return Response({'Category not found'}, status=404)

    except Exception as e:

        return Response(str(e), content_type='text/plain', status=500)

# La vista de eliminación de una categoría
@view_config(route_name='category_delete', request_method='DELETE')
def category_delete(request):
    try:
        category_id = request.matchdict['pk']
        category = request.dbsession.query(models.Category).filter_by(id=category_id).one()
        if category:
            
            request.dbsession.delete(category)
            request.dbsession.flush()

            return Response({'Category deleted successfully'}, status=204)
        else:
            return Response({'Category not found'}, status=404)

    except Exception as e:

        return Response(str(e), content_type='text/plain', status=500)
