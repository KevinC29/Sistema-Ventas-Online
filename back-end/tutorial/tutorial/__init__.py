from pyramid.config import Configurator
from wsgicors import CORS


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    def get_root(request):
        return {}

    config = Configurator(root_factory=get_root, settings=settings)
    config.begin()
    config.include('.security')
    config.include('.routes')
    config.include('.routes_app')
    config.include('.models')
    # config.include('.cors')
    config.scan()
    config.end()

    return CORS(config.make_wsgi_app(), headers="*", methods="*", maxage="180", origin="*")

