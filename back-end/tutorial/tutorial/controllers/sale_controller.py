from ..models import models
import uuid
from decimal import Decimal
from datetime import datetime, date

def validate_data_none_sale(date_joined, subtotal, iva, total, cli_id, detalle):
    validate_None = any(value is None for value in (date_joined, subtotal, iva, total, cli_id, detalle))
    return validate_None
    
def validate_data_type_sale(date_joined, subtotal, iva, total, cli_id, detalle):
    is_date_joined_valid = isinstance(datetime.strptime(date_joined, "%Y-%m-%d").date(), date) if isinstance(date_joined, str) else False
    is_subtotal_valid = isinstance(subtotal, (float, int))
    is_iva_valid = isinstance(iva, (float, int))
    is_total_valid = isinstance(total, (float, int))
    is_cli_id_valid = isinstance(uuid.UUID(str(cli_id)), uuid.UUID) if isinstance(cli_id, str) else False
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
    else:
        return False

def validate_exist_sale(request, sale_id):
    sale = request.dbsession.query(models.Sale).filter_by(id=sale_id).first()
    if not sale:
        return True
    else:
        return sale

def validate_balance_client(request, cli_id, total):
    client = request.dbsession.query(models.Client).filter_by(id=cli_id).first()
    if client.balance < total:
        return True
    else:
        return False

def payment_sale(request, cli_id, total):
    client = request.dbsession.query(models.Client).filter_by(id=cli_id).first()
    client.balance -= Decimal(str(total))
    request.dbsession.flush()

def list_sale(request):
    sale_all = request.dbsession.query(models.Sale).all()
    if not sale_all:
        return True
    else:
        categories_json = [sale.sale_to_dict() for sale in sale_all]
        return categories_json

def create_sale(request, date_joined, subtotal, iva, total, cli_id):
    new_sale = models.Sale(
        date_joined = datetime.strptime(date_joined, "%Y-%m-%d").date(),
        subtotal = subtotal,
        iva = iva,
        total = total,
        cli_id = cli_id
    )
    request.dbsession.add(new_sale)
    request.dbsession.flush()
    return new_sale

def delete_sale(request, sale_id):
    sale = validate_exist_sale(request, sale_id)
    if sale == True:
        return True
    else:
        sale.delete(request)
        return False