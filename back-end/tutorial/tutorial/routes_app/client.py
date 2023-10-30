def includeme(config):
    # client
    config.add_route('client_list', '/client/list/')
    # config.add_view(ClientListView, route_name='client_list', attr='get', renderer='json')
    config.add_route('client_create', '/client/add/')
    # config.add_view(ClientCreateView, route_name='client_create', attr='post', renderer='json')
    config.add_route('client_update', '/client/update/{pk}/')
    # config.add_view(ClientUpdateView, route_name='client_update', attr='put', renderer='json')
    config.add_route('client_delete', '/client/delete/{pk}/')
    # config.add_view(ClientDeleteView, route_name='client_delete', attr='delete', renderer='json')