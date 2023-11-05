from pyramid.view import view_config
from pyramid.response import Response

@view_config(route_name='dashboard')
def DashboardView(request):
    # Lógica para manejar la solicitud GET a '/category/list/'
    response = {
        'status': True,
        'msg': 'Bienvenido a la página de inicio'
    }
    return Response(json=response, status=200)