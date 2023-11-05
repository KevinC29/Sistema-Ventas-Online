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

@view_config(route_name='login', request_method='POST')
def login(request):
    try:
        json_data = request.json_body
        username = json_data.get('username')
        password = json_data.get('password')

        user = request.dbsession.query(models.User).filter_by(name=username).first()
        
        if user is not None and user.check_password(password):
            # csrf_token = new_csrf_token(request)
            next_url = request.route_url('dashboard')
            headers = remember(request, user.id)
            response = {
                'status': True,
                'msg': 'ok',
                'next_url': next_url,
                'data': user.user_to_dict()
                # 'token': csrf_token
            }
            return Response(json=response, status=200, headers=headers)
        else:
            next_url = request.route_url('login')
            response = {
                'status': False,
                'msg': 'Failed login',
                'next_url': next_url
                # 'token': csrf_token
            }
            return Response(json=response, status=400)

    except Exception as e:
        message = str(e)
        return Response(
            json={
                'status': False,
                "msg": message
            },
            status=500
        )


@view_config(route_name='logout', request_method='GET')
def logout(request):
    next_url = request.route_url('dashboard')
    # new_csrf_token(request)
    print(request.method)
    if request.method != 'GET':
        response = {
            'status': False,
            'msg': 'Failed Logout',
            'next_url': next_url
            # 'token': csrf_token
        }
        return Response(json=response)
    else:
        next_url = request.route_url('login')
        headers = forget(request)
        response = {
            'status': True,
            'msg': 'ok',
            'next_url': next_url
            # 'token': csrf_token
        }
        return Response(json=response, headers=headers)

@forbidden_view_config(renderer='json')
def forbidden_view(exc, request):
    if not request.is_authenticated:
        next_url = request.route_url('login', _query={'next': request.url})
        return HTTPSeeOther(location=next_url)

    request.response.status = 403
    data = {'msg': 'access denied'}
    return data