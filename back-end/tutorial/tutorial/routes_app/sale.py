def includeme(config):
    # sale
    config.add_route('sale_list', '/sale/list/')
    # config.add_view(SaleListView, route_name='sale_list', attr='get', renderer='json')
    config.add_route('sale_create', '/sale/add/')
    # config.add_view(SaleCreateView, route_name='sale_create', attr='post', renderer='json')
    config.add_route('sale_update', '/sale/update/{pk}/')
    # config.add_view(SaleUpdateView, route_name='sale_update', attr='put', renderer='json')
    config.add_route('sale_delete', '/sale/delete/{pk}/')
    # config.add_view(SaleDeleteView, route_name='sale_delete', attr='delete', renderer='json')