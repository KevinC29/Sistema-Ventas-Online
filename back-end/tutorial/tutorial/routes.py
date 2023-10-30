# from .routes_app.category import includeme as category_routes
# from .routes_app.client import includeme as client_routes
# from .routes_app.product import includeme as product_routes
# from .routes_app.sale import includeme as sale_routes


def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    # config.add_route('view_wiki', '/')
    # config.add_route('view_page', '/{pagename}')
    # config.add_route('add_page', '/add_page/{pagename}')
    # config.add_route('edit_page', '/{pagename}/edit_page')

    # home
    config.add_route('dashboard', '/')
    # config.add_route('homepage', '/{pagename}')
    # config.add_view(DashboardView, route_name='dashboard')

    #Routes Includes
    # category_routes(config)
    # client_routes(config)
    # product_routes(config)
    # sale_routes(config)
