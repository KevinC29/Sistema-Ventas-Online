from pyramid.view import notfound_view_config


@notfound_view_config(renderer='json')
def notfound_view(request):
    request.response.status = 404
    data = {'message': 'page not found'}
    return data
