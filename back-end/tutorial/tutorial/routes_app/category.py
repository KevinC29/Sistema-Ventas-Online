def includeme(config):
    # category
    config.add_route('category_list', '/category/list/')
    # config.add_view(CategoryListView, route_name='category_list', attr='get', renderer='json')
    config.add_route('category_create', '/category/add/')
    # config.add_view(CategoryCreateView, route_name='category_create', attr='post', renderer='json')
    config.add_route('category_update', '/category/update/{pk}/')
    # config.add_view(CategoryUpdateView, route_name='category_update', attr='put', renderer='json')
    config.add_route('category_delete', '/category/delete/{pk}/')
    # config.add_view(CategoryDeleteView, route_name='category_delete', attr='delete', renderer='json')
