import requests
import uuid
from ..models import models

def validate_url(url):
    try:
        response = requests.head(url)  # Realiza una solicitud HEAD para obtener solo los encabezados
        content_type = response.headers.get('content-type')  # Obtiene el tipo MIME del recurso
        # Verifica si el recurso tiene un tipo MIME que corresponde a una imagen
        return not ('image' in content_type)
    except Exception as e:
        return False  # Si hay un error al realizar la solicitud, retorna False

def validate_data_none_product(name, image, stock, pvp, cat_id):
    validate_None = any(value is None for value in (name, image, stock, pvp, cat_id))
    return validate_None
    
def validate_data_type_product(name, image, stock, pvp, cat_id):
    is_name_valid = isinstance(name, str)
    is_image_valid = isinstance(image, str)
    is_stock_valid = isinstance(stock, int)
    is_pvp_valid = isinstance(pvp, (int, float))
    is_cat_id_valid = isinstance(uuid.UUID(str(cat_id)) if isinstance(cat_id, str) else None, uuid.UUID)
    validate_Type = not all([is_name_valid, is_image_valid, is_stock_valid, is_pvp_valid, is_cat_id_valid])
    return validate_Type

def validate_exist_product(request, product_id):
    product = request.dbsession.query(models.Product).filter_by(id=product_id).first()
    if not product:
        return True
    else: 
        return product

def validate_exist_category(request, cat_id):
    category = request.dbsession.query(models.Category).filter_by(id=cat_id).first()
    if not category:
        return True
    else: 
        return category
    
def validate_data_stock_product(stock):
    validate_Stock = not stock >= 0
    if validate_Stock:
        return True

def validate_data_pvp_product(pvp):
    pvp_value = round(float(pvp),2)
    validate_Pvp = not pvp_value > 0
    if validate_Pvp:
        return True
    else:
        return pvp_value

def list_product(request):
    product_all = request.dbsession.query(models.Product).all()
    if not product_all:
        return True
    else:
        products_json = [product.product_to_dict() for product in product_all]
        return products_json
            
def create_product(request, name, image, stock, pvp, cat_id):
    new_product = models.Product(
        name=name,
        image=image,
        stock=stock,
        pvp=pvp,
        cat_id=cat_id
    )
    request.dbsession.add(new_product)
    request.dbsession.flush()
    return new_product.product_to_dict()

def update_product(request, product, name, image, stock, pvp, cat_id):
    if product.name == name:
        product.image = image
        product.stock = stock
        product.pvp = pvp
        product.cat_id = cat_id
    else:
        product.name = name
        product.image = image
        product.stock = stock
        product.pvp = pvp
        product.cat_id = cat_id
    request.dbsession.flush()
    return product.product_to_dict()

def delete_product(request, product_id):
    product = validate_exist_product(request, product_id)
    if product == True:
        return True
    else:
        request.dbsession.delete(product)
        request.dbsession.flush()
        return False