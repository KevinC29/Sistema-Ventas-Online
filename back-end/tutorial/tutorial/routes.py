# from .routes_app.category import includeme as category_routes
# from .routes_app.client import includeme as client_routes
# from .routes_app.product import includeme as product_routes
# from .routes_app.sale import includeme as sale_routes

def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    # home
    config.add_route('dashboard', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')