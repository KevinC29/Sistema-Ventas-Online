from sqlalchemy import (
    Column,
    ForeignKey,
)
import uuid
from enum import Enum
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import (
    UUID, 
    ENUM, 
    NUMERIC, 
    INTEGER, 
    TEXT,
    VARCHAR,
    DATE
)

from .meta import Base


class GenderEnum(Enum):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'


class Category(Base):
    __tablename__ = 'category'
    # id = Column(INTEGER, primary_key=True)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(VARCHAR(150), unique=True, doc='Nombre', nullable=False)
    desc = Column(TEXT, nullable=False, doc='Descripcion')

    def __str__(self):
        return self.name


class Product(Base):
    __tablename__ = 'product'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(VARCHAR(150), unique=True, doc='Nombre', nullable=False)
    image = Column(VARCHAR, nullable=True, doc='Imagen')  # Guardaremos las url de las imagenes
    stock = Column(INTEGER, default=0, doc='Stock')
    pvp = Column(NUMERIC(9, 2), default=0.00, doc='Precio de venta')

    cat_id = Column(UUID(as_uuid=True), ForeignKey('category.id', ondelete="CASCADE"))
    category = relationship("Category", backref="created_products")

    def __str__(self):
        return self.name


class Client(Base):
    __tablename__ = 'client'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    names = Column(VARCHAR(150), doc='Nombres', nullable=False)
    surnames = Column(VARCHAR(150), doc='Apellidos', nullable=False)
    dni = Column(VARCHAR(10), unique=True, doc='DNI', nullable=False)
    address = Column(VARCHAR(150), default='Direccion N/A', doc='Dirección')
    gender = Column(ENUM(GenderEnum), default=GenderEnum.MALE, doc='Genero')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} {} / {}'.format(self.names, self.surnames, self.dni)


class Sale(Base):
    __tablename__ = 'sale'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date_joined = Column(DATE, default=datetime.now, doc='Fecha de venta')
    subtotal = Column(NUMERIC(9, 2), default=0.00, doc='Subtotal')
    iva = Column(NUMERIC(9, 2), default=0.00, doc='IVA')
    total = Column(NUMERIC(9, 2), default=0.00, doc='Total')

    cli_id = Column(UUID(as_uuid=True), ForeignKey('client.id', ondelete="CASCADE"))
    client = relationship("Client", backref="created_sales")
    # det = relationship("DetSale", backref="sale")

    def __str__(self):
        return self.cli_id.names


class DetSale(Base):
    __tablename__ = 'det_sale'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    price = Column(NUMERIC(9, 2), default=0.00, doc='Precio')
    cant = Column(INTEGER, default=0, doc='Cantidad')
    subtotal = Column(NUMERIC(9, 2), default=0.00, doc='Subtotal')

    sale_id = Column(UUID(as_uuid=True), ForeignKey('sale.id', ondelete="CASCADE"))
    prod_id = Column(UUID(as_uuid=True), ForeignKey('product.id', ondelete="CASCADE"))
    sale = relationship("Sale", backref="created_detSales_sale")
    product = relationship("Product", backref="created_detSales_products")
    
    def __str__(self):
        return self.prod_id.name


# class Page(Base):
#     """ The SQLAlchemy declarative model class for a Page object. """
#     __tablename__ = 'pages'
#     id = Column(INTEGER, primary_key=True)
#     name = Column(TEXT, nullable=False, unique=True)
#     data = Column(TEXT, nullable=False)

#     user_id = Column(ForeignKey('users.id'), nullable=False)
#     creator = relationship('User', backref='created_pages')