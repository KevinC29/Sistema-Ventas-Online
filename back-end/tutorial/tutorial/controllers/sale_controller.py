from ..models import models
import uuid

def validate_data_none_sale(date_joined, subtotal, iva, total, cli_id, detalle):
    validate_None = any(value is None for value in (date_joined, subtotal, iva, total, cli_id, detalle))
    return validate_None
    
def validate_data_type_sale(date_joined, subtotal, iva, total, cli_id, detalle):
    is_date_joined_valid = isinstance(date_joined, date)
    is_subtotal_valid = isinstance(subtotal, (float, int))
    is_iva_valid = isinstance(iva, (float, int))
    is_total_valid = isinstance(total, (float, int))
    is_cli_id_valid = isinstance(uuid.UUID(str(cli_id)) if isinstance(cli_id, str) else None, uuid.UUID)
    is_detalle_valid = isinstance(detalle, list)
    validate_Type = not all([is_date_joined_valid, is_subtotal_valid, is_iva_valid, is_total_valid, is_cli_id_valid, is_detalle_valid])
    return validate_Type

def validate_data_subtotal_sale(subtotal):
    subtotal_value = round(float(subtotal),2)
    validate_Subtotal = not subtotal_value > 0
    if validate_Subtotal:
        return True
    else:
        return subtotal_value

def validate_data_iva_sale(iva):
    iva_value = round(float(iva),2)
    validate_Iva = not iva_value >= 0
    if validate_Iva:
        return True
    else:
        return iva_value

def validate_data_total_sale(total):
    total_value = round(float(total),2)
    validate_Total = not total_value > 0
    if validate_Total:
        return True
    else:
        return total_value

def validate_exist_client(request, cli_id):
    client = request.dbsession.query(models.Client).filter_by(id=cli_id).first()
    if not client:
        return True

def create_sale(request, data_joined, subtotal, iva, total, cli_id, detalle):
    new_sale = models.Sale(
        date_joined= date_joined,
        subtotal= subtotal_value,
        iva= iva_value,
        total= total_value,
        cli_id= cli_id
    )
    request.dbsession.add(new_sale)
    request.dbsession.flush()
    return new_sale