def includeme(config):
    # sale
    config.add_route('sale_list', '/sale/list/')
    config.add_route('sale_create', '/sale/add/')
    config.add_route('sale_update', '/sale/update/{pk}/')
    config.add_route('sale_delete', '/sale/delete/{pk}/')