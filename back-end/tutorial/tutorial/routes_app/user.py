def includeme(config):
    # user
    config.add_route('user_list', '/user/list/')
    config.add_route('user_create', '/user/add/')
    config.add_route('user_update', '/user/update/{pk}/')
    config.add_route('user_delete', '/user/delete/{pk}/')