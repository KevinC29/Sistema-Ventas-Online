from ..models import models
import uuid

def validate_data_none_detSale(prod_id, price, cant, subtotal):
    validate_None = any(value is None for value in (prod_id, price, cant, subtotal))
    return validate_None

def validate_data_type_detSale(prod_id, price, cant, subtotal):
    is_prod_id_valid = isinstance(uuid.UUID(str(prod_id)) if isinstance(prod_id, str) else None, uuid.UUID)
    is_price_valid = isinstance(price, (float, int))
    is_cant_valid = isinstance(cant, int)
    is_subtotal_valid = isinstance(subtotal, (float, int))
    validate_Type = not all([is_prod_id_valid, is_price_valid, is_cant_valid, is_subtotal_valid])
    return validate_Type

def validate_data_price_detSale(price):
    price_value = round(float(price),2)
    validate_Price = not price_value > 0
    return validate_Price

def validate_data_cant_detSale(cant):
    validate_Cant = not cant > 0
    return validate_Cant

def validate_data_subtotal_detSale(subtotal):
    subtotal_value = round(float(subtotal),2)
    validate_Subtotal = not subtotal_value > 0
    return validate_Subtotal

def validate_exist_product(request, prod_id):
    validate_Product = request.dbsession.query(models.Product).filter_by(id=prod_id).first()
    if not validate_Product:
        return True
    else:
        return validate_Product

def validate_value_price_detSale(request, prod_id, price):
    product = validate_exist_product(request, prod_id)
    price_value = round(float(price),2)
    if product.price != price_value:
        return True

def validate_value_stock_detSale(request, prod_id, cant):
    product = validate_exist_product(request, prod_id)
    if product.stock < cant:
        return True

def validate_value_subtotal_for_cant_detSale(request, prod_id, cant, subtotal):
    product = validate_exist_product(request, prod_id)
    subtotal_value_detalle = round(float(subtotal),2)
    if product.price * cant != subtotal_value_detalle:
        return True

def update_stock_product(request, prod_id, cant):
    product = validate_exist_product(request, prod_id)
    product.stock -= cant
    request.dbsession.flush()
    return print(product.product_to_dict())

def validate_data_list_detSale(request, detalle):
    message = ''
    cont_Subtotal = 0
    for det in detalle:
        prod_id = det.get('prod_id')
        price = det.get('price')
        cant = det.get('cant')
        subtotal = det.get('subtotal')
        if validate_data_none_detSale(prod_id, price, cant, subtotal):
            message = 'error data none'
            return True, message
        elif validate_data_type_detSale(prod_id, price, cant, subtotal):
            message = 'error data type'
            return True, message
        elif any(validate_data_price_detSale(price), 
            validate_data_cant_detSale(cant), 
            validate_data_subtotal_detSale(subtotal)):
            message = 'error data negative'
            return True, message
        elif validate_exist_product(request, prod_id):
            message = 'error product not found'
            return True, message
        elif validate_value_price_detSale(request, prod_id, price):
            message = 'error price product inconsistent'
            return True, message
        elif validate_value_stock_detSale(request, prod_id, cant):
            message = 'error stock insufficient'
            return True, message
        elif validate_value_subtotal_for_cant_detSale(request, prod_id, cant, subtotal):
            message = 'error subtotal inconsistent with cant'
            return True, message
        else:
            update_stock_product(request, prod_id, cant)
            subtotal_value_detalle = round(float(subtotal),2)
            cont_Subtotal += subtotal_value_detalle
    message = 'ok'
    return cont_Subtotal, message

def create_detSale(request, price, cant, subtotal, prod_id, sale):
    price_value = round(float(price),2)
    subtotal_value_detalle = round(float(subtotal),2)
    new_detSale = models.DetSale(
        price=price_value,
        cant=cant,
        subtotal=subtotal_value_detalle,
        prod_id=prod_id,
        sale=sale
    )
    request.dbsession.add(new_detSale)
    request.dbsession.flush()
    return print(new_detSale.detSale_to_dict())