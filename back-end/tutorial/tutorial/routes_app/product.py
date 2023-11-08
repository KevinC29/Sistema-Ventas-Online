def includeme(config):
    # product
    config.add_route('product_list', '/product/list/')
    config.add_route('product_create', '/product/add/')
    config.add_route('product_update', '/product/update/{pk}/')
    config.add_route('product_delete', '/product/delete/{pk}/')