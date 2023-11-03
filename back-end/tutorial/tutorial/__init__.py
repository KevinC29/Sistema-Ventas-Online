from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        # config.include('pyramid_jinja2')
        config.include('.security')
        config.include('.routes')
        config.include('.routes_app')
        config.include('.models')
        config.include('.cors')
        # make sure to add this before other routes to intercept OPTIONS
        config.add_cors_preflight_handler() #importacion adicional de cors
        config.scan()
    return config.make_wsgi_app()
