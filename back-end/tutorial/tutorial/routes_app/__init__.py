# En routes_app/__init__.py

from . import category, client, product, sale  # Importa los módulos que contienen las rutas

def includeme(config):
    # Llamando a las funciones includeme de cada módulo
    category.includeme(config)
    client.includeme(config)
    product.includeme(config)
    sale.includeme(config)