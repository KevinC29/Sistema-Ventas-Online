def includeme(config):
    # product
    config.add_route('product_list', '/product/list/')
    # config.add_view(ProductListView, route_name='product_list', attr='get', renderer='json')
    config.add_route('product_create', '/product/add/')
    # config.add_view(ProductCreateView, route_name='product_create', attr='post', renderer='json')
    config.add_route('product_update', '/product/update/{pk}/')
    # config.add_view(ProductUpdateView, route_name='product_update', attr='put', renderer='json')
    config.add_route('product_delete', '/product/delete/{pk}/')
    # config.add_view(ProductDeleteView, route_name='product_delete', attr='delete', renderer='json')