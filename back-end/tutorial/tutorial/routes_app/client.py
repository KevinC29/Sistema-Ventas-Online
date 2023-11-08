def includeme(config):
    # client
    config.add_route('client_list', '/client/list/')
    config.add_route('client_create', '/client/add/')
    config.add_route('client_update', '/client/update/{pk}/')
    config.add_route('client_delete', '/client/delete/{pk}/')