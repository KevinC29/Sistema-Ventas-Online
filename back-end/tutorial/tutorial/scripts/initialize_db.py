import argparse
import sys
import uuid

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import OperationalError

from .. import models


def setup_models(dbsession):
    """
    Add or update models / fixtures in the database.

    """
    editor = models.User(name='editor', role='editor')
    editor.set_password('editor123')
    dbsession.add(editor)

    basic = models.User(name='basic', role='basic')
    basic.set_password('basic123')
    dbsession.add(basic)

    # page = models.Page(
    #     name='FrontPage',
    #     creator=editor,
    #     data='This is the front page',
    # )

    category = models.Category(
        id=uuid.uuid4(),  # Generar un UUID aleatorio para el ID
        name="Carnes",
        desc="Cualquier tipo de carne"
    )
    product = models.Product(
        id=uuid.uuid4(),  # Generar un UUID aleatorio para el ID
        name="Product 1",
        image="URL_imagen_1",
        stock=10,
        pvp=49.99,
        category=category  # Asociamos el producto a la categoría previamente creada
    )

    client = models.Client(
        id=uuid.uuid4(),  # Generar un UUID aleatorio para el ID
        names="John",
        surnames="Doe",
        dni="1234567890",
        address="123 Loja" # Establecer el género como MALE desde el Enum
    )

    dbsession.add(category)
    dbsession.add(product)
    dbsession.add(client)
    # dbsession.add(page)



def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri',
        help='Configuration file, e.g., development.ini',
    )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)

    try:
        with env['request'].tm:
            dbsession = env['request'].dbsession
            setup_models(dbsession)
    except OperationalError:
        print('''
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for description and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.
            ''')
