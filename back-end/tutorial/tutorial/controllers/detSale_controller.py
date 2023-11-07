from ..models import models
import uuid

def validate_data_none_detSale(prod_id, price, cant, subtotal):
    validate_None = any(value is None for value in (prod_id, price, cant, subtotal))
    return validate_None

def validate_data_type_detSale(prod_id, price, cant, subtotal):
    is_prod_id_valid = isinstance(uuid.UUID(str(prod_id)), uuid.UUID) if isinstance(prod_id, str) else False
    is_price_valid = isinstance(price, (float, int))
    is_cant_valid = isinstance(cant, int)
    is_subtotal_valid = isinstance(subtotal, (float, int))
    validate_Type = not all([is_prod_id_valid, is_price_valid, is_cant_valid, is_subtotal_valid])
    return validate_Type

def validate_data_price_detSale(price):
    validate_Price = not round(float(price),2) > 0
    return validate_Price

def validate_data_cant_detSale(cant):
    validate_Cant = not cant > 0
    return validate_Cant

def validate_data_subtotal_detSale(subtotal):
    validate_Subtotal = not round(float(subtotal),2) > 0
    return validate_Subtotal

def validate_exist_product(request, prod_id):
    validate_Product = request.dbsession.query(models.Product).filter_by(id=prod_id).first()
    if not validate_Product:
        return True
    else:
        return validate_Product

def validate_value_price_detSale(product, price):
    if round(float(product.pvp),2) != round(float(price),2):
        return True
    else:
        return False

def validate_value_stock_detSale(product, cant):
    if product.stock < cant:
        return True
    else:
        return False

def validate_value_subtotal_for_cant_detSale(product, cant, subtotal):
    if rount(float(product.pvp) * cant,2) != round(float(subtotal),2):
        return True
    else:    
        return False

def validate_products_equal(data):
    prod_ids = [item['prod_id'] for item in data]

    for prod_id in set(prod_ids):
        count = prod_ids.count(prod_id)
        if count > 1:
            return True
    return False

def update_stock_product(request, prod_id, cant):
    product = validate_exist_product(request, prod_id)
    product.stock -= cant
    request.dbsession.flush()
    # return print(product.product_to_dict())

def validate_data_list_detSale(request, detalle):
    message = ''
    cont_Subtotal = 0

    if validate_products_equal(detalle):
        message = 'error data product duplicates'
        return True, message
    else:
        for det in detalle:
            prod_id = det.get('prod_id')
            price = det.get('price')
            cant = det.get('cant')
            subtotal = det.get('subtotal')

            product = validate_exist_product(request, prod_id)

            if validate_data_none_detSale(prod_id, price, cant, subtotal) :
                message = 'error data none'
                return True, message
            elif validate_data_type_detSale(prod_id, price, cant, subtotal) :
                message = 'error data type'
                return True, message
            elif any([validate_data_price_detSale(price),validate_data_cant_detSale(cant), validate_data_subtotal_detSale(subtotal)]) :
                message = 'error data negative or equal 0'
                return True, message
            elif True if product == True else False :
                message = 'error product not found'
                return True, message
            elif validate_value_price_detSale(product, price) if product != True else False :
                message = 'error price product inconsistent'
                return True, message
            elif validate_value_stock_detSale(product, cant) if product != True else False :
                message = 'error stock insufficient'
                return True, message
            elif validate_value_subtotal_for_cant_detSale(product, cant, subtotal) if product != True else False :
                message = 'error subtotal inconsistent with cant detSale'
                return True, message
            else:
                # update_stock_product(request, prod_id, cant)
                subtotal_value_detalle = round(float(subtotal),2)
                cont_Subtotal += subtotal_value_detalle
    message = 'ok'
    return cont_Subtotal, message

def create_detSale(request, price, cant, subtotal, prod_id, sale):
    new_detSale = models.DetSale(
        price = round(float(price),2),
        cant = cant,
        subtotal = round(float(subtotal),2),
        prod_id = prod_id,
        sale = sale
    )
    request.dbsession.add(new_detSale)
    request.dbsession.flush()
    # return print(new_detSale.detSale_to_dict())