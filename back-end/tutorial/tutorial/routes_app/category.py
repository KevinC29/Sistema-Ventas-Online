def includeme(config):
    # category
    config.add_route('category_list', '/category/list/')
    config.add_route('category_create', '/category/add/')
    config.add_route('category_update', '/category/update/{pk}/')
    config.add_route('category_delete', '/category/delete/{pk}/')
