from pyramid.csrf import new_csrf_token
from pyramid.httpexceptions import HTTPSeeOther
from pyramid.security import (
    remember,
    forget,
)
from pyramid.response import Response
from pyramid.view import (
    forbidden_view_config,
    view_config,
)

from .. import models


@view_config(route_name='login')
def login(request):
    if request.content_type != 'application/json':
        return Response('Unsupported Media Type', status=415)
    message = ''
    login = ''
    status_code = 200
    csrf_token = None  

    if request.method == 'POST':
        print("Entro al post")
        try:
            print(request.body)
            json_data = request.json_body
            
            login = json_data.get('login')
            password = json_data.get('password')
        except ValueError:
            return Response('Invalid JSON', status=400)

        user = (
            request.dbsession.query(models.User)
            .filter_by(name=login)
            .first()
        )
        print("Este es el token1")
        if user is not None and user.check_password(password):
            # csrf_token = new_csrf_token(request)
            headers = remember(request, user.id)
            # return HTTPSeeOther(location=next_url, headers=headers)
            message = 'OK'
            status_code = 200
            # print("Este es el token")
        else:
            message = 'Failed login'
            status_code = 400 
    return Response(json_body={
                'message': message,
                'url': request.route_url('login'),
                'login': login,
                # 'token': csrf_token
            }, status=status_code)


@view_config(route_name='logout')
def logout(request):
    next_url = request.route_url('dashboard')
    if request.method == 'POST':
        new_csrf_token(request)
        headers = forget(request)
        return HTTPSeeOther(location=next_url, headers=headers)

    return HTTPSeeOther(location=next_url)

@forbidden_view_config(renderer='tutorial:templates/403.jinja2')
def forbidden_view(exc, request):
    if not request.is_authenticated:
        next_url = request.route_url('login', _query={'next': request.url})
        return HTTPSeeOther(location=next_url)

    request.response.status = 403
    return {}